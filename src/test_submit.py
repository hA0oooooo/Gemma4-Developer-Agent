"""Submission entry regressions; fake clients only, no Kaggle requests."""
from contextlib import ExitStack, redirect_stdout, redirect_stderr
import hashlib
import io
from pathlib import Path
import tempfile
import traceback
import unittest
from unittest.mock import MagicMock, patch
import requests
import submit

class SubmissionEntryTests(unittest.TestCase):
    def setUp(self):
        self.stack=ExitStack();self.addCleanup(self.stack.close)
        self.directory=self.stack.enter_context(tempfile.TemporaryDirectory())
        self.archive=Path(self.directory)/'submission.zip';self.archive.write_bytes(b'test archive bytes')
        self.stdout=io.StringIO();self.stderr=io.StringIO()
        self.stack.enter_context(redirect_stdout(self.stdout));self.stack.enter_context(redirect_stderr(self.stderr))
        self.network=self.stack.enter_context(patch.object(submit,'configure_kaggle_network'))
        self.route=self.stack.enter_context(patch.object(submit,'configure_upload_route'))
        self.factory=self.stack.enter_context(patch.object(submit,'ServerKaggleApi'))
        self.api=self.factory.return_value
        self.api.competition_get_submission_limits.return_value.num_allowed_now=1
        self.api.competition_submit.return_value.message='accepted fake request'
    def args(self):return ['--file',str(self.archive),'--message','Explicit frozen candidate']
    def assert_rejected_without_client(self,args):
        with self.assertRaises(SystemExit) as error:submit.main(args)
        self.assertEqual(error.exception.code,2)
        self.factory.assert_not_called();self.network.assert_not_called();self.route.assert_not_called()
    def test_no_default_archive(self):self.assert_rejected_without_client([])
    def test_formal_description_required(self):self.assert_rejected_without_client(['--file',str(self.archive)])
    def test_blank_description_rejected(self):self.assert_rejected_without_client(['--file',str(self.archive),'--message','  '])
    def test_missing_archive_rejected_before_auth(self):
        self.archive.unlink();self.assert_rejected_without_client(self.args())
    def test_empty_archive_rejected_before_auth(self):
        self.archive.write_bytes(b'');self.assert_rejected_without_client(self.args())
    def test_directory_rejected_before_auth(self):
        self.archive.unlink();self.archive.mkdir();self.assert_rejected_without_client(self.args())
    def test_formal_request_once_with_explicit_identity(self):
        submit.main(self.args())
        self.api.authenticate.assert_called_once_with()
        self.network.assert_called_once_with();self.route.assert_called_once_with()
        self.api.competition_submit.assert_called_once_with(str(self.archive.resolve()),'Explicit frozen candidate',submit.COMPETITION,quiet=True)
        self.assertIn(hashlib.sha256(self.archive.read_bytes()).hexdigest(),self.stdout.getvalue())
        self.assertIn('accepted fake request',self.stdout.getvalue())
    def test_auth_failure_never_uploads_or_submits(self):
        with patch.object(submit, 'authenticate_kaggle', side_effect=RuntimeError('Auth unavailable')):
            with self.assertRaisesRegex(RuntimeError, 'Auth unavailable'):
                submit.main(self.args())
        self.api.competition_get_submission_limits.assert_not_called()
        self.api.build_kaggle_client.assert_not_called()
        self.api.upload_complete.assert_not_called()
        self.api.competition_submit.assert_not_called()
    def test_no_quota_never_submits(self):
        self.api.competition_get_submission_limits.return_value.num_allowed_now=0
        with self.assertRaisesRegex(RuntimeError,'No official submissions'):submit.main(self.args())
        self.api.competition_submit.assert_not_called()
    def test_ambiguous_timeout_never_retries_or_exposes_url(self):
        self.api.competition_submit.side_effect=requests.Timeout('https://example.invalid/upload?signature=FAKE_TEST_VALUE')
        with self.assertRaisesRegex(RuntimeError,'reconcile the official list') as error:submit.main(self.args())
        self.api.competition_submit.assert_called_once()
        formatted=''.join(traceback.format_exception(error.exception))
        self.assertNotIn('FAKE_TEST_VALUE',formatted);self.assertNotIn('https://',formatted)
        self.assertIn('Timeout',formatted)
    def test_http_error_reports_status_without_body(self):
        response=requests.Response();response.status_code=400
        self.api.competition_submit.side_effect=requests.HTTPError('FAKE_SENSITIVE_RESPONSE',response=response)
        with self.assertRaisesRegex(RuntimeError,'HTTP 400') as error:submit.main(self.args())
        self.api.competition_submit.assert_called_once()
        self.assertNotIn('FAKE_SENSITIVE_RESPONSE',''.join(traceback.format_exception(error.exception)))
    def test_upload_check_requires_file_but_no_formal_description(self):
        client=MagicMock();self.api.build_kaggle_client.return_value.__enter__.return_value=client
        client.competitions.competition_api_client.start_submission_upload.return_value.create_url='https://example.invalid/fake-upload'
        submit.main(['--check-upload','--file',str(self.archive)])
        request=client.competitions.competition_api_client.start_submission_upload.call_args.args[0]
        self.assertEqual(request.file_name,'submission.zip');self.assertEqual(request.content_length,self.archive.stat().st_size)
        self.api.upload_complete.assert_called_once_with(self.archive.resolve(),'https://example.invalid/fake-upload',quiet=True)
        self.api.competition_submit.assert_not_called();self.api.competition_get_submission_limits.assert_not_called()
        self.assertIn('no scored submission created',self.stdout.getvalue())

if __name__=='__main__':unittest.main()
