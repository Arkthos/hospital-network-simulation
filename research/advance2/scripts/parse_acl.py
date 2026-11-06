"""Deterministic parser for the named IOS/ASA ACL forms present in this corpus.
Unsupported syntax is recorded, never treated as a permit or silently discarded.
"""
import ipaddress
import re
from common import BASE, ROOT, write_csv

PORTS = {'domain': 53, 'www': 80, 'https': 443, 'ssh': 22}

def address(tokens, i):
    if tokens[i] == 'any':
        return '0.0.0.0', '255.255.255.255', i + 1
    if tokens[i] == 'host':
        ipaddress.IPv4Address(tokens[i + 1])
        return tokens[i + 1], '0.0.0.0', i + 2
    ipaddress.IPv4Address(tokens[i])
    ipaddress.IPv4Address(tokens[i + 1])
    return tokens[i], tokens[i + 1], i + 2

def parse_rule(text):
    t = text.split()
    action, protocol = t[:2]
    if action not in {'permit', 'deny'} or protocol not in {'ip', 'icmp', 'tcp', 'udp'}:
        raise ValueError('Unsupported action/protocol')
    src, sw, i = address(t, 2)
    sport = 'any'
    if i < len(t) and t[i] == 'eq':
        sport, i = t[i + 1], i + 2
    dst, dw, i = address(t, i)
    dport = 'any'
    if i < len(t) and t[i] == 'eq':
        dport, i = t[i + 1], i + 2
    if i != len(t):
        raise ValueError('Unsupported suffix')
    return dict(action=action, protocol=protocol, source=src, source_wildcard=sw,
                source_port=sport, destination=dst, destination_wildcard=dw, destination_port=dport)

def parse_files(paths):
    rules, bindings, errors = [], [], []
    for path in paths:
        acl, interface = None, 'unknown'
        relative = path.relative_to(ROOT).as_posix()
        for line, raw in enumerate(path.read_text(encoding='utf-8-sig', errors='replace').splitlines(), 1):
            s = raw.strip()
            m = re.fullmatch(r'ip access-list extended\s+(\S+)', s)
            if m:
                acl = m[1]
                continue
            m = re.match(r'(?:int|interface)\s+(.+)', s, re.I)
            if m:
                interface = m[1].strip().lower().replace('vlan ', 'vlan')
                acl = None
            m = re.fullmatch(r'ip access-group (\S+) (in|out)', s)
            if m:
                bindings.append(dict(acl=m[1], interface=interface, direction=m[2], file=relative, line=line, scope='both MLS (folder claim; runtime unverified)'))
            m = re.fullmatch(r'access-group (\S+) (in|out) interface (\S+)', s)
            if m:
                bindings.append(dict(acl=m[1], interface=m[3], direction=m[2], file=relative, line=line, scope='ASA'))
            m = re.fullmatch(r'access-list (\S+) extended (.+)', s)
            rule_acl, body = (m[1], m[2]) if m else (acl, s)
            if rule_acl and re.match(r'^(permit|deny)\b', body):
                try:
                    rule = parse_rule(body)
                    rule.update(acl=rule_acl, file=relative, line=line,
                                sequence=1 + sum(r['acl'] == rule_acl and r['file'] == relative for r in rules), raw=s)
                    rules.append(rule)
                except (ValueError, IndexError) as e:
                    errors.append(dict(file=relative, line=line, raw=s, error=str(e)))
    return rules, bindings, errors

def contains(ip, base, wildcard):
    mask = (~int(ipaddress.IPv4Address(wildcard))) & 0xffffffff
    return int(ipaddress.IPv4Address(ip)) & mask == int(ipaddress.IPv4Address(base)) & mask

def port_matches(wanted, actual):
    return wanted == 'any' or (actual != 'unknown' and str(PORTS.get(wanted, wanted)) == str(actual))

def evaluate(rules, acl, src, dst, protocol, sport='unknown', dport='unknown'):
    """First-match packet decision, NOT an end-to-end connectivity prediction."""
    selected = [r for r in rules if r['acl'] == acl]
    if not selected:
        return 'unknown', 'ACL absent'
    for r in selected:
        if r['protocol'] not in {'ip', protocol}:
            continue
        if contains(src, r['source'], r['source_wildcard']) and contains(dst, r['destination'], r['destination_wildcard']) and port_matches(r['source_port'], sport) and port_matches(r['destination_port'], dport):
            return ('allow' if r['action'] == 'permit' else 'deny'), f"{r['file']}:{r['line']} ({acl} #{r['sequence']})"
    return 'deny', f'{acl}: implicit deny'

def main():
    rules, bindings, errors = parse_files(sorted((ROOT / 'Hospital network  simulation').rglob('*.txt')))
    from common import write_json
    write_csv(BASE / 'baseline/acl_rules.csv', rules, ['acl','sequence','action','protocol','source','source_wildcard','source_port','destination','destination_wildcard','destination_port','file','line','raw'])
    write_csv(BASE / 'baseline/acl_bindings.csv', bindings, ['acl','interface','direction','scope','file','line'])
    write_json(BASE / 'baseline/acl_parse_errors.json', errors)
    if errors:
        raise SystemExit('Unsupported ACL syntax; review acl_parse_errors.json')
    print(f'{len(rules)} ACL rules, {len(bindings)} bindings, no unsupported ACL rules')

if __name__ == '__main__':
    main()
