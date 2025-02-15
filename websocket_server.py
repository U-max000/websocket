import os
import asyncio
import websockets

PORT = int(os.environ.get("PORT", 8080))  # Get PORT from environment

async def handle_client(websocket, path):
    print("🔌 Client connected")
    try:
        async for message in websocket:
            print(f"📩 Received: {message}")
            await websocket.send(f"Echo: {message}")  # Echo back the message
    except websockets.exceptions.ConnectionClosed:
        print("⚠️ Client disconnected")

async def start_server():
    async def reject_http_requests(websocket, path):
        if "Upgrade" not in websocket.request_headers:
            print("🚫 Received an HTTP request, rejecting...")
            await websocket.close()
            return
        await handle_client(websocket, path)

    server = await websockets.serve(reject_http_requests, "0.0.0.0", PORT)
    print(f"✅ WebSocket Server Running on ws://0.0.0.0:{PORT}")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(start_server())
