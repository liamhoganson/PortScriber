from abc import ABC, abstractmethod
from typing import List, Literal

class BasePortOrOutletParser(ABC):
    '''
    Base class responsible for parsing output returned from Clickup payload and allows for easy interfacing to get either network device port numbers or PDU outlet numbers.
    Attributes
    - device: Network device (Router, sw-1, sw-2)
    - pdu_data: instantiated Clickup Payload object
    - ports_or_outlets: Literal that splits logic
    '''
    def __init__(self, device: str, pdu_data: dict, port_or_outlet = Literal["ports", "outlet"]):
        self.device = device
        self.pdu_data = pdu_data
        self.port_or_outlet = port_or_outlet

    @abstractmethod
    async def get_list(self) -> List[str]:
        pass
