import websockets
import asyncio
import json
import os

connected = []

os.system("python -m http.server")

async def handler(websocket):
    for message in websocket:
        event = json.loads(message)
        if event["type"] == "message":
            f = open("messages.txt", "w")
            f.write(message["text"] + "<br>")
            f.close()
            event = {"type": "message", "text": message["text"] + "<br>"}
            websockets.broadcast(iter(connected))
        elif event["type"] == "fetch":
            connected.append(websocket)
            f = open("messages.txt", "r")
            log = f.read()
            f.close()
            event = {"type": "message", "text": log}
            await websocket.send(json.dumps(log))


async def main():
    async with websockets.serve(handler,host="10.82.16.170", port=8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
