import socket
import json
from functools import wraps
from typing import Dict, Union, Any, Callable
import xmltodict
from scrapli_netconf.driver import AsyncNetconfDriver
from pydantic import BaseModel, ValidationError, field_validator
from pydantic.networks import IPvAnyAddress
from typing import Dict, Union, Any, Callable

# TODO: Handle errors better


# Netconf Connection parameters data model
class NetConfConnectionParamsModel(BaseModel):
    host: IPvAnyAddress
    auth_username: str
    auth_password: str
    auth_strict_key: bool = False
    transport: str = "asyncssh"

    @field_validator("host", mode="before")
    @classmethod
    def dns_to_ip_address(cls, hostname: str) -> IPvAnyAddress:
        if isinstance(hostname, str):
            try:
                ip_address = socket.gethostbyname(hostname)
                return IPvAnyAddress(ip_address)
            except socket.gaierror:
                raise ValueError(f"Could not resolve hostname: {hostname}")
        return IPvAnyAddress(hostname)


class NetConfConnection(object):
    """
    Netconf connection async context manager
    """

    def __init__(self, conn_params: NetConfConnectionParamsModel):
        self.conn_params = conn_params

    async def __aenter__(self) -> AsyncNetconfDriver:
        self.conn = AsyncNetconfDriver(**self.conn_params)
        try:
            await self.conn.open()
            return self.conn
        except Exception as e:
            raise ConnectionError(f"Failed to connect to device! {e}")

    async def __aexit__(self, type, value, traceback):
        """This will close connections and handle any errors that occur within the 'with' block."""
        await self.conn.close()


# Wrapper function for executing netconf state data queries
def netconf_query(xml_filter: str) -> Callable:
    """
    Wrapper method in order to reduce code duplication across the Netconf query methods.

    Args:
        xml_filter: XML formatted netconf filter (this should correspond with the method its being called on)

    Raises:
        N/A
    """

    def decorator(
        func: Callable,
    ) -> Callable:  # Decorator function that takes in NetConfClient instance query method as a 'callback'.
        @wraps(func)
        async def wrapper(self, *args: Any, **kwargs: Any) -> Callable:
            """
            Wrapper method that wraps any NetConfClient query methods. Handles netconf request, general error handling, and parsing that's universal to any NetConfClient query.
            """
            try:
                async with NetConfConnection(self.conn_params) as conn:
                    state_data = await conn.get(filter_=xml_filter.format(args[0]))
                    if (
                        "<data/>" in state_data.result
                    ):  # This indicates the RPC reply is null of any state data.
                        raise ValueError(
                            f"Could not find any state data from device: {self.conn_params['host']}!"
                        )
                    rpc_reply: Dict[str, ...] = xmltodict.parse(state_data.result)
                    return func(self, rpc_reply, *args, **kwargs)
            except Exception as e:
                raise RuntimeError(f"Could not fetch state data from device! {e}")

        return wrapper

    return decorator


# Main class
class NetConfClient(object):
    model = NetConfConnectionParamsModel

    def __init__(self, host: Union[str, IPvAnyAddress], username: str, password: str):
        """
        Initialize the NetConfClient object with the connection parameters.
        """
        self.host = host
        self.username = username
        self.password = password
        try:
            self.conn_params: Dict = json.loads(
                self.model(
                    host=self.host,
                    auth_username=self.username,
                    auth_password=self.password,
                    auth_strict_key=False,
                    transport="asyncssh",
                ).json()
            )
        except ValidationError as e:
            raise ValueError(f"Could not validate connection parameters! {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to load connection parameters! {e}")

    # Instance methods

    @netconf_query(
        xml_filter="""
        <filter>
          <interfaces xmlns="http://openconfig.net/yang/interfaces">
            <interface>
              <name>{}</name>
              <config>
                <description/>
              </config>
            </interface>
          </interfaces>
        </filter>
        """
    )
    def get_interface_desc(self, rpc_reply: Dict[str, ...], interface: str) -> str:
        """
        Retrieve interface description(s) async method.

        Args:
          interface: String representation of interface to query (For example, "GigabitEthernet00/0/5").

        Returns:
          Single interface description string object.
        """
        parsed_response: Union[str, None] = (
            rpc_reply.get("rpc-reply", {})
            .get("data", {})
            .get("interfaces", {})
            .get("interface", {})
            .get("config", {})
            .get("description", None)
        )
        if parsed_response is None:
            raise ValueError("No interface description configured")
        return parsed_response
