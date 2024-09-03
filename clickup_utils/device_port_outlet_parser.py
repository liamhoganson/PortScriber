from typing import List
from .abstract_device_list import BasePortOrOutletParser

class DeviceOutletOrPortList(BasePortOrOutletParser):
     """
    Extracts and parses device ports or outlet numbers from pdu_data object based on positional.
    Attributes
    - device: Network device (Router, sw-1, sw-2)
    - pdu_data: instantiated Clickup Payload object
    - ports_or_outlets: Literal that splits logic
     """
     async def get_list(self) -> List[str]:
        posistional: str = None
        posistional = 1 if self.port_or_outlet == "ports" else posistional == 0
        try:
            device_ports_list = self.pdu_data.get("ports_data").get(self.device)
            if not device_ports_list:
                raise ValueError(f"No ports data found for device: {self.device}")
            device_data_list:List[str] = [port.split(":")[posistional] for port in device_ports_list]
            return device_data_list
        except Exception as e:
            raise RuntimeError(f"Could not parse port list data: {e}")
