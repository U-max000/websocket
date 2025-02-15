import asyncio
import websockets

connected_clients = set()

async def handle_client(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"📩 Received: {message}")
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)  # Broadcast Morse code to all clients
    except websockets.exceptions.ConnectionClosed:
        print("❌ A client disconnected.")
    finally:
        connected_clients.remove(websocket)

async def start_server():
    server = await websockets.serve(handle_client, "0.0.0.0", 8080)
    print("✅ WebSocket Server Running on ws://0.0.0.0:8080")
    await server.wait_closed()

# Fix for Python 3.13: Explicitly create and run the event loop
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_server())
    loop.run_forever()
