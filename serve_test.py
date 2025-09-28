#!/usr/bin/env python3
"""
Simple HTTP server to serve the test interface for CORS testing
"""
import http.server
import socketserver
import webbrowser
import os

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

def main():
    print(f"🌐 Starting local server for test interface...")
    print(f"📁 Serving from: {DIRECTORY}")
    print(f"🔗 URL: http://localhost:{PORT}")
    print(f"📄 Test interface: http://localhost:{PORT}/test_interface.html")
    print(f"🛑 Press Ctrl+C to stop the server")
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            # Open browser automatically
            webbrowser.open(f'http://localhost:{PORT}/test_interface.html')
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n🛑 Server stopped")

if __name__ == "__main__":
    main()