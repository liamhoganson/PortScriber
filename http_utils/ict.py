from .base_pdu import BasePDUClient

class ICTClient(BasePDUClient):
    def __init__(self, ip: str):
        self.ip = ip
        super().__init__(self.ip, endpoint="/output/")

    async def update_pdu(self, outlets: dict):
        for outlet_number, outlet_description in outlets.items():
            if int(outlet_number) < 10:
                data = {
                    str(f"n0{int(outlet_number)-1}"): f"{outlet_description}"
                }
            else:
                data = {
                    str(f"n{int(outlet_number)-1}"): f"{outlet_description}"
                }
            return await self.send_request(payload_data=data)
