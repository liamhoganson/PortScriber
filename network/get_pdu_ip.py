from pydantic import BaseModel, IPvAnyAddress

class PDUIPAddressModel(BaseModel):
    pdu_ip: IPvAnyAddress

class PDUIP:
    def __init__(self, ssh_client: object, network_device_mac: str, network_arp: object):
        self.ssh_client = ssh_client
        self.network_device_mac = network_device_mac
        self.network_arp = network_arp

    async def get_ip(self) -> str:
        try:
            arp_list = await self.network_arp(self.ssh_client).execute()
            for entry in (arp_list.textfsm_parse_output()):
                if str((entry.get("mac_address"))) == self.network_device_mac:
                    get_pdu_ip = entry.get("ip_address")
                    return PDUIPAddressModel(pdu_ip=get_pdu_ip).model_dump_json()
        except Exception as e:
            raise RuntimeError(f"An error has occured: {e}")
        return await self.ssh_client.close()
