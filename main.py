import websockets
import asyncio
import json
import os

#os.chdir(os.getcwd())
#os.system("python -m http.server")

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
            f.write(log + message["user"] + ": " + message["text"] + chr(7))
            f.close()
            event = {"type": "message", "text": message["user"] + ": " + message["text"]}
            websockets.broadcast(iter(connected), json.dumps(event))
        elif message["type"] == "fetch":
            connected.append(websocket)
            f = open("messages.txt", "r")
            log = f.read()
            f.close()
            log = log.split(chr(7))
            for i in range(len(log) - 1):
                event = {"type": "message", "text": log[i]}
                await websocket.send(json.dumps(event))


async def main():
    async with websockets.serve(handler,host="localhost", port=8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
