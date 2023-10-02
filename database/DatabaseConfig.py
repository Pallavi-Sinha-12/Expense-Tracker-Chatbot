from enum import Enum

class DatabaseConfig(Enum):

    SQL_DATABASE_SERVER_NAME = "expense-tracker-database-server.database.windows.net"
    SQL_DATABASE_NAME = "expense-tracker-database"
    SQL_DATABASE_USERNAME = "expense-user"
    KEY_VAULT_URL = "https://keyvault2806.vault.azure.net/"
    SQL_DATABASE_PASSWORD_SECRET_NAME = "expense-sql-database-password"