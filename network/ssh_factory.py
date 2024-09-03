class SSHClient:
    def __init__(self, host: str, password: str, platform: object):
        self.host = host
        self.password = password
        self.platform = platform

    async def connect(self):
        connection_params = {
            "host": self.host,
            "auth_username": "admin",
            "auth_password": self.password,
            "auth_strict_key": False,
            "transport": "asyncssh"
        }
        try:
            conn = self.platform(**connection_params)
            await conn.open()
            return conn
        except ConnectionError as e:
            raise f"Could not connect to: {self.host}: {e}"
        except Exception as e:
            raise RuntimeError(f"Unknown error: {e}")

    async def close_connection(self):
        return await self.conn.close()
