import websockets
import asyncio
import json
import sqlite3

#os.chdir(os.getcwd())
#os.system("python -m http.server")

connected = []
sql = sqlite3.connect("messages.sqlite3")
cur = sql.cursor()
print(cur.fetchall())

async def handler(websocket):
    async for message in websocket:
        message = json.loads(message)
        print(message)
        if message["type"] == "message":
            print(message["text"])
            """
            f = open("messages.txt", "r")
            log = f.read()
            f.close()
            f = open("messages.txt", "w")
            f.write(log + message["user"] + ": " + message["text"] + chr(7))
            f.close()
            """
            event = {"type": "message", "text": message["text"], "user": message["user"]}
            sql.execute("INSERT INTO Messages(Message, User) VALUES ('{}', '{}')".format(message["text"], message["user"]))
            for i in connected:
                try:
                    await i.send(json.dumps(event))
                except websockets.exceptions.ConnectionClosed:
                    connected.pop(connected.index(i))
            print(connected)
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
