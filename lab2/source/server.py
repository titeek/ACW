#!/usr/bin/env python3
import http.server
import socketserver
import os
from datetime import datetime
from urllib.parse import urlparse, parse_qs

#print('source code for "http.server":', http.server.__file__)

class web_server(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
 
        path = urlparse(self.path)
        query_params = parse_qs(path.query) 
        
        if path.path == '/':
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()
            if not query_params:            
                self.wfile.write(b"Hello World!\n")
            elif(query_params.get('cmd', None) == ['time']):
                self.wfile.write(str.encode(datetime.now().strftime("%H:%M:%S")))
            elif(query_params.get('cmd', None) == ['rev']):
                string_to_reverse = query_params.get('str', None)[0]
                if string_to_reverse:
                    self.wfile.write(str.encode(string_to_reverse[::-1]))
        else:
            super().do_GET()
    
# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
