# -*- coding: utf-8 -*-

import asyncio
from websockets import connect, serve


async def server_task(websocket, _):
    message = await websocket.recv()
    response = message
    await websocket.send(response)


def run_websocket_server(address='localhost', port=8087):
    start_server = serve(server_task, address, port)
    asyncio.get_event_loop().run_until_complete(start_server)


class WebSocketClient:
    def __init__(self, address):
        self._address = address
        self._connection = None
        self.websocket = None

    async def __aenter__(self):
        self._connection = connect(self._address)
        self.websocket = await self._connection.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._connection.__aexit__(*args, **kwargs)

    async def send(self, message):
        await self.websocket.send(message)

    async def receive(self):
        response = await self.websocket.recv()
        return response


async def send(message, address):
    async with WebSocketClient(address) as connection:
        await connection.send(message)
        result = await connection.receive()
        return result
