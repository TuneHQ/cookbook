import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from cashgpt import cashgpt_controller  # Import the controller function

# Define the request handler class
class RequestHandler(BaseHTTPRequestHandler):
    
    def _send_response(self, response_data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type') 
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    # Handle POST requests
    def do_POST(self):
        # Check if the request path is /api/cashgpt
        if self.path == '/api/cashgpt':
            content_length = int(self.headers['Content-Length']) 
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse the data as JSON
                data = json.loads(post_data)
                
                # Check if 'hukum' key is in the data
                if 'hukum' not in data:
                    response_data = {"error": "Missing 'hukum' key"}
                    self._send_response(response_data, status=400)
                    return
                
                # Process the 'hukum' value
                hukum_value = data['hukum']
                # Call the controller function
                response_data = cashgpt_controller(hukum_value)
                self._send_response(response_data)

            except json.JSONDecodeError:
                # Handle invalid JSON
                response_data = {"error": "Invalid JSON format"}
                self._send_response(response_data, status=400)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    # Handle OPTIONS requests for CORS preflight
    def do_OPTIONS(self):
        self.send_response(204)  # No content
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow all origins
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')  # Allow specific methods
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')  # Allow specific headers
        self.end_headers()

# Define the server address and port
server_address = ('', 8080)

# Create and run the HTTP server
httpd = HTTPServer(server_address, RequestHandler)
print("Server running on port 8080...")
httpd.serve_forever()
