import os
import asyncio
import websockets
from http import HTTPStatus
from websockets.exceptions import InvalidMessage

PORT = int(os.environ.get("PORT", 8080))  # WebSocket port

# This function intercepts HTTP requests before the WebSocket handshake.
async def process_request(path, request_headers):
    if path == "/health":
        print("✅ Health check request received")
        # Return a 200 OK response with a simple body.
        return HTTPStatus.OK, [("Content-Type", "text/plain")], b"OK"
    # For all other paths, return None to continue with the normal WebSocket handshake.
    return None

# 🚀 WebSocket Handler
async def handle_client(websocket, path):
    print("🔌 WebSocket Client Connected")
    try:
        async for message in websocket:
            print(f"📩 Received: {message}")
            await websocket.send(f"Echo: {message}")  # Echo message back
    except websockets.exceptions.ConnectionClosed:
        print("⚠️ WebSocket Client Disconnected")

async def start_websocket_server():
    print(f"✅ WebSocket Server Running on ws://0.0.0.0:{PORT}")
    try:
        async with websockets.serve(
            handle_client, "0.0.0.0", PORT, process_request=process_request
        ):
            await asyncio.Future()  # Run forever.
    except InvalidMessage as e:
        print(f"⚠️ Ignoring invalid request: {e}")

if __name__ == "__main__":
    asyncio.run(start_websocket_server())
