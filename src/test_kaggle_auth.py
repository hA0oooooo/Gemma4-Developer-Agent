"""OAuth expiry regressions using actual SDK expiry state and fake refresh only."""
from contextlib import ExitStack
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
import traceback
import unittest
from unittest.mock import MagicMock, patch

from kaggle.api.kaggle_api_extended import KaggleCredentials
import requests
import kaggle_network


class KaggleAuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.now = datetime.now(timezone.utc)
        self.api = SimpleNamespace(authenticate=MagicMock(), build_kaggle_client=MagicMock(),
            config_values={"auth_method": "OAUTH", "username": "fixture-user", "token": "expired-fixture"},
            CONFIG_NAME_USER="username", CONFIG_NAME_TOKEN="token")
        self.creds = KaggleCredentials(client=MagicMock(), refresh_token="invalid-test-fixture",
            access_token="expired-fixture", access_token_expiration=self.now - timedelta(minutes=1),
            username="fixture-user", scopes=["fixture-scope"])
        self.loader = self.stack.enter_context(patch.object(KaggleCredentials, "load", return_value=self.creds))
        self.refresh = self.stack.enter_context(patch.object(self.creds, "refresh_access_token", side_effect=self.renew))
        clock = self.stack.enter_context(patch.object(kaggle_network, "datetime"))
        clock.now.return_value = self.now

    def renew(self):
        self.creds._access_token = "renewed-fixture"
        self.creds._access_token_expiration = self.now + timedelta(hours=1)

    def test_sdk_expiry_gap_is_refreshed_once_and_bound_to_client(self):
        self.assertFalse(self.creds.access_token_has_expired())
        kaggle_network.authenticate_kaggle(self.api)
        self.api.authenticate.assert_called_once_with()
        self.refresh.assert_called_once_with()
        self.assertEqual(self.api.config_values["token"], "renewed-fixture")

    def test_future_oauth_token_does_not_refresh(self):
        self.creds._access_token_expiration = self.now + timedelta(minutes=2)
        kaggle_network.authenticate_kaggle(self.api)
        self.refresh.assert_not_called()
        self.assertEqual(self.api.config_values["token"], "expired-fixture")

    def test_one_minute_boundary_refreshes(self):
        self.creds._access_token_expiration = self.now + timedelta(seconds=60)
        kaggle_network.authenticate_kaggle(self.api)
        self.refresh.assert_called_once_with()

    def test_legacy_auth_does_not_load_or_refresh_oauth(self):
        self.api.config_values["auth_method"] = "LEGACY_API_KEY"
        kaggle_network.authenticate_kaggle(self.api)
        self.api.authenticate.assert_called_once_with()
        self.loader.assert_not_called()
        self.refresh.assert_not_called()

    def test_missing_oauth_state_stops(self):
        self.loader.return_value = None
        with self.assertRaisesRegex(RuntimeError, "credential state"):
            kaggle_network.authenticate_kaggle(self.api)
        self.refresh.assert_not_called()

    def test_unknown_or_naive_expiry_stops(self):
        for expiry in [None, self.now.replace(tzinfo=None)]:
            with self.subTest(expiry=expiry):
                self.creds._access_token_expiration = expiry
                with self.assertRaisesRegex(RuntimeError, "expiry"):
                    kaggle_network.authenticate_kaggle(self.api)
        self.refresh.assert_not_called()

    def test_refresh_failure_is_not_retried_or_logged(self):
        response = requests.Response()
        response.status_code = 401
        self.refresh.side_effect = requests.HTTPError("https://example.invalid/?secret=INVALID_FIXTURE", response=response)
        with self.assertRaisesRegex(RuntimeError, "HTTP 401") as error:
            kaggle_network.authenticate_kaggle(self.api)
        self.refresh.assert_called_once_with()
        formatted = "".join(traceback.format_exception(error.exception))
        self.assertNotIn("INVALID_FIXTURE", formatted)
        self.assertNotIn("https://", formatted)
        self.assertEqual(self.api.config_values["token"], "expired-fixture")

    def test_initial_auth_error_stops_without_refresh_or_sensitive_text(self):
        self.api.authenticate.side_effect = requests.Timeout("https://example.invalid/?secret=AUTH_FIXTURE")
        with self.assertRaisesRegex(RuntimeError, "authentication failed: Timeout") as error:
            kaggle_network.authenticate_kaggle(self.api)
        self.refresh.assert_not_called()
        self.loader.assert_not_called()
        self.assertNotIn("AUTH_FIXTURE", "".join(traceback.format_exception(error.exception)))

    def test_renewal_cannot_silently_change_account(self):
        self.creds._username = "other-fixture"
        with self.assertRaisesRegex(RuntimeError, "preserve the account"):
            kaggle_network.authenticate_kaggle(self.api)
        self.refresh.assert_called_once_with()
        self.assertEqual(self.api.config_values["token"], "expired-fixture")


if __name__ == "__main__":
    unittest.main()
