import os
import asyncio
import websockets
from websockets.exceptions import InvalidMessage

PORT = int(os.environ.get("PORT", 8080))  # Use Render-assigned port

# 🚀 WebSocket Handler
async def handle_client(websocket, path):
    print("🔌 WebSocket Client Connected")
    try:
        async for message in websocket:
            print(f"📩 Received: {message}")
            await websocket.send(f"Echo: {message}")  # Echo the message back
    except websockets.exceptions.ConnectionClosed:
        print("⚠️ WebSocket Client Disconnected")

# 🌍 WebSocket Server with Error Handling
async def start_websocket_server():
    print(f"✅ WebSocket Server Running on ws://0.0.0.0:{PORT}")
    async with websockets.serve(handle_client, "0.0.0.0", PORT):
        await asyncio.Future()  # Keep running

if __name__ == "__main__":
    try:
        asyncio.run(start_websocket_server())
    except InvalidMessage:
        print("⚠️ Ignoring invalid HTTP request (likely a health check)")
