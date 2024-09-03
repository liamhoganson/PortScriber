class Arp:

    def __init__(self, conn):
        self.conn = conn

    async def execute(self):
        command = "show iparp"
        await self.conn.channel.get_prompt()
        return self.conn.send_command(command)