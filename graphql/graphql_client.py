from typing import Literal
from gql import gql, Client
from gql.transport.exceptions import TransportError, TransportQueryError
from gql.transport.aiohttp import AIOHTTPTransport
from ..config import EnvConfig

class GraphQlClient:
    def __init__(self, platform: Literal["netbox", "sonar"]):
        self.platform = platform
        match self.platform:
            case "netbox":
                self.api_url = EnvConfig().get_config("Netbox", "NETBOX_API_URL")
                self.api_token = EnvConfig().get_config("Netbox", "NETBOX_API_TOKEN")
                self.gql_headers = {"Authorization": f"Token {self.api_token}"}
            case "sonar":
                self.api_url = EnvConfig().get_config("Sonar", "SONAR_API_URL")
                self.api_token = EnvConfig().get_config("Sonar", "SONAR_API_TOKEN")
                self.gql_headers = {"Authorization": f"Bearer {self.api_token}"}
        self.gql_transport = AIOHTTPTransport(url=self.api_url, headers=self.gql_headers)

    async def execute_query(self, query: str, query_vars: dict):
        client = Client(transport=self.gql_transport)
        try:
            return await client.execute_async(gql(query), query_vars)
        except TransportError or TransportQueryError:
            raise f"Could not connect to {self.api_url} or malformed gql query"
