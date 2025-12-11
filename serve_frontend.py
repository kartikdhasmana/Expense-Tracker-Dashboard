#!/usr/bin/env python3
"""
Simple HTTP server to serve the web frontend.
Run this from the web-frontend directory.
"""
import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 3000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def serve():
    # Change to web-frontend directory
    web_frontend_dir = os.path.join(os.path.dirname(__file__), 'web-frontend')
    if os.path.exists(web_frontend_dir):
        os.chdir(web_frontend_dir)
    
    # Start server
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"🌐 Web frontend server running at http://localhost:{PORT}")
        print("📱 Open this URL in your browser to access the app")
        print("🛑 Press Ctrl+C to stop the server")
        
        # Open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}')
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🔴 Server stopped")

if __name__ == "__main__":
    serve()