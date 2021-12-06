import websockets
import asyncio
import json
import sqlite3

#os.chdir(os.getcwd())
#os.system("python -m http.server")

connected = []
db = sqlite3.connect("messages.db")
print(db.execute("SELECT * FROM Messages").fetchall())

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
            db.execute("INSERT INTO Messages (Message, User) VALUES ('{}', '{}');".format(message["text"], message["user"]))
            db.commit()
            for i in connected:
                try:
                    await i.send(json.dumps(event))
                except websockets.exceptions.ConnectionClosed:
                    connected.pop(connected.index(i))
            print(connected)
        elif message["type"] == "fetch":
            connected.append(websocket)
            log = db.execute("SELECT * FROM Messages").fetchall()
            for i in log:
                event = {"type": "message", "text": i[0], "user": i[1]}
                await websocket.send(json.dumps(event))


async def main():
    async with websockets.serve(handler,host="localhost", port=8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
