from abc import ABC, abstractmethod
from .base_http_client import PDUHTTPClient

class BasePDUClient(ABC, PDUHTTPClient):
    '''
    Base class that sub PDU classes inherit from and implement the update_pdu method given the attributes.
    Attributes:
    - IP: IP address of PDU
    - outlets: PDU Outlet Number to Outlet description mapping
    '''
    def __init__(self, ip: str, endpoint: str):
        super().__init__(ip, endpoint)

    @abstractmethod
    def update_pdu(self, outlets: dict):
        pass
