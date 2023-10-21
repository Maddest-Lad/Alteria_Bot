from aiomcrcon import Client
from utils import log

class minecraft_rcon:

    host: str
    port: str
    password: str
    client: Client

    async def __init__(self, host="0.0.0.0", port="25575", password="password"):
        self.client = Client(host, port, password)

    # Open Connection, Send Command, Close Connection
    async def send_command(self, command):
        try:
            log(f"Minecraft: Sending RCON Command: {command}")
            await self.client.connect()
            response = await self.client.send_cmd(command)
            log(f"Minecraft: Command Response: {response}")
        except Exception as e:
            log(str(e))
        finally:
            await self.client.close()

