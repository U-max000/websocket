import asyncio
import websockets

async def handle_client(websocket, path):
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosedError:
        print("Client disconnected")
    except Exception as e:
        print(f"Unexpected error: {e}")

# 🔴 Reject HTTP requests (Render health checks, browsers, etc.)
async def process_request(path, request_headers):
    if "Upgrade" not in request_headers or request_headers["Upgrade"].lower() != "websocket":
        return (426, [], b"WebSocket connection required\n")

async def start_server():
    server = await websockets.serve(
        handle_client, "0.0.0.0", 8080, process_request=process_request
    )
    print("✅ WebSocket Server Running on ws://0.0.0.0:8080")
    await server.wait_closed()

asyncio.run(start_server())
