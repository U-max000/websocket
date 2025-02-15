import asyncio
import websockets

connected_clients = set()

async def handle_client(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received: {message}")
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)  # Broadcast message
    finally:
        connected_clients.remove(websocket)

async def websocket_handler(websocket, path):
    """ Handles WebSocket connections, rejecting non-WebSocket requests. """
    if path != "/":
        await websocket.close()
        return
    
    await handle_client(websocket, path)

async def start_server():
    server = await websockets.serve(websocket_handler, "0.0.0.0", 8080)
    print("✅ WebSocket Server Running on ws://0.0.0.0:8080")
    await server.wait_closed()

asyncio.run(start_server())
