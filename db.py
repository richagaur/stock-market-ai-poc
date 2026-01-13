from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient

def get_cosmos_container():
    COSMOS_ENDPOINT = "https://<cosmos-account-name>.documents.azure.com:443/"
    COSMOS_DATABASE = "Stocks"
    COSMOS_CONTAINER = "StocksInfo"
    client = CosmosClient(COSMOS_ENDPOINT, credential=DefaultAzureCredential())
    container = client.get_database_client(COSMOS_DATABASE).get_container_client(COSMOS_CONTAINER)
    return container