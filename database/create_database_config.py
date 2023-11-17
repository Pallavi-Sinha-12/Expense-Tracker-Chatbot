import yaml

def get_database_config_env_variables():
    print("Select Database Type")
    print("1. PostgresSQL")
    print("2. AzureSQL")

    database_type = input("Enter Database Type: ")

    if database_type == "1":
        print("You have selected PostgresSQL")
        database = input(f"Enter Database Name (default: 'expense_tracker_chatbot'): ") or 'expense_tracker_chatbot'
        username = input(f"Enter Database User Name (default: 'postgres'): ") or 'expense_user'
        password = input("Enter Database Password: ")
        host = input(f"Enter Database Host (default: 'localhost'): ") or 'localhost'
        port = input(f"Enter Database Port (default: '5432'): ") or '5432'

        db_config = {
            "database_type": "PostgresSQL",
            "database": database,
            "username": username,
            "password": password,
            "host": host,
            "port": port
        }

        return db_config
    
    elif database_type == "2":
        print("You have selected AzureSQL")
        server = input("Enter Database Server Name: ")
        database = input(f"Enter Database Name (default: 'expense_tracker_chatbot'): ") or 'expense_tracker_chatbot'
        username = input(f"Enter Database User Name (default: 'postgres'): ") or 'expense_user'
        key_vault_url = input("Enter Key Vault URL: ")
        password_secret = input("Enter Database Password Secret Name: ")

        db_config = {
            "database_type": "AzureSQL",
            "server": server,
            "database": database,
            "username": username,
            "key_vault_url": key_vault_url,
            "password_secret": password_secret
        }

        return db_config
    
    else:
        print("Invalid Input")
        exit()

if __name__ == "__main__":
    db_config = get_database_config_env_variables()

    with open("database/database_config.yaml", "w") as file:
        yaml.dump(db_config, file)

    print("Database Config File Created")
