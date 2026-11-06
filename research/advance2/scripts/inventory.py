"""Inventory committed baseline sources, retaining per-line provenance and unknowns."""
import ipaddress
import re
import subprocess
import xml.etree.ElementTree as ET
from zipfile import ZipFile, BadZipFile
from common import ROOT, BASE, digest, write_json, write_csv, write_text, read_json
from parse_acl import main as parse_acls

def build():
    manifest = BASE / 'baseline/hashes.json'
    if manifest.exists():
        frozen = read_json(manifest)
        for item in frozen['files']:
            p = ROOT / item['path']
            if not p.is_file() or digest(p) != item['sha256']:
                raise SystemExit('Baseline changed: ' + item['path'])
        base_commit = frozen['baseline_commit']
    else:
        base_commit = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip()
    files = subprocess.check_output(['git','ls-tree','-r','--name-only',base_commit], cwd=ROOT, text=True).splitlines()
    hashes, vlans, interfaces, networks, features, documents = [], [], [], [], [], []
    for name in files:
        p = ROOT / name
        hashes.append(dict(path=name, bytes=p.stat().st_size, sha256=digest(p)))
        if p.suffix.lower() == '.docx':
            try:
                with ZipFile(p) as z:
                    text = '\n'.join(''.join(t.text or '' for t in para.iter() if t.tag.endswith('}t')) for para in ET.fromstring(z.read('word/document.xml')).iter() if para.tag.endswith('}p'))
                    documents.append(dict(file=name, text=text, embedded_images=sum(n.startswith('word/media/') for n in z.namelist()), status='text extracted; historical images not new observations'))
            except BadZipFile:
                documents.append(dict(file=name, text='unknown', status='not OOXML ZIP; OLE signature; extension mismatch; not converted'))
        if p.suffix.lower() != '.txt':
            continue
        vlan, interface, pool = None, 'unknown', 'unknown'
        for n, raw in enumerate(p.read_text(encoding='utf-8-sig', errors='replace').splitlines(), 1):
            s = raw.strip()
            provenance = dict(file=name, line=n, raw=s)
            m = re.fullmatch(r'vlan\s+(\d+)', s, re.I)
            if m:
                vlan = m[1]
                vlans.append(dict(vlan_id=vlan, name='unknown', **provenance))
            elif vlan and s.startswith('name '):
                vlans[-1]['name'] = s[5:]
                vlan = None
            m = re.match(r'(?:int|interface)\s+(.+)', s, re.I)
            if m:
                interface = m[1].strip().lower().replace('vlan ', 'vlan')
                interfaces.append(dict(interface=interface, **provenance))
            m = re.fullmatch(r'ip dhcp pool (\S+)', s)
            if m:
                pool = m[1]
            m = re.fullmatch(r'(?:ip add(?:ress)?|net(?:work)?)\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)(.*)', s)
            if m:
                kind = 'interface' if s.startswith('ip ') else ('ospf' if 'area' in m[3] else 'dhcp')
                try:
                    network = str(ipaddress.ip_network(m[1] + '/' + m[2], strict=False))
                except ValueError:
                    network = 'unknown'
                networks.append(dict(address=m[1], mask_or_wildcard=m[2], network=network, kind=kind, interface=interface if kind=='interface' else 'unknown', dhcp_pool=pool if kind=='dhcp' else 'unknown', **provenance))
            if re.match(r'(?:ip route|route |router |standby |ip dhcp|default-rout|option |sw |switchport |ip access-group|access-group |nat |logging |aaa |ssh |inspect |security-level |nameif )', s):
                features.append(dict(interface=interface, **provenance))
    pkt = [h for h in hashes if h['path'].endswith('.pkt')]
    frozen = dict(baseline_commit=base_commit, capture_date='2026-11-05', timezone='America/Costa_Rica', files=hashes)
    if not manifest.exists():
        write_json(manifest, frozen)
    elif frozen['files'] != read_json(manifest)['files']:
        raise SystemExit('Refusing to replace frozen baseline manifest')
    inv = dict(baseline_commit=base_commit, file_count=len(files), packet_tracer=dict(product_version='9.0.1.0858', executable='C:/Program Files/Cisco Packet Tracer 9.0.1/bin/PacketTracer.exe', source='Windows executable VersionInfo; not packet creation version'), packets=pkt, packets_identical=len({x['sha256'] for x in pkt})==1, interfaces=interfaces, features=features, documents=documents, unknowns=['Saved .pkt state vs text configurations not yet compared','Live endpoint names/IPs and external target unknown','RADIUS IP and enabled services unknown','SSID/authentication documented, not yet observed','Embedded historical screenshots not re-executed','Two misnamed .docx files not readable as OOXML'])
    write_json(BASE / 'baseline/inventory.json', inv)
    write_csv(BASE / 'baseline/vlans.csv', vlans, ['vlan_id','name','file','line','raw'])
    write_csv(BASE / 'baseline/networks.csv', networks, ['address','mask_or_wildcard','network','kind','interface','dhcp_pool','file','line','raw'])
    write_json(BASE / 'baseline/document-text.json', documents)
    write_text(BASE / 'baseline/inventory.md', '# Inventario baseline\n\n' + f"Commit: `{base_commit}`. {len(files)} archivos originales; {len(pkt)} PKT idénticos por SHA-256.\n\n" + 'VLAN declaradas: ' + ', '.join(sorted({v['vlan_id'] for v in vlans}, key=int)) + '.\n\n' + 'Fuentes: inventory.json (interfaces y comandos con línea), vlans.csv, networks.csv, acl_rules.csv, acl_bindings.csv y document-text.json. Las filas repetidas conservan procedencia por dispositivo; no son nuevas VLAN. OSPF utiliza wildcard IOS y máscara ASA; se conserva el valor original.\n\n## Desconocidos\n\n' + '\n'.join('- ' + s for s in inv['unknowns']) + '\n')
    parse_acls()
    print(f'Inventoried {len(files)} original files; immutable commit {base_commit}')

if __name__ == '__main__':
    build()
