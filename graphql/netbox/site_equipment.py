from pydantic import BaseModel, IPvAnyAddress, field_validator
import json
import ipaddress
from ..graphql_client import GraphQlClient

class DeviceDataModel(BaseModel):
    name: str
    device_type: str
    ip: IPvAnyAddress
    device_role: str

    @field_validator('ip', mode="before")
    def custom_validator(cls, v: str) -> str:
        try:
            network = ipaddress.ip_network(v, strict=False)
            return IPvAnyAddress(network.network_address)
        except ValueError as e:
            raise ValueError(f"Invalid IP address or CIDR notation: {e}")


async def get_site_equipment(site_slug: str) -> list:
    netbox_client = GraphQlClient(platform="netbox")
    query = """
    query getSiteSwitchAndRouter($slug: [String!]) {
        device_list(filters: {site: $slug, role_id: ["1", "6"]}) {
            name
            device_type {
                manufacturer {
                    display
                }
            }
            role{
                name
            }
            primary_ip4 {
                display
            }
        }
    }
    """

    query_vars = {
        "slug": site_slug
    }

    try:
        site_equipment = []
        device_dict = {}
        execute_get_site_equipment_query = await netbox_client.execute_query(query=query, query_vars=query_vars)
        for result in execute_get_site_equipment_query.get('device_list'):
            device_dict.update({"name": result.get('name'), "device_type": result.get('device_type').get('manufacturer').get('display'), "ip": result.get("primary_ip4").get('display'), "device_role": result.get("role").get("name")})
            site_equipment.append(json.loads(DeviceDataModel(**device_dict).json()))
        return site_equipment
    except Exception as e:
        raise RuntimeError(f"Error: Could not get devices from Netbox: {e}")
