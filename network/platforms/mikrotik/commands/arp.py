class Arp:

    def __init__(self, conn):
        self.conn = conn

    def execute(self):
        command = "/ip arp print"
        return self.conn.send_command(command)