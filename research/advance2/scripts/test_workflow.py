"""Research integrity tests; all synthetic fixtures live only in temporary directories.
They are software tests, never Packet Tracer observations or experimental evidence.
"""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import common
from common import write_json, write_csv, OBS_FIELDS, digest
from parse_acl import parse_rule, evaluate, parse_files
from compare_pco import classify
import validate_evidence
import collect_evidence

class ACLTests(unittest.TestCase):
    def test_real_corpus_first_match(self):
        rules,bindings,errors=parse_files(sorted((common.ROOT/'Hospital network  simulation').rglob('*.txt')))
        self.assertFalse(errors)
        self.assertEqual(len(rules),80)
        self.assertEqual(len(bindings),10)
        self.assertEqual(evaluate(rules,'guestwifi','192.168.50.21','192.168.10.5','icmp')[0],'deny')
        self.assertEqual(evaluate(rules,'guestwifi','192.168.50.21','192.168.70.5','udp','49152','5246')[0],'allow')
        self.assertEqual(evaluate(rules,'guestwifi','192.168.50.21','192.168.70.5','tcp','49152','443')[0],'deny')
        self.assertEqual(evaluate(rules,'management','192.168.60.8','192.168.70.5','tcp','49152','443')[0],'allow')
        self.assertEqual(evaluate(rules,'management','192.168.60.9','192.168.70.5','tcp','49152','443')[0],'deny')
        self.assertEqual(evaluate(rules,'radius','192.168.70.5','192.168.80.5','udp','49152','1812')[0],'deny')

    def test_dhcp_source_destination_ports(self):
        r=parse_rule('permit udp any eq 68 any eq 67')
        r.update(acl='a',sequence=1,file='fixture',line=1)
        self.assertEqual(evaluate([r],'a','0.0.0.0','255.255.255.255','udp','68','67')[0],'allow')
        self.assertEqual(evaluate([r],'a','0.0.0.0','255.255.255.255','udp','67','68')[0],'deny')

    def test_unsupported_not_silent(self):
        with self.assertRaises(ValueError):
            parse_rule('permit tcp any any range 1 99')

class PCOTests(unittest.TestCase):
    def test_all_classifications_and_unknown(self):
        self.assertEqual(classify('deny','deny','deny','true'),'CONFORMING')
        self.assertEqual(classify('deny','allow','allow','true'),'DESIGN_OR_CONFIGURATION_GAP')
        self.assertEqual(classify('deny','deny','allow','true'),'UNEXPECTED_BEHAVIOR')
        self.assertEqual(classify('allow','deny','allow','true'),'COMPLEX_DISCREPANCY')
        self.assertEqual(classify('allow','unknown','allow','true'),'INDETERMINATE')
        self.assertEqual(classify('deny','deny','deny','false'),'INDETERMINATE')
        self.assertEqual(classify('conditional','deny','deny','true'),'INDETERMINATE')
        self.assertEqual(classify('allow','allow','error','false'),'INDETERMINATE')

class EvidenceTests(unittest.TestCase):
    def test_preflight_integrity_and_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)/'preflight'
            run = directory/'CP3-fixture'
            run.mkdir(parents=True)
            artifact = run/'fixture.txt'
            artifact.write_text('SOFTWARE FIXTURE', encoding='utf-8')
            m = dict(kind='preflight_not_test_result', baseline_commit='fixture',
                     artifacts=[dict(path='fixture.txt', sha256=digest(artifact))])
            write_json(run/'manifest.json', m)
            self.assertFalse(validate_evidence.validate_preflight(directory, 'fixture'))
            artifact.write_text('tampered', encoding='utf-8')
            self.assertTrue(validate_evidence.validate_preflight(directory, 'fixture'))
            m['artifacts'][0]['path'] = '../outside.txt'
            write_json(run/'manifest.json', m)
            self.assertTrue(any('outside directory' in e for e in validate_evidence.validate_preflight(directory, 'fixture')))

    def test_record_retest_refuse_overwrite_and_detect_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)/'advance2'
            base.mkdir()
            write_json(base/'baseline/hashes.json',{'baseline_commit':'fixture','files':[]})
            write_json(base/'policy/policy.yaml',{})
            t=dict(id='T001',source_vlan=50,destination_vlan=10,source_ip='unknown',destination_ip='192.168.10.5',protocol='icmp',policy_expected='allow',config_expected='unknown',positive_control_ids=['T001'])
            write_json(base/'tests/test-plan.yaml',{'tests':[t]})
            write_csv(base/'results/observations.csv',[],OBS_FIELDS)
            artifact=Path(tmp)/'actual-output.txt'
            artifact.write_text('SOFTWARE FIXTURE; NOT EXPERIMENTAL EVIDENCE',encoding='utf-8')
            meta=Path(tmp)/'input.json'
            m=dict(test_id='T001-R1',timestamp='2026-11-05T12:00:00-06:00',source='192.168.50.21',destination='192.168.10.5',method='fixture',packet_tracer_version='fixture',observed='allow',valid='true',notes='software fixture',causality='unknown',positive_control_runs=[],destination_verified=True,artifact_sources=[str(artifact)])
            def safe(relative):
                p=(base/relative).resolve()
                if not p.is_relative_to(base.resolve()):
                    raise ValueError('Outside base')
                return p
            with patch.object(common,'BASE',base),patch.object(collect_evidence,'BASE',base),patch.object(validate_evidence,'BASE',base),patch.object(validate_evidence,'safe_path',safe):
                write_json(meta,m)
                with contextlib.redirect_stdout(io.StringIO()):
                    collect_evidence.collect(meta)
                self.assertFalse(validate_evidence.validate())
                with self.assertRaises(ValueError):
                    collect_evidence.collect(meta)
                m['test_id']='T001-R2'
                write_json(meta,m)
                with contextlib.redirect_stdout(io.StringIO()):
                    collect_evidence.collect(meta)
                self.assertEqual(len(common.rows(base/'results/observations.csv')),2)
                self.assertFalse(validate_evidence.validate())
                a=next((base/'evidence/raw/T001-R1').glob('*.txt'))
                a.write_text('tampered',encoding='utf-8')
                self.assertTrue(any('hash mismatch' in e for e in validate_evidence.validate()))
                a.write_text('SOFTWARE FIXTURE; NOT EXPERIMENTAL EVIDENCE',encoding='utf-8')
                self.assertFalse(validate_evidence.validate())
                m['test_id']='T001-R3'
                m['observed']='deny'
                write_json(meta,m)
                with self.assertRaisesRegex(ValueError,'Deny lacks'):
                    collect_evidence.collect(meta)
                self.assertEqual(len(common.rows(base/'results/observations.csv')),2)
                self.assertFalse((base/'evidence/raw/T001-R3').exists())

    def test_path_traversal(self):
        with self.assertRaises(ValueError):
            common.safe_path('../../../../outside')

if __name__=='__main__':
    unittest.main()
