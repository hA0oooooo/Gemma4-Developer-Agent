"""Scripted OpenAI-compatible stub used only to exercise the official harness.

This is not a model and produces no meaningful solution. It exists so the agent
loop, tool execution, patch extraction and Phase 2 verification can be
validated on a machine without a GPU or an official model mount.
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PLAN = [
    ("run_command", {"command": "ls /workspace && git -C /workspace log --oneline -1"}),
    ("run_command", {"command": "echo '<!-- harness plumbing marker -->' >> /workspace/README.md"}),
    ("submit_patch", {}),
]


class Handler(BaseHTTPRequestHandler):
    calls = 0

    def log_message(self, *args):
        pass

    def _send(self, payload):
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send({"object": "list", "data": [{"id": "mock", "object": "model"}]})

    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        Handler.calls += 1
        index = Handler.calls - 1
        if index < len(PLAN):
            name, arguments = PLAN[index]
            message = {
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": f"call_{index}",
                    "type": "function",
                    "function": {"name": name, "arguments": json.dumps(arguments)},
                }],
            }
            finish = "tool_calls"
        else:
            message = {"role": "assistant", "content": "Done."}
            finish = "stop"
        self._send({
            "id": f"mock-{Handler.calls}",
            "object": "chat.completion",
            "created": 1800000000,
            "model": "mock",
            "choices": [{"index": 0, "message": message, "finish_reason": finish}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
        })


def serve(port=0):
    """Starts the stub server in a daemon thread and returns (server, base_url)."""
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}/v1"
