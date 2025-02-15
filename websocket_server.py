import os
import asyncio
import websockets
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

PORT = int(os.environ.get("PORT", 8080))  # Render assigns a port

# 🚀 WebSocket Handler
async def handle_client(websocket, path):
    print("🔌 WebSocket Client Connected")
    try:
        async for message in websocket:
            print(f"📩 Received: {message}")
            await websocket.send(f"Echo: {message}")  # Echo the message back
    except websockets.exceptions.ConnectionClosed:
        print("⚠️ WebSocket Client Disconnected")

async def start_websocket_server():
    print(f"✅ WebSocket Server Running on ws://0.0.0.0:{PORT}")
    async with websockets.serve(handle_client, "0.0.0.0", PORT):
        await asyncio.Future()  # Keep running

# 🌐 HTTP Server for Health Checks (on a different port)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")  # Response for Render health checks

def start_http_server():
    HTTP_PORT = 8081  # Different port for HTTP
    server = HTTPServer(("0.0.0.0", HTTP_PORT), HealthCheckHandler)
    print(f"🌍 HTTP Health Check Server Running on http://0.0.0.0:{HTTP_PORT}")
    server.serve_forever()

# 🏃 Run Both Servers
if __name__ == "__main__":
    # Run HTTP health check server in a separate thread
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()

    # Run WebSocket server
    asyncio.run(start_websocket_server())
