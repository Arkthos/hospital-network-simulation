"""Shared, standard-library-only research utilities. JSON is a YAML 1.2 subset."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'research/advance2'
OBS_FIELDS = 'test_id timestamp source destination protocol policy_expected config_expected observed valid evidence_path notes'.split()
RESULT_FIELDS = 'test_id policy configuration observed classification severity evidence notes'.split()

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def write_json(path, data):
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')

def rows(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def write_csv(path, data, fields):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with Path(path).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore', lineterminator='\n')
        w.writeheader()
        w.writerows(data)

def safe_path(relative):
    p = (BASE / relative).resolve()
    if not p.is_relative_to(BASE.resolve()):
        raise ValueError('Path outside research directory: ' + relative)
    return p

def plan():
    return read_json(BASE / 'tests/test-plan.yaml')['tests']
