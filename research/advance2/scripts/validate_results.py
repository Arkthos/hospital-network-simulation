"""Quality gates for policy, test plan, observations, results and analytical traceability."""
import argparse
from common import BASE, rows, read_json, plan
from validate_evidence import validate as validate_evidence

def validate(require_complete=False):
    errors=validate_evidence()
    tests=plan()
    ids=[t['id'] for t in tests]
    if len(ids)!=len(set(ids)):
        errors.append('Duplicate test IDs')
    policies=read_json(BASE/'policy/policy.yaml')['policies']
    pmap={p['policy_id']:p for p in policies}
    if len(pmap)!=len(policies):
        errors.append('Duplicate policy IDs')
    required=read_json(BASE/'tests/test-schema.json')['properties']['tests']['items']['required']
    for t in tests:
        for key in required:
            if key not in t or t[key] in ('',None):
                errors.append(t.get('id','?')+': missing '+key)
        if t.get('policy_expected') not in {'allow','deny','conditional','not_testable'} or t.get('config_expected') not in {'allow','deny','unknown'}:
            errors.append(t['id']+': invalid P/C')
        if t.get('objective') not in {'OE1','OE2','OE3'} or t.get('protocol') not in {'icmp','tcp','udp'}:
            errors.append(t['id']+': invalid objective/protocol')
        if t.get('policy_id') not in pmap or pmap[t['policy_id']]['expected']!=t['policy_expected']:
            errors.append(t['id']+': missing/conflicting policy')
        for control in t.get('positive_control_ids',[]):
            if control not in ids:
                errors.append(t['id']+': unknown positive control')
    obs=rows(BASE/'results/observations.csv')
    observed_ids={o['test_id'] for o in obs}
    results_path=BASE/'results/results.csv'
    results=rows(results_path) if results_path.exists() else []
    if len({r['test_id'] for r in results})!=len(results):
        errors.append('Duplicate result IDs')
    for r in results:
        if r['test_id'] not in observed_ids:
            errors.append('Result without observation: '+r['test_id'])
        else:
            from compare_pco import classify
            o=next(o for o in obs if o['test_id']==r['test_id'])
            expected=classify(o['policy_expected'],o['config_expected'],o['observed'],o['valid'])
            if r['classification']!=expected or r['policy']!=o['policy_expected'] or r['configuration']!=o['config_expected'] or r['observed']!=o['observed'] or r['evidence']!=o['evidence_path']:
                errors.append('Result inconsistent with observation: '+r['test_id'])
    if results_path.exists() and observed_ids!={r['test_id'] for r in results}:
        errors.append('Stale/incomplete results; regenerate comparison')
    analytical=read_json(BASE/'analysis/traceability.json')
    findings={f['finding_id']:f for f in analytical['findings']}
    for f in findings.values():
        if not f.get('test_ids') or any(t not in ids for t in f['test_ids']):
            errors.append('Finding without valid test IDs: '+f['finding_id'])
        if not f.get('evidence_basis'):
            errors.append('Finding without evidence: '+f['finding_id'])
    for p in analytical['proposed_controls']:
        if not p.get('finding_ids') or any(f not in findings for f in p['finding_ids']):
            errors.append('Recommendation without findings')
        if not p.get('verification_test') or not p.get('evidence_basis'):
            errors.append('Recommendation lacks verification/evidence')
    if require_complete and set(ids)!={o['test_id'].split('-R')[0] for o in obs}:
        errors.append('CP3 incomplete: not all tests have recorded runs')
    return errors

if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('--require-complete',action='store_true')
    args=a.parse_args()
    problems=validate(args.require_complete)
    for p in problems:
        print('ERROR:',p)
    print(f'Quality validation: {len(problems)} critical errors; CP3 completion required={args.require_complete}')
    raise SystemExit(bool(problems))
