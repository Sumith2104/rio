"""
High-Performance Transparent HTTP Reverse Proxy (Port 8000 -> Port 8002)
Ensures seamless unified access whether user navigates to localhost:8000 or localhost:8002.
Supports all HTTP methods, headers, query params, streaming responses, and file downloads.
"""

import sys
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urljoin

TARGET_PORT = 8002
TARGET_HOST = f"http://127.0.0.1:{TARGET_PORT}"

class TransparentProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        self._proxy_request("GET")

    def do_POST(self):
        self._proxy_request("POST")

    def do_PUT(self):
        self._proxy_request("PUT")

    def do_DELETE(self):
        self._proxy_request("DELETE")

    def do_OPTIONS(self):
        self._proxy_request("OPTIONS")

    def do_HEAD(self):
        self._proxy_request("HEAD")

    def do_PATCH(self):
        self._proxy_request("PATCH")

    def _proxy_request(self, method: str):
        target_url = urljoin(TARGET_HOST, self.path)

        # Forward headers, excluding hop-by-hop
        headers = {}
        for key, val in self.headers.items():
            if key.lower() not in ["host", "connection", "transfer-encoding"]:
                headers[key] = val
        headers["Host"] = f"127.0.0.1:{TARGET_PORT}"

        # Read body if present
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        try:
            resp = requests.request(
                method=method,
                url=target_url,
                headers=headers,
                data=body,
                allow_redirects=False,
                stream=True,
                timeout=60
            )

            # Send response status
            self.send_response(resp.status_code)

            # Send response headers
            for k, v in resp.headers.items():
                if k.lower() not in ["transfer-encoding", "content-encoding", "content-length"]:
                    self.send_header(k, v)

            content = resp.content
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()

            if method != "HEAD":
                self.wfile.write(content)
        except Exception as err:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            err_json = f'{{"error": "Proxy error to backend port 8002: {str(err)}"}}'.encode('utf-8')
            self.wfile.write(err_json)

    def log_message(self, format, *args):
        # Suppress noisy access logs
        pass

def run(port=8000):
    server = HTTPServer(("0.0.0.0", port), TransparentProxyHandler)
    print(f"[*] Port 8000 Transparent Reverse Proxy active -> Forwarding to {TARGET_HOST}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    run()

