from pydantic import BaseModel, HttpUrl, ValidationError, IPvAnyAddress
from typing import Dict
import httpx
import json
from ..config import EnvConfig

class BaseHTTPClientModel(BaseModel):
    ip: IPvAnyAddress
    endpoint: str
    url: HttpUrl
    http_headers: Dict[str, str]


class PDUHTTPClient:
    '''
    Base class responsible for creating an async HTTP client to send POST requests to PDUs.

    Attributes:
    - ip: The ip address of the PDU.
    - endpoint: The specific endpoint on the PDU to interact with.
    - username: Username for PDU authentication, loaded from environment variables.
    - password: Password for PDU authentication, loaded from environment variables.
    - url: The constructed URL with embedded credentials.
    - headers: HTTP headers used in the request.
    '''
    def __init__(self, ip: IPvAnyAddress, endpoint: str):
        self.username = EnvConfig().get_config("SSH/PDU", "USERNAME")
        self.password = EnvConfig().get_config("SSH/PDU", "GENERAL_PASSWORD")
        self.ip = ip
        self.endpoint = endpoint
        self.url: str = f"http://{self.username}:{self.password}@{self.ip}{self.endpoint}"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": str(self.ip),
            "Origin": f"http://{str(self.ip)}",
            "Referer": f"http://{str(self.ip)}/{self.endpoint}",
            "Upgrade-Insecure-Requests": "1"
        }
        try:
            self.client_data = json.loads(BaseHTTPClientModel(ip=self.ip, endpoint=self.endpoint, url=self.url, http_headers=self.headers).model_dump_json())
        except ValidationError as e:
            print(f"Could not validate HTTP input data: {e}")

    async def send_request(self, payload_data: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.client_data.get("url"), headers=self.client_data.get("http_headers"), data=payload_data)
                if response.status_code == 200:
                    return "Successfully updated PDU"
                else:
                    return "Something went wrong"
        except Exception as e:
            print(f"An error has occurred: {e}")
