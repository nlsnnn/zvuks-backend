from fastapi import WebSocket, WebSocketDisconnect


class WebSocketManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def add_connection(self, user_id: int, websocket: WebSocket):
        self.active_connections[user_id] = websocket
    
    async def remove_connection(self, user_id: int):
        self.active_connections.pop(user_id, None)

    async def notify_user(self, user_id: int, message: dict):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                await websocket.send_json(message)
            except (WebSocketDisconnect, RuntimeError, ValueError):
                await self.remove_connection(user_id)


websocket_manager = WebSocketManager()

def get_websocket_manager():
    return websocket_manager