import websockets
import asyncio
import json
import os

connected = []

async def handler(websocket):
    async for message in websocket:
        message = json.loads(message)
        print(message["type"])
        if message["type"] == "message":
            print(message["text"])
            f = open("messages.txt", "r")
            log = f.read()
            f.close()
            f = open("messages.txt", "w")
            f.write(log + message["text"] + "<br>")
            f.close()
            event = {"type": "message", "text": message["text"] + "<br>"}
            websockets.broadcast(iter(connected), json.dumps(event))
        elif message["type"] == "fetch":
            connected.append(websocket)
            f = open("messages.txt", "r")
            log = f.read()
            f.close()
            event = {"type": "message", "text": log}
            await websocket.send(json.dumps(event))


async def main():
    async with websockets.serve(handler,host="192.168.86.157", port=8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
