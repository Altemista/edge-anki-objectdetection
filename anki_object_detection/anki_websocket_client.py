from ws4py.client.threadedclient import WebSocketClient

class AnkiWebSocketClient(WebSocketClient):
    def received_message(self, m):
        pass