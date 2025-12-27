"""Wrapper for Cosmos DB I/O"""
import os
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient

class OlieCosmos:
    """Repository for Cosmos DB"""
    SATELLITE_AWS_PRODUCTS = "satelliteAwsProducts"

    def __init__(self):
        credential = DefaultAzureCredential()
        endpoint = os.environ['OlieCosmosEndpoint']
        database = os.environ['OlieCosmosDatabase']

        self.client = CosmosClient(url=endpoint, credential=credential)
        self.database = self.client.get_database_client(database)

    def satellite_aws_product_read(self, item: str, eff_dt: str) -> any:
        """Read a specific Satellite AWS Inventory record"""
        container = self.database.get_container_client(self.SATELLITE_AWS_PRODUCTS)
        pk = [eff_dt]
        item = container.read_item(item=item, partition_key=pk)

        return item

    def satellite_aws_product_update(self, item: dict[str, any]):
        """Read a specific Satellite AWS Inventory record"""
        container = self.database.get_container_client(self.SATELLITE_AWS_PRODUCTS)
        item = container.upsert_item(body=item)
