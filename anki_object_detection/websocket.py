from autobahn.asyncio.websocket import WebSocketClientProtocol, WebSocketClientFactory
import os
import asyncio


class WebsocketClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    def send(self, message):
        self.sendMessage(message.encode('utf8'))


class Websocket:

    def __init__(self, loop):
        self.httpWebsocket = os.environ.get('HTTP_WEBSOCKET')

        if self.httpWebsocket is None:
            print('Using 127.0.0.1 as default websocket server.')
            self.httpWebsocket='127.0.0.1'

        factory = WebSocketClientFactory(u"ws://" + self.httpWebsocket + ":8003/status")
        factory.protocol = WebsocketClientProtocol

        self.coroutine = loop.create_connection(factory, self.httpWebsocket, 8003)