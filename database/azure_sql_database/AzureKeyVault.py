from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class AzureKeyVault:

    def __init__(self, key_vault_url):
        self.key_vault_url = key_vault_url

    def get_secret(self, secret_name):
        credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=self.key_vault_url, credential=credential)

        retrieved_secret = secret_client.get_secret(secret_name)
        return retrieved_secret.value
