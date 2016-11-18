# -*- coding: utf-8 -*-

import asyncio
import websockets
from websockets import connect

async def server_task(websocket, path): #pylint: disable=unused-argument
    message = await websocket.recv()
    response = message
    await websocket.send(response)

def run_websocket_server(address='localhost', port=8087):
    start_server = websockets.serve(server_task, address, port)
    asyncio.get_event_loop().run_until_complete(start_server)


class EchoWebsocket:
    def __init__(self, address):
        self._address = address

    async def __aenter__(self):
        self._conn = connect(self._address) #pylint: disable=attribute-defined-outside-init
        self.websocket = await self._conn.__aenter__() #pylint: disable=attribute-defined-outside-init
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    async def send(self, message):
        await self.websocket.send(message)

    async def receive(self):
        response = await self.websocket.recv()
        return response


async def main(message, address):
    async with EchoWebsocket(address) as echo:
        await echo.send(message)
        result = await echo.receive()
        return result


def send_get_echo_message(message, address='ws://localhost:8087'):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main(message, address))
    return result
