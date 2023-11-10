from enum import Enum

class PostgresSQLDatabaseConfig(Enum):

    SQL_DATABASE_NAME = 'expense_tracker_chatbot'   
    SQL_DATABASE_USERNAME =  'expense_user'
    SQL_DATABASE_PASSWORD = '<your_password>'
    SQL_DATABASE_HOST =  'localhost'
    PORT = '5432'