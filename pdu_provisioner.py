from clickup_utils.clickup import PDUData
from sonar import get_mac
from netbox import site_equipment
from network.ssh_factory import SSHClient
from network.get_pdu_ip import PDUIP
from scrapli.driver.core import AsyncIOSXRDriver
from network.platforms.cisco_xr.commands.arp import Arp as CiscoArp
from network.platforms.cisco_xr.commands.show_desc import ShowDesc as CiscoShowDesc
from http_utils.synaccess import SynaccessClient
from http_utils.ict import ICTClient
from http_utils.packetflux import PacketFluxClient
from network.network_utils import cisco_mac_address_formatter
import asyncio
from dotenv import load_dotenv
import os
import json
import logging

# log = logging.getLogger(__name__)
# load_dotenv("env_vars.env")

# router_password = os.environ.get("ROUTER_PASSWORD")
# standard_password = os.environ.get("PDU_PASSWORD")

# #TODO: Ensure connections and queries are not being redundantly invoked
# #TODO: Refactor Graphql client to stay DRY across all queries and platforms
# #TODO: Construct an object that maps device input data from Clickup

# #pdu_asset_number = PDU_DATA.get("pdu_asset_number")


# async def get_site_devices():
#     '''
#     Retrieves routers and switches from the given Netbox site.
#     '''
#     devices = []
#     site_eq = await site_equipment.get_site_equipment("mid")
#     for device in site_eq:
#         devices.append(device)
#     return devices


# async def ssh_factory(device_type: str, device_ip: str, device_role: str) -> SSHClient:
#     '''
#     Creates SSH client object that connects to the router/switch devices.

#     Attributes (values returned from get_site_devices):
#     - device_type: The manufacturer of the device. Used to pick the right Scrapli driver
#     - device_ip: IP address of the device.
#     - device_role: Either Router or Switch
#     '''
#     match device_type:
#         case "Cisco":
#             driver = AsyncIOSXRDriver
#         case _:
#             log.error("Could not match device type to scrapli driver!")
#     if device_role == "Router":
#         ssh = SSHClient(device_ip, router_password, driver)
#     elif device_role == "Switch":
#         ssh = SSHClient(device_ip, standard_password, driver)
#     else:
#         log.error("Unexpected device role returned from Netbox!")
#         return await ssh.connect()



# async def fetch_pdu_ip(): #TODO: Break this out into smaller functions and clean this up.
#     '''
#     Fetches PDU's IP from site router by matching PDU's MAC address in router's ARP table
#     '''
#     mac_address = await get_mac.get_pdu_mac(pdu_asset_number)
#     mac_address = mac_address.model_dump()["pdu_mac"]
#     for device in await get_site_devices():
#         if device.get("device_role") == "Router":
#             if device.get("device_type") == "Cisco":
#                 mac_address = cisco_mac_address_formatter(mac_address)
#             ssh_client = await ssh_factory(
#                 device.get("device_type"), device.get("ip"), device.get("device_role")
#             )
#             pdu_ip = await PDUIP(ssh_client, mac_address, CiscoArp).get_ip()
#             if pdu_ip is not None:
#                 pdu_ip = json.loads(pdu_ip).get("pdu_ip")
#                 return pdu_ip
#             else:
#                 log.error("Could not retrive PDU's IP address from router!")
#             ssh_client.close()


# async def fetch_interface_descriptions(port_list: dict, device: dict) -> list:
#     '''
#     Retreives interface descriptions from network device and returns a list of them.

#     Attributes:
#     - port_list: Port list grabbed from Clickup Webhook
#     - device: Network device (router or switch) to grab interface descriptions from.
#     '''
#     descriptions = []
#     ssh_client = await ssh_factory(
#         device.get("device_type"), device.get("ip"), device.get("device_role")
#     )
#     if port_list is not None:
#         for interface in port_list:
#             get_int_desc = await CiscoShowDesc(ssh_client, interface).execute()
#             interfaces = get_int_desc.textfsm_parse_output()
#             if interfaces is not None or [] or '[]':
#                 for interface_desc in interfaces:
#                     descriptions.append(interface_desc["description"])
#             else:
#                 log.error(f"Could not retrieve interface descriptions from {device.get("ip")}")
#     ssh_client.close()
#     return descriptions


# async def http_client_factory():
#     '''
#     Creates http_client object to connect to remote PDU's.
#     '''
#     http_client = None
#     pdu_type: str = PDU_DATA.get("pdu_type")
#     match pdu_type:
#         case "Synaccess":
#             http_client = SynaccessClient()
#         case "Ict":
#             http_client = ICTClient()
#         case "packet flux":
#             http_client = PacketFluxClient()
#         case _:
#             log.error(f"Got unexpected PDU type: {pdu_type}!")
#     if http_client is not None:
#         return http_client


# async def update_pdu(pdu_ip, device_port_list: dict, interface_descriptions: list):
#     '''
#     Sends POST request to remote PDU device to update PDU outlets.

#     Attributes:
#     - pdu_ip: IP address of PDU
#     - device_port_list: Returned from Clickup payload; PDU to router ports.
#     - interface_descriptions: List of descriptions returned from fetch_interface_descriptions.
#     '''
#     pdu_client = await http_client_factory()
#     outlet_to_description_map = {
#         "outlet": device_port_list.get("pdu_outlets"),
#         "descriptions": interface_descriptions,
#     }
#     await pdu_client.update_pdu(pdu_ip, outlet_to_description_map)


# async def main():
#     pdu_data = PDUData().get_pdu_data()
#     for device in pdu_data.get("ports_data").keys():
#         print(device)
#         device_ports = PortListParser(device, pdu_data, ports_or_outlets="ports")
#         device_ports= (await(device_ports.get_each_device_port_list()))
#         print(device_ports)
#         device_ports = PortListParser(device, pdu_data, ports_or_outlets="outlets")
#         device_ports= (await(device_ports.get_each_device_port_list()))
#         print(device_ports)


# if __name__ == "__main__":
#     asyncio.run(main())
from typing import Dict, List
from clickup_utils.device_port_outlet_parser import DeviceOutletOrPortList

# async def process_device(device: str, pdu_data: dict, ports_or_outlets: str) -> Dict[str, List[str]]:
#     parser = PortListParser(device, pdu_data, ports_or_outlets=ports_or_outlets)
#     device_ports = await parser.get_each_device_port_list()
#     return {device: device_ports}

# async def process_all_devices(pdu_data: dict):
#     tasks = []
#     for device in pdu_data.get("ports_data").keys():
#         tasks.append(process_device(device, pdu_data, ports_or_outlets="ports"))
#         tasks.append(process_device(device, pdu_data, ports_or_outlets="outlets"))

#     # Run all tasks concurrently
#     results = await asyncio.gather(*tasks)
#     return results


async def main():
    # Defining constants
    pdu_data = PDUData().get_pdu_data()
    device_ports = await(DeviceOutletOrPortList("Switch1 Ports", pdu_data, "ports").get_list())
    device_outlets = await(DeviceOutletOrPortList(device="Switch1 Ports", pdu_data=pdu_data, port_or_outlet="outlets").get_list())
    print(device_ports)

if __name__ == "__main__":
    asyncio.run(main())
