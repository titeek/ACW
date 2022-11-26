#!/usr/bin/env python3
import http.server
import socketserver
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs

#print('source code for "http.server":', http.server.__file__)

class web_server(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
 
        path = urlparse(self.path)
        query_params = parse_qs(path.query) 
        document = query_params.get('str', None)
        
        if path.path == '/':
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=UTF-8")
            self.end_headers()

            if document:
                word = document[0]
                result =  { "lowercase" : 0, "uppercase" : 0, "digits" : 0, "special" : 0}

                for char in word:
                    if char.islower():
                        result["lowercase"] += 1
                    elif char.isupper():
                        result["uppercase"] += 1
                    elif char.isdigit():
                        result["digits"] += 1
            
            self.wfile.write(str.encode(json.dumps(result)))

        else:
            super().do_GET()
    
# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("",PORT), web_server)
tcp_server.serve_forever()
