from database.azure_sql_database.AzureKeyVault import AzureKeyVault
from database.azure_sql_database.AzureSQLDatabaseConnector import AzureSQLDatabaseConnector
from database.azure_sql_database.AzureSQLVisualisationQuery import AzureSQLVisualisationQuery
from database.postgres_sql_database.PostgresSQLDatabaseConnector import PostgresSQLDatabaseConnector
from database.postgres_sql_database.PostgresVisualisationQuery import PostgresVisualisationQuery

class DatabaseFactory:

    @staticmethod
    def get_database_connector_instance(**kwargs):
        database_type = kwargs["database_type"]
        if database_type == "AzureSQL":
            azureKeyVault = AzureKeyVault(kwargs["key_vault_url"])
            sql_database_password = azureKeyVault.get_secret(kwargs["password_secret"])
            return AzureSQLDatabaseConnector(kwargs["server"], kwargs["database"], kwargs["username"], sql_database_password)
        elif database_type == "PostgresSQL":
            return PostgresSQLDatabaseConnector(kwargs["host"], kwargs["port"], kwargs["database"], kwargs["username"], kwargs["password"])
        else:
            print("Unsupported database type")
            return None
        
    @staticmethod
    def get_visualisation_query_instance(database_type, vis_group_by_type, vis_aggregate_type, vis_time_period):
        if database_type == "AzureSQL":
            return AzureSQLVisualisationQuery(vis_group_by_type, vis_aggregate_type, vis_time_period)
        
        elif database_type == "PostgresSQL":
            return PostgresVisualisationQuery(vis_group_by_type, vis_aggregate_type, vis_time_period)
       
        else:
            print("Unsupported database type")
            return None