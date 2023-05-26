class ServerNotReady(Exception):
    def __init__(self, health):
        self.health = health
        self.message = f"Server not ready. Network synchronization at: {health.network_sync_at}"
        super().__init__(self.message)
        
        
class RequestError(Exception):
    def __init__(self, response):
        self.response = response
        self.message = f"Request error: {response.status}"
        super().__init__(self.message)