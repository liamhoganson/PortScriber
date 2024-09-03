class ShowDesc:

    def __init__(self, conn: object, interface_number: int):
        self.conn = conn
        self.interface_number = interface_number

    async def execute(self):
        if int(self.interface_number) <= 23:
            interface = "GigabitEthernet0/0/0/"
        elif int(self.interface_number) > 23:
            interface = "TenGigE0/0/0/"
        command = f"show interface {interface}{self.interface_number}"
        return await self.conn.send_command(command)
