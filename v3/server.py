# server.py
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import List, Dict

from jinja2 import Template

class EmailHandler(BaseHTTPRequestHandler):
    """
    Minimal HTTP handler that serves pre-rendered HTML emails from memory.
    - GET /0 serves the first email, /1 the second, etc.
    - No disk writes; everything is in the class variable.
    """
    emails: List[str] = []

    def do_GET(self):
        try:
            # Strip leading "/" and parse index; default to 0 when hitting "/"
            path = self.path.strip("/")
            idx = int(path) if path else 0

            if 0 <= idx < len(self.emails):
                html = self.emails[idx]
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
            else:
                self.send_error(404, "Email not found")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")

def render_emails(customers: List[Dict], template_path: str = "email_template.html") -> List[str]:
    """
    Load the Jinja2 template once and render an HTML string per customer.
    Returns a list of HTML documents (strings).
    """
    template = Template(Path(template_path).read_text(encoding='utf-8'))
    return [
        template.render(
            customer_name=c['customer_name'],
            account_number=c['account_number'],
            renewal_link=c['renewal_link'],
            physical_address=c['physical_address'],
            products=c['products']
        )
        for c in customers
    ]

def start_server_and_open_tabs(rendered_emails: List[str], host: str = "localhost", port: int = 8000) -> int:
    """
    Start a background HTTP server and open each email in a separate browser tab.
    Returns the number of opened tabs.
    """
    EmailHandler.emails = rendered_emails

    server = HTTPServer((host, port), EmailHandler)

    # Run server in a daemon thread so the main thread can keep printing and exit on Ctrl+C
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    # Open each email in its own browser tab
    for i in range(len(rendered_emails)):
        webbrowser.open_new_tab(f"http://{host}:{port}/{i}")

    return len(rendered_emails)
