"""Register actual artifacts in a new immutable run; never execute simulated traffic.
An input JSON supplies metadata; artifacts are copied, hashed and verified before append.
"""
import argparse
from datetime import datetime
import json
import re
import shutil
import ipaddress
from common import BASE, plan, read_json, write_json, digest, rows, OBS_FIELDS

def collect(metadata_path):
    m=read_json(metadata_path)
    run=m['test_id']
    if not re.fullmatch(r'T\d{3}-R[1-9]\d*',run):
        raise ValueError('Use T001-R1, T001-R2, ...')
    t=next(t for t in plan() if t['id']==run.split('-R')[0])
    for k in ['timestamp','source','destination','method','packet_tracer_version','observed','valid','notes','causality','positive_control_runs','destination_verified','artifact_sources']:
        if k not in m:
            raise ValueError('Missing '+k)
    if datetime.fromisoformat(m['timestamp']).tzinfo is None:
        raise ValueError('Timezone required')
    for field,vlan in [('source',t['source_vlan']),('destination',t['destination_vlan'])]:
        ip=ipaddress.ip_address(m[field])
        if isinstance(vlan,int) and ip not in ipaddress.ip_network(f'192.168.{vlan}.0/24'):
            raise ValueError('Endpoint outside expected VLAN: '+field)
        if t[field+'_ip']!='unknown' and m[field]!=t[field+'_ip']:
            raise ValueError('Known endpoint mismatch; freeze a revised plan before execution')
    if not m['artifact_sources']:
        raise ValueError('Actual evidence files required')
    dest=BASE/'evidence/raw'/run
    if dest.exists():
        raise ValueError('Run exists; never overwrite evidence')
    old=rows(BASE/'results/observations.csv')
    if any(o['test_id']==run for o in old):
        raise ValueError('Observation exists')
    # Stage in a temporary sibling; retain it for investigation on unexpected failure.
    stage=BASE/'evidence/raw'/('.staging-'+run)
    stage.mkdir(parents=True,exist_ok=False)
    artifacts=[]
    for n,source in enumerate(m.pop('artifact_sources'),1):
        from pathlib import Path
        src=Path(source).resolve()
        if not src.is_file():
            raise ValueError('Evidence source missing')
        name=f'{n:02}-'+src.name
        shutil.copyfile(src,stage/name)
        artifacts.append(dict(path=(dest/name).relative_to(BASE).as_posix(),sha256=digest(stage/name)))
    m.update(baseline_commit=read_json(BASE/'baseline/hashes.json')['baseline_commit'],expected_policy=t['policy_expected'],expected_config=t['config_expected'],protocol=t['protocol'],artifacts=artifacts,plan_sha256=digest(BASE/'tests/test-plan.yaml'),policy_sha256=digest(BASE/'policy/policy.yaml'))
    write_json(stage/'manifest.json',m)
    # Validate a complete snapshot in a temporary copy BEFORE publishing or appending.
    import tempfile
    import validate_evidence
    with tempfile.TemporaryDirectory() as tmp:
        from pathlib import Path
        trial=Path(tmp)/'advance2'
        shutil.copytree(BASE,trial,ignore=shutil.ignore_patterns('.staging-*','runtime','__pycache__'))
        shutil.copytree(stage,trial/'evidence/raw'/run)
        obs=dict(test_id=run,timestamp=m['timestamp'],source=m['source'],destination=m['destination'],protocol=t['protocol'],policy_expected=t['policy_expected'],config_expected=t['config_expected'],observed=m['observed'],valid=m['valid'],evidence_path=(dest/'manifest.json').relative_to(BASE).as_posix(),notes=m['notes'])
        from common import write_csv
        write_csv(trial/'results/observations.csv',old+[obs],OBS_FIELDS)
        saved=validate_evidence.BASE
        validate_evidence.BASE=trial
        # safe_path is bound in common; temporarily bind the trial resolver.
        original_safe=validate_evidence.safe_path
        def trial_safe(relative):
            p=(trial/relative).resolve()
            if not p.is_relative_to(trial.resolve()):
                raise ValueError('Path traversal')
            return p
        validate_evidence.safe_path=trial_safe
        try:
            errors=validate_evidence.validate()
        finally:
            validate_evidence.BASE=saved
            validate_evidence.safe_path=original_safe
        if errors:
            raise ValueError('\n'.join(errors))
    stage.rename(dest)
    import csv
    with (BASE/'results/observations.csv').open('a',encoding='utf-8',newline='') as f:
        csv.DictWriter(f,fieldnames=OBS_FIELDS).writerow(obs)
    print('Recorded immutable run '+run+'; regenerate comparison and summary')

if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('metadata_json')
    try:
        collect(a.parse_args().metadata_json)
    except (ValueError,KeyError,StopIteration,OSError) as e:
        raise SystemExit(str(e))
