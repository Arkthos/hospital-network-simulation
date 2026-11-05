"""Classify only real observations. Unknown C or nonbinary P cannot be conforming."""
from common import BASE, rows, write_csv, RESULT_FIELDS
from validate_evidence import validate

def classify(p,c,o,valid):
    if valid!='true' or o not in {'allow','deny'} or p not in {'allow','deny'} or c not in {'allow','deny'}:
        return 'INDETERMINATE'
    if p==c==o:
        return 'CONFORMING'
    if p!=c and c==o:
        return 'DESIGN_OR_CONFIGURATION_GAP'
    if p==c and c!=o:
        return 'UNEXPECTED_BEHAVIOR'
    return 'COMPLEX_DISCREPANCY'

def main():
    errors=validate()
    if errors:
        raise SystemExit('\n'.join(errors))
    results=[]
    for o in rows(BASE/'results/observations.csv'):
        results.append(dict(test_id=o['test_id'],policy=o['policy_expected'],configuration=o['config_expected'],observed=o['observed'],classification=classify(o['policy_expected'],o['config_expected'],o['observed'],o['valid']),severity='not_assessed',evidence=o['evidence_path'],notes=o['notes']))
    write_csv(BASE/'results/results.csv',results,RESULT_FIELDS)
    write_csv(BASE/'results/discrepancies.csv',[r for r in results if r['classification'] not in {'CONFORMING','INDETERMINATE'}],RESULT_FIELDS)
    print(f'{len(results)} recorded runs classified; no pending test converted to an observation')

if __name__=='__main__':
    main()
