"""Project-scoped Kaggle TLS and Google storage transport for this server."""

import json
from datetime import datetime, timedelta, timezone
import ssl
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

import requests


class KaggleTLS(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.maximum_version = ssl.TLSVersion.TLSv1_2
        kwargs["ssl_context"] = context
        return super().init_poolmanager(*args, **kwargs)


_SESSION_SEND = requests.Session.send


def configure_kaggle_network(download_cache=None):
    original = _SESSION_SEND

    def send(session, request, **kwargs):
        host = urlsplit(request.url).hostname
        if host == "api.kaggle.com":
            session.mount("https://api.kaggle.com/", KaggleTLS())
            kwargs["timeout"] = (10, 60)
        if host != "storage.googleapis.com" or request.method != "GET":
            return original(session, request, **kwargs)

        # Signed URLs go through stdin, never command arguments or logs.
        if download_cache is not None:
            download_cache.parent.mkdir(parents=True, exist_ok=True)
            command = ["curl", "--silent", "--fail", "--location", "--connect-timeout", "10",
                       "--max-time", "28800", "--continue-at", "-",
                       "--output", str(download_cache), "--config", "-"]
            result = subprocess.run(command,
                                    input=("url = " + json.dumps(request.url) + "\n").encode(),
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode:
                raise requests.ConnectionError("Model download interrupted; partial file retained")
            response = requests.Response()
            response.status_code = 200
            response.headers["Content-Length"] = str(download_cache.stat().st_size)
            response.url = request.url
            response.request = request
            response.raw = download_cache.open("rb")
            return response

        body = tempfile.TemporaryFile()
        settings = "url = " + json.dumps(request.url) + "\n"
        for name in ("Range", "If-Range"):
            if name in request.headers:
                settings += "header = " + json.dumps(name + ": " + request.headers[name]) + "\n"
        with tempfile.TemporaryDirectory(prefix="gemma-download-") as folder:
            header_path = Path(folder) / "headers"
            command = ["curl", "--silent", "--fail", "--location", "--connect-timeout", "10",
                       "--max-time", "1800",
                       "--dump-header", str(header_path), "--config", "-"]
            result = subprocess.run(
                command, input=settings.encode(), stdout=body,
                stderr=subprocess.DEVNULL,
            )
            if result.returncode:
                body.close()
                raise requests.ConnectionError("Google storage download failed")
            headers = header_path.read_text().strip().split("\n\n")[-1].splitlines()
        body.seek(0)
        response = requests.Response()
        response.status_code = int(headers[0].split()[1])
        response.headers.update(dict(line.split(": ", 1) for line in headers[1:] if ": " in line))
        response.url = request.url
        response.request = request
        response.raw = body
        return response

    requests.Session.send = send


def authenticate_kaggle(api):
    """Use the SDK credentials, refreshing OAuth before the real expiry boundary.

    kaggle 2.2.4 may reuse a token until 30 minutes after its recorded expiry.
    Keep the installed SDK's refresh/save behavior and account/scopes; never retry
    an API or submission after a failure, and never include credentials in errors.
    """
    from kaggle.api.kaggle_api_extended import KaggleCredentials

    try:
        api.authenticate()
        if api.config_values.get("auth_method") != "OAUTH":
            return
        with api.build_kaggle_client() as client:
            creds = KaggleCredentials.load(client=client)
            if creds is None:
                raise RuntimeError("Kaggle OAuth credential state is unavailable")
            expiry = creds._access_token_expiration
            if expiry is None or expiry.tzinfo is None:
                raise RuntimeError("Kaggle OAuth expiry is unavailable")
            # One minute covers the interval before the next authenticated request.
            if expiry <= datetime.now(timezone.utc) + timedelta(seconds=60):
                creds.refresh_access_token()
                token = creds.get_access_token()
                if not token or creds.get_username() != api.config_values.get(api.CONFIG_NAME_USER):
                    raise RuntimeError("Kaggle OAuth renewal did not preserve the account")
                api.config_values[api.CONFIG_NAME_TOKEN] = token
    except requests.RequestException as error:
        status = error.response.status_code if error.response is not None else None
        detail = f"HTTP {status}" if status is not None else type(error).__name__
        raise RuntimeError(f"Kaggle authentication failed: {detail}") from None
