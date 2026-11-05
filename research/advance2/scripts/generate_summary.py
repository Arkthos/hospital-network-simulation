"""Per-case metrics use first recorded run, preserving all retests separately."""
from collections import Counter
from common import BASE, rows, write_json, write_text, plan
from compare_pco import classify
from validate_results import validate

def main():
    errors=validate()
    if errors:
        raise SystemExit('\n'.join(errors))
    observations=rows(BASE/'results/observations.csv')
    first={}
    for o in observations:
        first.setdefault(o['test_id'].split('-R')[0],o)
    labels=Counter(classify(o['policy_expected'],o['config_expected'],o['observed'],o['valid']) for o in first.values())
    valid=sum(o['valid']=='true' and o['observed'] in {'allow','deny'} for o in first.values())
    policy_matches=sum(o['valid']=='true' and o['observed'] in {'allow','deny'} and o['policy_expected']==o['observed'] for o in first.values())
    conforming=labels['CONFORMING']
    summary=dict(total_tests=len(plan()),executed_tests=len(first),recorded_runs=len(observations),pending_tests=len(plan())-len(first),valid_tests=valid,conforming=conforming,design_configuration_gaps=labels['DESIGN_OR_CONFIGURATION_GAP'],unexpected_behavior=labels['UNEXPECTED_BEHAVIOR'],complex_discrepancies=labels['COMPLEX_DISCREPANCY'],indeterminate=labels['INDETERMINATE'],conformity_rate=100*conforming/valid if valid else None,policy_agreement_rate=100*policy_matches/valid if valid else None,metric_note='Conformity is P=C=O among valid first runs; unknown C prevents conformity. Policy agreement reports P=O separately. Neither metric is a network security percentage.',run_selection='first recorded run per test; all retests retained; no cherry-picking',status='CP2; CP3 pending' if not first else 'experimental observations; review completion gate')
    write_json(BASE/'results/summary.json',summary)
    write_text(BASE/'results/summary.md','# Reporte técnico provisional\n\n'+ '\n'.join(f'- {k}: {v}' for k,v in summary.items())+'\n\nNo hay resultados académicos ni conclusión de seguridad derivados de casos pendientes. C unknown puede coexistir con una observación válida; su clasificación permanece INDETERMINATE. Conformity_rate usa el numerador solicitado P=C=O; policy_agreement_rate distingue la coincidencia estricta P=O para evitar atribuir al primero un significado diferente.\n')
    print(f'{len(first)}/{len(plan())} cases executed; conformity={summary["conformity_rate"]}')

if __name__=='__main__':
    main()
