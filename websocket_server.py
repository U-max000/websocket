import asyncio
import websockets
from http.server import BaseHTTPRequestHandler, HTTPServer

# Handle HTTP requests (to prevent HEAD error)
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"WebSocket Server Running")

# Start WebSocket Server
async def handle_client(websocket, path):
    try:
        async for message in websocket:
            print(f"📩 Received: {message}")
            await websocket.send(f"Echo: {message}")  # Echo back the message
    except websockets.exceptions.ConnectionClosed:
        print("⚠️ Client Disconnected")

async def start_websocket():
    server = await websockets.serve(handle_client, "0.0.0.0", 8080)
    print("✅ WebSocket Server Running on ws://0.0.0.0:8080")
    await server.wait_closed()

# Start HTTP server to handle health checks
def start_http_server():
    httpd = HTTPServer(('0.0.0.0', 8080), SimpleHTTPRequestHandler)
    httpd.serve_forever()

# Run both WebSocket and HTTP servers
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_websocket())
    loop.run_in_executor(None, start_http_server)
    loop.run_forever()
