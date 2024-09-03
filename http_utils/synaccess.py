from .base_pdu import BasePDUClient

class SynaccessClient(BasePDUClient):
    def __init__(self, ip: str):
        self.ip = ip
        super().__init__(self.ip, endpoint="/pwr.htm")

    async def update_pdu(self, outlets: dict):
        for outlet_number, outlet_description in zip(outlets.get("outlet"), outlets.get("descriptions")):
            data = {
                f"ON{int(outlet_number)-1}": f"{outlet_description}"
            }
            return await self.send_request(payload_data=data)
