"""Prospective coverage checks never promote a failed or incompletely tested patch."""
import copy
import unittest
import xml.etree.ElementTree as ET
from analyze_runs import source_syntax_collection_evidence
from evaluate_development import qualified_syntax_collection_pair


class SyntaxCoverageTests(unittest.TestCase):
    def fixture(self):
        good=dict(independently_verified=True,junit_case_names_sha256='all-clean-tests',junit_skipped_case_names=[])
        bad=dict(independently_verified=False,patch_source_syntax_collection_failure=True,
                 junit_collection_blocked=True,verifier_agreement=True,resolved=False,
                 test_like_patch_paths=[],verification_sensitive_patch_paths=[])
        expected=dict(case_names_sha256='all-clean-tests',skipped_case_names=[])
        return good,bad,expected

    def test_symmetric_and_failure_never_changes(self):
        a,b,e=self.fixture();before=copy.deepcopy(b)
        self.assertTrue(qualified_syntax_collection_pair(a,b,e))
        self.assertTrue(qualified_syntax_collection_pair(b,a,e))
        self.assertEqual(before,b)

    def test_missing_qualification_or_partial_positive_scope_rejected(self):
        a,b,e=self.fixture();self.assertFalse(qualified_syntax_collection_pair(a,b,{}))
        a['junit_case_names_sha256']='fewer-tests'
        self.assertFalse(qualified_syntax_collection_pair(a,b,e))

    def test_new_skip_or_missing_skip_receipt_rejected(self):
        a,b,e=self.fixture();a['junit_skipped_case_names']=[('x','failed_test')]
        self.assertFalse(qualified_syntax_collection_pair(a,b,e))
        a.pop('junit_skipped_case_names');self.assertFalse(qualified_syntax_collection_pair(a,b,e))

    def test_ordinary_dependency_errors_or_missing_verifier_rejected(self):
        for field in ('patch_source_syntax_collection_failure','junit_collection_blocked','verifier_agreement'):
            a,b,e=self.fixture();b[field]=False
            self.assertFalse(qualified_syntax_collection_pair(a,b,e))

    def test_changed_tests_or_verification_rejected(self):
        for field in ('test_like_patch_paths','verification_sensitive_patch_paths'):
            a,b,e=self.fixture();b[field]=['tests/test_a.py']
            self.assertFalse(qualified_syntax_collection_pair(a,b,e))

    def test_two_failures_not_repair_credit(self):
        a,b,e=self.fixture();a['independently_verified']=False
        self.assertFalse(qualified_syntax_collection_pair(a,b,e))

    def test_source_proof_requires_actual_patched_implementation(self):
        test=ET.Element('testcase');err=ET.SubElement(test,'error',message='collection failure')
        err.text='File "/tmp/swegemma_sandbox_probe/workspace/pkg/api.py", line 8\nIndentationError: bad indent'
        self.assertTrue(source_syntax_collection_evidence([test],['pkg/api.py'])['patch_source_syntax_collection_failure'])
        self.assertFalse(source_syntax_collection_evidence([test],['other.py'])['patch_source_syntax_collection_failure'])
        err.text=err.text.replace('IndentationError','ModuleNotFoundError')
        self.assertFalse(source_syntax_collection_evidence([test],['pkg/api.py'])['patch_source_syntax_collection_failure'])

    def test_all_errors_must_qualify_and_tests_cannot_supply_proof(self):
        test=ET.Element('testcase');err=ET.SubElement(test,'error',message='collection failure')
        err.text='File "/workspace/tests/test_a.py", line 8\nSyntaxError: invalid code'
        self.assertFalse(source_syntax_collection_evidence([test],['tests/test_a.py'])['patch_source_syntax_collection_failure'])
        self.assertFalse(source_syntax_collection_evidence([],[])['patch_source_syntax_collection_failure'])
        err.text=err.text.replace('tests/test_a.py','pkg/api.py')
        other=ET.Element('testcase');ET.SubElement(other,'error',message='collection failure').text='ModuleNotFoundError: dependency'
        self.assertFalse(source_syntax_collection_evidence([test,other],['pkg/api.py'])['patch_source_syntax_collection_failure'])


if __name__=='__main__':
    unittest.main()
