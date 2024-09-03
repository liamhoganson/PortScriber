from .base_pdu import BasePDUClient

class PacketFluxClient(BasePDUClient):
    def __init__(self, ip: str):
        self.ip = ip
        super().__init__(self.ip, endpoint="/rw/doaction.cgi")

    async def update_pdu(self, outlets: dict):
        for outlet_number, outlet_description in outlets.items():
            data = {
                f"SETDL": f"{int(outlet_number)-1},{outlet_description}"
            }
            return await self.send_request(payload_data=data)
