import asyncio
import websockets
import json
from result import GameResult

class ConnectionManager():
    def __init__(self, app, port=3000):
        self._port = port
        self._app = app
        self._server_stop_event = asyncio.Event()

    async def run(self):
        while self._app.isAppRunning:
            print(self._app.isAppRunning)
            if self._app.cm_createLobby:
                self._app.cm_createLobby = False
                self._server_stop_event.clear()
                await self.createLobby()
            elif self._app.cm_joinLobby:
                self._app.cm_joinLobby = False
                self._server_stop_event.clear()
                await self.runGameAsClient()
            await asyncio.sleep(0.1)  

    async def runGameAsClient(self):
        uri = f"ws://{self._app.host_ip}"
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps({"userId": self._app.userId,
                                             "message": "start game",
                                            "duration" : 10}))
            response = json.loads(await websocket.recv())
            if response["message"] == "go":
                score, _  = await self._app.game(response["duration"])
                await websocket.send(json.dumps({"userId": self._app.userId,
                                            "message": "end game",
                                            "duration" : 10,
                                            "score": score}))
                response = json.loads(await websocket.recv())
                if response["message"] == "draw":
                    score, duration = await self._app.game()
                    await websocket.send(json.dumps({"userId": self._app.userId,
                                            "message": "fatality",
                                            "duration" : duration,
                                            "score": score}))
                    response = json.loads(await websocket.recv())
                    if duration > response["duration"]: 
                        GameResult((True, "You win")) 
                        self._app.gm_result.append((True, "You win"))
                        self._app.db_manager.addGame(self.app.userId, response["userId"])
                    else: 
                        GameResult((False, "You lose"))
                        self._app.gm_result.append((False, "You lose"))
                        self._app.db_manager.addGame(response["userId"], self.app.userId)
                        
                else:
                    if score > response["score"]:
                        self._app.gm_result.append((True, "You win"))
                        GameResult((True, "You win")) 
                        self._app.db_manager.addGame(self.app.userId, response["userId"])
                    else: 
                        GameResult((False, "You lose"))
                        self._app.gm_result.append((False, "You lose"))
                        self._app.db_manager.addGame(response["userId"], self.app.userId)
                
                self._app._server_stop_event.set()

    async def createLobby(self):
        async with websockets.serve(self.handle_client, "0.0.0.0", self._port):
            await self._server_stop_event.wait()

    async def handle_client(self, websocket):
        async for message in websocket:
            data = json.loads(message)
            if data["message"] == "start game":
                self._app.gm_startGame = True
                await websocket.send(json.dumps({"userId": self.userId,
                                                 "message": "go", 
                                                 "duration" : self._app.gm_duration}))
            elif data["message"] == "end game":
                print("Enemy score "+str(data["score"]))
                while self._app.gm_isRunning: 
                    await asyncio.sleep(0.1)
                if self._app.gm_myScore == data["score"]:
                    self._app.gm_duration = 0
                    self._app.gm_startGame = True
                    await websocket.send(json.dumps({"userId": self.userId,
                                                     "message": "draw", 
                                                     "score": self._app.gm_myScore}))
                else:
                    print("You win" if self._app.gm_myScore > data["score"] else "You lose")
                    self._app.gm_ended = True
                    await websocket.send(json.dumps({"userId": self.userId,
                                                     "message": "not draw", 
                                                     "score": self._app.gm_myScore}))
                    self._server_stop_event.set()
                
            elif data["message"] == "fatality":
                while self._app.gm_isRunning: 
                    await asyncio.sleep(0.1)
                print("You win" if self._app.gm_duration >= data["duration"] else "You lose")
                self._app.gm_ended = True
                await websocket.send(json.dumps({"duration": self._app.gm_duration}))
                self._server_stop_event.set()
