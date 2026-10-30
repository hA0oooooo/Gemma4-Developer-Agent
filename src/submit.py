"""Submit from Linux using a reachable Google upload address."""

import argparse
import hashlib
import json
import socket
from pathlib import Path

import requests
from kaggle_network import authenticate_kaggle, configure_kaggle_network
from kaggle.api.kaggle_api_extended import (
    ApiStartSubmissionUploadRequest,
    KaggleApi,
    ResumableUploadResult,
)

ROOT = Path(__file__).resolve().parents[1]
COMPETITION = "gemma-4-developer-agent"


def configure_upload_route():
    original = socket.getaddrinfo

    def resolve(host, *args, **kwargs):
        # Both services accept the upload hostname; retain its TLS/SNI checks.
        if host == "www.googleapis.com":
            host = "storage.googleapis.com"
        return original(host, *args, **kwargs)

    socket.getaddrinfo = resolve


class ServerKaggleApi(KaggleApi):
    def upload_complete(self, path, url, quiet, resume=False):
        try:
            with open(path, "rb") as source:
                response = requests.put(url, data=source, timeout=(10, 60))
        except requests.RequestException as error:
            # Signed upload URLs must not appear in error messages.
            raise RuntimeError(f"Upload failed: {type(error).__name__}") from None
        if response.status_code not in (200, 201):
            raise RuntimeError(f"Upload failed: HTTP {response.status_code}")
        print(f"Uploaded submission.zip: HTTP {response.status_code}")
        return ResumableUploadResult.COMPLETE


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-upload", action="store_true",
                        help="Test file upload without creating a scored submission")
    parser.add_argument("--message",
                        help="Description recorded with the scored submission")
    parser.add_argument("--file", type=Path, required=True,
                        help="Explicit frozen archive; there is no default package")
    args = parser.parse_args(argv)
    if not args.check_upload and not (args.message and args.message.strip()):
        parser.error("--message is required for a scored submission")
    path = args.file.expanduser().resolve()
    if not path.is_file() or path.stat().st_size == 0:
        parser.error("--file must name an existing, nonempty archive")
    print(json.dumps({"archive": path.name, "bytes": path.stat().st_size,
                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}))
    configure_kaggle_network()
    configure_upload_route()
    api = ServerKaggleApi()
    authenticate_kaggle(api)

    if args.check_upload:
        with api.build_kaggle_client() as client:
            request = ApiStartSubmissionUploadRequest()
            request.competition_name = COMPETITION
            request.file_name = path.name
            request.content_length = path.stat().st_size
            request.last_modified_epoch_seconds = int(path.stat().st_mtime)
            result = client.competitions.competition_api_client.start_submission_upload(request)
        api.upload_complete(path, result.create_url, quiet=True)
        print("Upload check complete; no scored submission created")
    else:
        if api.competition_get_submission_limits(COMPETITION).num_allowed_now < 1:
            raise RuntimeError("No official submissions remaining today")
        try:
            result = api.competition_submit(
                str(path), args.message, COMPETITION, quiet=True)
        except requests.RequestException as error:
            # The request may have been accepted; never retry or print signed URLs.
            status = error.response.status_code if error.response is not None else None
            detail = f"HTTP {status}" if status is not None else type(error).__name__
            raise RuntimeError(
                f"Submission request failed: {detail}; reconcile the official list before any new request"
            ) from None
        print(result.message)


if __name__ == "__main__":
    main()
