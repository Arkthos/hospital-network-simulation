"""Validate immutable source hashes and all recorded evidence. Nonzero on critical error."""
from datetime import datetime
import ipaddress
import re
from common import ROOT, BASE, digest, read_json, rows, safe_path, plan

def validate_preflight(directory, baseline_commit):
    errors = []
    for manifest in directory.glob('*/manifest.json'):
        try:
            m = read_json(manifest)
            if m['kind'] != 'preflight_not_test_result' or m['baseline_commit'] != baseline_commit:
                raise ValueError('Preflight kind/baseline mismatch')
            listed = set()
            for artifact in m['artifacts']:
                p = (manifest.parent / artifact['path']).resolve()
                if not p.is_relative_to(manifest.parent.resolve()) or p == manifest.resolve():
                    raise ValueError('Preflight artifact outside directory')
                if p in listed:
                    raise ValueError('Duplicate preflight artifact')
                listed.add(p)
                if not p.is_file() or digest(p) != artifact['sha256']:
                    raise ValueError('Preflight evidence missing/hash mismatch')
            actual = {p.resolve() for p in manifest.parent.rglob('*') if p.is_file() and p != manifest}
            if not listed or actual != listed:
                raise ValueError('Unhashed/unlisted preflight evidence')
        except (ValueError, KeyError, TypeError, OSError) as e:
            errors.append(manifest.parent.name + ': ' + str(e))
    return errors

def validate():
    errors = []
    frozen = read_json(BASE/'baseline/hashes.json')
    errors.extend(validate_preflight(BASE/'evidence/preflight', frozen['baseline_commit']))
    for f in frozen['files']:
        p = ROOT/f['path']
        if not p.is_file() or digest(p)!=f['sha256']:
            errors.append('Baseline missing/modified: '+f['path'])
    preflight=BASE/'baseline/gui-preflight.txt'
    checksum=BASE/'baseline/gui-preflight.sha256'
    if preflight.exists() or checksum.exists():
        if not preflight.is_file() or not checksum.is_file() or digest(preflight)!=checksum.read_text(encoding='utf-8').split()[0]:
            errors.append('GUI preflight missing/modified')
    tests = {t['id']:t for t in plan()}
    observations = rows(BASE/'results/observations.csv')
    seen = set()
    for o in observations:
        run = o['test_id']
        if not re.fullmatch(r'T\d{3}-R[1-9]\d*',run):
            errors.append('Invalid run ID: '+run)
        if run in seen:
            errors.append('Duplicate observation: '+run)
        seen.add(run)
        tid = run.split('-R')[0]
        t = tests.get(tid)
        if not t:
            errors.append('Unknown test: '+run)
            continue
        try:
            path = safe_path(o['evidence_path'])
            if not o['evidence_path'] or path.name!='manifest.json' or not path.is_file():
                raise ValueError('Missing manifest')
            m = read_json(path)
            required = ['test_id','timestamp','baseline_commit','packet_tracer_version','source','destination','method','expected_policy','expected_config','observed','artifacts','notes','valid','protocol','causality','positive_control_runs','destination_verified','plan_sha256','policy_sha256']
            for key in required:
                if key not in m:
                    raise ValueError('Manifest missing '+key)
            if m['test_id']!=run or m['baseline_commit']!=frozen['baseline_commit']:
                raise ValueError('Run/baseline mismatch')
            if m['plan_sha256']!=digest(BASE/'tests/test-plan.yaml') or m['policy_sha256']!=digest(BASE/'policy/policy.yaml'):
                raise ValueError('Plan/policy changed after observation')
            dt=datetime.fromisoformat(m['timestamp'])
            if dt.tzinfo is None:
                raise ValueError('Timestamp needs timezone')
            for key in ['timestamp','source','destination','observed','protocol','valid','notes']:
                if str(m[key]) != str(o[key]):
                    raise ValueError('Observation/manifest mismatch: '+key)
            if not all(m[k] for k in ['source','destination','packet_tracer_version','method']):
                raise ValueError('Missing execution metadata')
            if m['protocol']!=t['protocol']:
                raise ValueError('Protocol mismatch')
            for field,vlan in [('source',t['source_vlan']),('destination',t['destination_vlan'])]:
                ip=ipaddress.ip_address(m[field])
                if isinstance(vlan,int) and ip not in ipaddress.ip_network(f'192.168.{vlan}.0/24'):
                    raise ValueError('Endpoint outside expected VLAN: '+field)
                if t[field+'_ip']!='unknown' and m[field]!=t[field+'_ip']:
                    raise ValueError('Known endpoint mismatch')
            if m['expected_policy']!=t['policy_expected'] or m['expected_config']!=t['config_expected'] or o['policy_expected']!=t['policy_expected'] or o['config_expected']!=t['config_expected']:
                raise ValueError('P/C mismatch with locked plan')
            if m['observed'] not in {'allow','deny','indeterminate','error'} or m['valid'] not in {'true','false'}:
                raise ValueError('Invalid O/valid value')
            if m['observed'] in {'indeterminate','error'} and m['valid']=='true':
                raise ValueError('Indeterminate/error cannot be valid')
            if m['causality'] not in {'confirmed','strongly_supported','possible','unknown'}:
                raise ValueError('Invalid causality')
            if not isinstance(m['destination_verified'],bool) or not isinstance(m['positive_control_runs'],list):
                raise ValueError('Invalid control metadata types')
            if not m['artifacts']:
                raise ValueError('No evidence artifacts')
            listed = set()
            for a in m['artifacts']:
                p = safe_path(a['path'])
                if not p.is_relative_to(path.parent.resolve()) or p.name=='manifest.json':
                    raise ValueError('Artifact outside immutable run')
                if a['path'] in listed:
                    raise ValueError('Duplicate artifact')
                listed.add(a['path'])
                if not p.is_file() or len(a.get('sha256',''))!=64 or digest(p)!=a['sha256']:
                    raise ValueError('Evidence missing/hash mismatch: '+a['path'])
            actual = {p.relative_to(BASE).as_posix() for p in path.parent.rglob('*') if p.is_file() and p.name!='manifest.json'}
            if actual != listed:
                raise ValueError('Unhashed/unlisted evidence file')
            if m['valid']=='true' and m['observed']=='deny':
                if not m['destination_verified'] or not m['positive_control_runs']:
                    raise ValueError('Deny lacks reachable destination/positive controls')
                for control in m['positive_control_runs']:
                    matches=[x for x in observations if x['test_id']==control and x['valid']=='true' and x['observed']=='allow']
                    if not matches or control.split('-R')[0] not in t['positive_control_ids']:
                        raise ValueError('Invalid/unobserved positive control: '+control)
        except (ValueError, KeyError, TypeError, OSError) as e:
            errors.append(run+': '+str(e))
    recorded_paths = {o['evidence_path'] for o in observations}
    for p in (BASE/'evidence/raw').glob('*/manifest.json'):
        if p.relative_to(BASE).as_posix() not in recorded_paths:
            errors.append('Orphan evidence manifest: '+str(p))
    return errors

def main():
    errors=validate()
    for e in errors:
        print('ERROR:', e)
    print(f'Evidence validation: {len(errors)} critical errors. Empty observations are pending, not observed outcomes.')
    raise SystemExit(bool(errors))

if __name__=='__main__':
    main()
