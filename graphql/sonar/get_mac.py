from pydantic import BaseModel
from pydantic_extra_types.mac_address import MacAddress
from ..graphql_client import GraphQlClient

class PDUMACModel(BaseModel):
    pdu_mac: MacAddress


async def get_pdu_mac(asset: str) -> PDUMACModel:
    sonar_client = GraphQlClient("sonar")
    get_mac_query = ("""
    query GetMAC($asset_number: String!){
        inventory_items(general_search_mode: ROOT_PLUS_RELATIONS, general_search: $asset_number){
            entities{
                inventory_model_field_data{
                    entities{
                        value
                    }
                }
            }
        }
    }
    """)

    get_mac_query_variables = {
        "asset_number": asset
    }
    execute_get_mac_query = await sonar_client.execute_query(get_mac_query, get_mac_query_variables)
    try:
        for result in execute_get_mac_query.get('inventory_items').get('entities'):
            if (result.get('inventory_model_field_data').get('entities')[0].get('value')) == asset:
                pdu_mac_address = ((result.get('inventory_model_field_data').get('entities')[2].get('value')))
                return PDUMACModel(pdu_mac=pdu_mac_address)
    except Exception as e:
        print(e)
