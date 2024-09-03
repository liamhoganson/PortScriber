class Arp:

    def __init__(self, conn):
        self.conn = conn

    def execute(self):
        command = "show arp"
        return self.conn.send_command(command)
