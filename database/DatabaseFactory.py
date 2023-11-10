from database.azure_sql_database.AzureSQLDatabaseConnector import AzureSQLDatabaseConnector
from database.azure_sql_database.AzureSQLVisualisationQuery import AzureSQLVisualisationQuery
from database.postgres_sql_database.PostgresSQLDatabaseConnector import PostgresSQLDatabaseConnector
from database.postgres_sql_database.PostgresVisualisationQuery import PostgresVisualisationQuery

class DatabaseFactory:

    @staticmethod
    def get_database_connector_instance(database_type, **kwargs):
        if database_type == "AzureSQL":
            return AzureSQLDatabaseConnector(kwargs["server"], kwargs["database"], kwargs["username"], kwargs["password"])
        elif database_type == "PostgresSQL":
            return PostgresSQLDatabaseConnector(kwargs["host"], kwargs["port"], kwargs["database"], kwargs["user"], kwargs["password"])
        else:
            print("Unsupported database type")
            return None
        
    @staticmethod
    def get_visualisation_query_instance(database_type, vis_group_by_type, vis_aggregate_type, vis_time_period, **kwargs):
        if database_type == "AzureSQL":
            return AzureSQLVisualisationQuery(vis_group_by_type, vis_aggregate_type, vis_time_period)
        
        elif database_type == "PostgresSQL":
            return PostgresVisualisationQuery(vis_group_by_type, vis_aggregate_type, vis_time_period)
       
        else:
            print("Unsupported database type")
            return None