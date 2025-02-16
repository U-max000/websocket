import os
import asyncio
import websockets
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from websockets.exceptions import InvalidMessage

PORT = int(os.environ.get("PORT", 8080))  # WebSocket port
HTTP_PORT = 8081  # Separate HTTP port for health checks

# 🚀 WebSocket Handler
async def handle_client(websocket, path):
    print("🔌 WebSocket Client Connected")
    try:
        async for message in websocket:
            print(f"📩 Received: {message}")
            await websocket.send(f"Echo: {message}")  # Echo message back
    except websockets.exceptions.ConnectionClosed:
        print("⚠️ WebSocket Client Disconnected")

# 🌍 HTTP Server for Health Checks
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":  # Only respond to /health checks
            print(f"✅ Health check request from {self.client_address}")
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        print(f"Received GET request from {self.client_address}")  # Log GET requests
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

def start_http_server():
    server = HTTPServer(("0.0.0.0", HTTP_PORT), HealthCheckHandler)
    print(f"🌍 HTTP Health Check Server Running on http://0.0.0.0:{HTTP_PORT}")
    server.serve_forever()

# ✅ WebSocket Server with Error Handling
async def start_websocket_server():
    print(f"✅ WebSocket Server Running on ws://0.0.0.0:{PORT}")

    async def custom_handler(websocket, path):
        """ Ensure only GET requests for WebSocket upgrade are processed """
        if websocket.request_headers.get("Upgrade", "").lower() != "websocket":
            print("❌ Non-WebSocket request received, ignoring.")
            return  # Ignore non-WebSocket requests

        await handle_client(websocket, path)

    try:
        async with websockets.serve(custom_handler, "0.0.0.0", PORT):
            await asyncio.Future()  # Keep running
    except InvalidMessage as e:
        print(f"⚠️ Ignoring invalid request: {e}")

if __name__ == "__main__":
    # Start HTTP health check server in separate thread
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()

    # Run WebSocket server
    asyncio.run(start_websocket_server())
