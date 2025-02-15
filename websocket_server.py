import os
import asyncio
import websockets

# Get port from environment variable or use 8080 as default
PORT = int(os.environ.get("PORT", 8080))

# Handle incoming client connections
async def handle_client(websocket, path):
    print("🔌 Client connected")
    try:
        async for message in websocket:
            print(f"📩 Received: {message}")
            await websocket.send(f"Echo: {message}")  # Echo back the message
    except websockets.exceptions.ConnectionClosed:
        print("⚠️ Client disconnected")

# Start WebSocket server
async def start_server():
    server = await websockets.serve(handle_client, "0.0.0.0", PORT)
    print(f"✅ WebSocket Server Running on ws://0.0.0.0:{PORT}")
    await server.wait_closed()

# Run the WebSocket server
if __name__ == "__main__":
    asyncio.run(start_server())
