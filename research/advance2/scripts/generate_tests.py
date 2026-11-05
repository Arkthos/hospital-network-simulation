"""Generate a conservative case policy and 14 nonredundant tests, without observations."""
from common import BASE, read_json, write_json, write_csv, write_text, OBS_FIELDS
from parse_acl import evaluate
from common import rows

# Case design decisions; independent of ACL parsing. These are not observed facts.
CASES = [
    # source VLAN, destination VLAN/zone, protocol, port, P, category, positive control
    (50,'external','icmp','none','allow','external-connectivity','T001'),
    (50,10,'icmp','none','deny','guest-isolation','T001,T013'),
    (50,60,'icmp','none','deny','management','T001'),
    (50,80,'icmp','none','deny','radius','T001'),
    (50,40,'icmp','none','deny','guest-isolation','T001,T006'),
    (40,'external','icmp','none','allow','external-connectivity','T006'),
    (40,10,'icmp','none','deny','internal-access','T006,T013'),
    (40,60,'icmp','none','deny','management','T006'),
    (60,70,'tcp','443','allow','wlc','T009'),
    (60,80,'tcp','22','allow','radius','T009'),
    (30,80,'icmp','none','deny','radius','T013'),
    (30,60,'icmp','none','deny','management','T013'),
    (30,10,'icmp','none','allow','negative-control','T013'),
    (50,70,'tcp','443','deny','wlc','T001,T009'),
]
ZONES = {10:'Internal Server',30:'Hospitalstaff cableado',40:'Corp Wi-Fi movilidad',50:'Guest Wi-Fi',60:'Management autorizado',70:'WLC',80:'RADIUS','external':'External fuera del ASA'}
ACL_BY_SOURCE = {40:'wifi',50:'guestwifi',60:'management',70:'wlc'}
ACL_BY_DEST = {10:'intserver',80:'radius'}

def packet_path(rules, sv, dv, src, dst, protocol, sport, dport):
    checks = []
    if sv in ACL_BY_SOURCE:
        checks.append(evaluate(rules, ACL_BY_SOURCE[sv],src,dst,protocol,sport,dport))
    if dv in ACL_BY_DEST:
        checks.append(evaluate(rules, ACL_BY_DEST[dv],src,dst,protocol,sport,dport))
    return checks

def main():
    observations=BASE/'results/observations.csv'
    if observations.exists() and rows(observations):
        raise SystemExit('Campaign already has observations: refusing to replace policy/test plan. Create a separate campaign.')
    rules = rows(BASE / 'baseline/acl_rules.csv')
    # Only representative packet addresses for evaluating subnet rules, never endpoint assignments.
    tests, policy = [], []
    for i, (sv,dv,proto,port,p,cat,controls) in enumerate(CASES,1):
        tid = f'T{i:03}'
        src = '192.168.60.8' if sv==60 else f'192.168.{sv}.254'
        dst = '192.168.70.5' if dv==70 else ('192.168.10.5' if dv==10 else ('203.0.113.254' if dv=='external' else f'192.168.{dv}.254'))
        forward = packet_path(rules,sv,dv,src,dst,proto,'49152',port)
        reverse = packet_path(rules,dv,sv,dst,src,proto,port,'49152')
        checks = forward + reverse
        acl_expected = 'deny' if any(x[0]=='deny' for x in checks) else ('unknown' if any(x[0]=='unknown' for x in checks) else 'allow')
        # A permit through known MLS ACLs is insufficient to establish end-to-end C.
        c = 'deny' if acl_expected=='deny' else 'unknown'
        rationale = ('Política propuesta del caso: acceso externo para movilidad sin acceso clínico interno.' if sv==40 else
                     'Política propuesta del caso: acceso administrativo mínimo desde bastión autorizado.' if sv==60 else
                     'Política propuesta del caso: aislamiento de invitados y protección de zonas administrativas.' if p=='deny' else
                     'Política propuesta del caso: conectividad funcional de control y servicios autorizados.')
        policy.append(dict(policy_id='P'+tid[1:],source_zone=ZONES[sv],destination_zone=ZONES[dv],service=proto+('/'+port if proto=='tcp' else ' echo'),expected=p,rationale=rationale,objective='OE2',status='proposed_case_policy',scope='Servicio concreto de este caso, no todos los protocolos'))
        notes = 'C derivada exclusivamente de fragmentos textuales; validar su aplicación en ambos MLS y su correspondencia con PKT. '
        if c=='unknown':
            notes += 'Las ACL MLS conocidas no bloquean este intercambio; routing/ASA/NAT o servicio del destino no verificados impiden predecir conectividad completa. '
        if i==12:
            notes += 'La solicitud ICMP no tiene deny de entrada a Management identificado; la respuesta sería bloqueada por management in. No equivale a demostrar aislamiento de solicitudes.'
        if i==10:
            notes += 'No consta que el servidor RADIUS simule SSH; no habilitarlo para que la prueba funcione. Si no existe, resultado indeterminate.'
        if dv=='external':
            notes += 'Seleccionar host externo real de la topología; no usar DMZ ni IP pública hairpin como sustituto de Internet. 203.0.113.254 solo se usa internamente como representante matemático; no es un objetivo a ejecutar.'
        tests.append(dict(id=tid,policy_id='P'+tid[1:],objective='OE2',category=cat,secondary_categories=['segmentation'] if sv!=dv else [],source=ZONES[sv],source_vlan=sv,source_ip='192.168.60.8' if sv==60 else 'unknown',destination=ZONES[dv],destination_vlan=dv,destination_ip=dst if dv in {10,70} else 'unknown',protocol=proto,port=port,policy_expected=p,config_expected=c,acl_exchange_expected=acl_expected,config_basis=[dict(decision=a,reference=b) for a,b in checks],forward_acl_decisions=[dict(decision=a,reference=b) for a,b in forward],reverse_acl_decisions=[dict(decision=a,reference=b) for a,b in reverse],execution_method='Packet Tracer GUI: '+('Desktop Command Prompt: ping <confirmed_destination_ip>' if proto=='icmp' else ('Desktop Web Browser: https://192.168.70.5' if port=='443' else 'Desktop Command Prompt: ssh -l <existing_user> <confirmed_radius_ip>')),acceptance_criteria='Registrar entrega/respuesta real por servicio; timeout solo no demuestra ACL. Para deny válido verificar control positivo y destino activo; indeterminate ante prerrequisito ausente.',evidence_required=['endpoint IP/SSID/gateway','comando o acción y salida real','captura real o transcripción verificable','configuración y trazado PDU para atribuir causa','manifest con SHA-256'],positive_control_ids=controls.split(','),status='pending_endpoint_verification',notes=notes))
    document = dict(schema_version=1,policy_status='Propuesta explícita para caso hipotético; no política aprobada por hospital real',decisions=['VLAN40: movilidad no clínica; acceso interno denegado por diseño del caso, no por deducción del nombre staff','No se evalúa autenticación RADIUS de clientes hasta confirmar AAA efectivo','Management administrativo por TCP443 WLC y TCP22 RADIUS solo si servicio existe; ICMP no sustituye administración'],additional_rules=[dict(policy_id='P-GUEST-OTHER',source_zone='Guest',destination_zone='otras redes internas',service='ip',expected='deny',rationale='Aislamiento; DMZ publicada se trata separadamente',objective='OE2'),dict(policy_id='P-GUEST-CAPWAP',source_zone='AP autorizado exclusivamente',destination_zone='WLC',service='udp/5246,5247',expected='conditional',rationale='Tráfico de infraestructura; no concede a clientes Guest acceso administrativo',objective='OE2'),dict(policy_id='P-AUTH',source_zone='clientes WLAN',destination_zone='WLAN',service='autenticación representada',expected='conditional',rationale='Inventariar SSID y WPA2-PSK efectivo antes de diseñar prueba; no asumir AAA',objective='OE1'),dict(policy_id='P-CRYPTO',source_zone='WLAN',destination_zone='WLAN',service='seguridad criptográfica real',expected='not_testable',rationale='Fuera del alcance experimental de Packet Tracer',objective='OE1')],policies=policy)
    write_json(BASE / 'policy/policy.yaml',document)
    write_text(BASE / 'policy/policy.md','# Política propuesta del caso\n\nJSON compatible con YAML 1.2; Python estándar evita una dependencia de parsing YAML.\n\n'+'\n'.join('- '+x for x in document['decisions'])+'\n\n'+ '\n'.join(f"- {x['policy_id']}: {x['source_zone']} → {x['destination_zone']}, {x['service']}: **{x['expected']}**. {x['rationale']}" for x in policy)+'\n\nLa documentación original afirma Corp Wi-Fi sin acceso clínico; se adopta una política hospitalaria explícita de movilidad restringida. No representa una WLAN clínica autorizada. Un cambio a acceso clínico sería otra política versionada antes de CP3, sin cambiar baseline.\n')
    write_json(BASE / 'tests/test-plan.yaml',dict(schema_version=1,tests=tests))
    fields = ['id','objective','category','source','source_vlan','source_ip','destination','destination_vlan','destination_ip','protocol','port','policy_expected','config_expected','acl_exchange_expected','execution_method','acceptance_criteria','positive_control_ids','status','notes']
    write_csv(BASE / 'tests/test-plan.csv',tests,fields)
    write_json(BASE / 'tests/test-schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','required':['schema_version','tests'],'properties':{'schema_version':{'const':1},'tests':{'type':'array','items':{'type':'object','required':list(tests[0]),'properties':{'id':{'type':'string','pattern':'^T[0-9]{3}$'},'policy_expected':{'enum':['allow','deny','conditional','not_testable']},'config_expected':{'enum':['allow','deny','unknown']},'protocol':{'enum':['icmp','tcp','udp']}}}}}})
    if not (BASE / 'results/observations.csv').exists():
        write_csv(BASE / 'results/observations.csv',[],OBS_FIELDS)
    for t in tests:
        d = BASE / 'evidence/raw' / t['id']
        d.mkdir(parents=True,exist_ok=True)
        template = d / 'manifest.template.json'
        if not template.exists():
            write_json(template,dict(test_id=t['id'],timestamp='',baseline_commit=read_json(BASE/'baseline/hashes.json')['baseline_commit'],packet_tracer_version='',source='',destination='',method='',expected_policy=t['policy_expected'],expected_config=t['config_expected'],observed='',artifacts=[],notes='PLANTILLA SIN EJECUTAR; no es evidencia'))
    write_text(BASE / 'tests/test-procedures.md','# Procedimientos por caso\n\nAplicar primero docs/advance2/PACKET_TRACER_EXECUTION.md; IP unknown se resuelve mediante inspección, nunca por asignación de nuevas IP. Controles T001/T006/T013 se ejecutan primero.\n\n'+ '\n\n'.join(f"## {t['id']} — {t['source']} → {t['destination']}\n\nP={t['policy_expected']}; C={t['config_expected']}; decisión del intercambio en ACL conocidas={t['acl_exchange_expected']}.\n\nOrigen: VLAN {t['source_vlan']}, IP {t['source_ip']}. Destino: VLAN {t['destination_vlan']}, IP {t['destination_ip']}.\n\nAcción: `{t['execution_method']}`.\n\nControles: {', '.join(t['positive_control_ids'])}. {t['acceptance_criteria']}\n\n{t['notes']}\n\nEvidencia: `evidence/raw/{t['id']}/` (plantilla únicamente); crear ejecución inmutable `{t['id']}-R1` con collect_evidence.py. Registrar IP, comando, salida, hora, controles y causa. " for t in tests)+'\n')
    print(f'{len(tests)} tests generated; no observations created')

if __name__ == '__main__':
    main()
