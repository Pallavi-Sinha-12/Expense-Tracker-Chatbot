# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from pytz import timezone 
from datetime import datetime, timedelta

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import AllSlotsReset
from database.AzureKeyVault import AzureKeyVault
from data_exporter.CSVFile import CSVFile
from database.SQLDatabase import SQLDatabase
from database.SQLQuery import SQLQuery
from database.DatabaseConfig import DatabaseConfig

EXPENSE_CATEGORIES =  ["household", "transportation", "work&education", "food&dining", "entertainment"]


class ValidateExpenseForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_expense_form"

    def validate_expense_category(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if slot_value.lower() in EXPENSE_CATEGORIES:
            dispatcher.utter_message(text=f"Great, I will categorize it as {slot_value}.")
            return {"expense_category": slot_value}
        elif slot_value.lower() == "default":
            dispatcher.utter_message(text=f"I don't understand the category")
            return {"expense_category": None}
        else:
            dispatcher.utter_message(text=f"Sorry, Can you enter any of these 5 {'/'.join(EXPENSE_CATEGORIES)}.")
            return {"expense_category": None}
        
    def validate_expense_amount(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if slot_value.isnumeric():
            dispatcher.utter_message(text=f"Sure, I will enter the amount as {slot_value}.")
            return {"expense_amount": slot_value}
        else:
            dispatcher.utter_message(text=f"Sorry, Can you enter the amount in whole number?")
            return {"expense_amount": None}
        
    def validate_expense_date(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if slot_value.lower() == "today":
            date = datetime.now(timezone('Asia/Kolkata')).strftime("%Y-%m-%d")
            dispatcher.utter_message(text=f"Sure, I will enter the date as {date}.")
            return {"expense_date": date}
        elif slot_value.lower() == "yesterday":
            date = (datetime.now(timezone('Asia/Kolkata')) - timedelta(days=1)).strftime("%Y-%m-%d")
            dispatcher.utter_message(text=f"Sure, I will enter the date as {date}.")
            return {"expense_date": date}
        elif slot_value.lower() == "day before yesterday":
            date = (datetime.now(timezone('Asia/Kolkata')) - timedelta(days=2)).strftime("%Y-%m-%d")
            dispatcher.utter_message(text=f"Sure, I will enter the date as {date}.")
            return {"expense_date": date}
        elif slot_value.lower() == "tomorrow":
            date = (datetime.now(timezone('Asia/Kolkata')) + timedelta(days=1)).strftime("%Y-%m-%d")
            dispatcher.utter_message(text=f"Sure, I will enter the date as {date}.")
            return {"expense_date": date}
        elif slot_value.lower() == "day after tomorrow":
            date = (datetime.now(timezone('Asia/Kolkata')) + timedelta(days=2)).strftime("%Y-%m-%d")
            dispatcher.utter_message(text=f"Sure, I will enter the date as {date}.")
            return {"expense_date": date}
        elif len(slot_value.split("-")) == 3:
            try:
                datetime.strptime(slot_value, '%Y-%m-%d')
                dispatcher.utter_message(text=f"Sure, I will enter the date as {slot_value}.")
                return {"expense_date": slot_value}
            except ValueError:
                dispatcher.utter_message(text=f"Sorry, Can you enter the date in yyyy-mm-dd format?")
                return {"expense_date": None}
        else:
            dispatcher.utter_message(text=f"Sorry, Can you enter the date in yyyy-mm-dd format?")
            return {"expense_date": None}
        
    def validate_expense_confirmation(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if tracker.get_intent_of_latest_message() == "affirm":
            dispatcher.utter_message(text=f"Great, Your expense details are submitted.")
            return {"expense_confirmation": True}
        elif tracker.get_intent_of_latest_message() == "deny":
            dispatcher.utter_message(text=f"Ok, I will not submit the expense.")
            return {"expense_confirmation": False}
        else:
            dispatcher.utter_message(text=f"Sorry, Can you enter either yes or no?")
            return {"expense_confirmation": None}

class AskForExpenseCategory(Action):
    def name(self) -> Text:
        return "action_ask_expense_category"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Please select the category of your expense.", buttons=[{"payload": "default", "title": "default"}, {"payload": "household", "title": "household"}, {"payload": "transportation", "title": "transportation"}, {"payload": "work&education", "title": "work&education"}, {"payload": "food&dining", "title": "food&dining"}, {"payload": "entertainment", "title": "entertainment"}])
        return []
    
class ActionAskExpenseAmount(Action):
    def name(self) -> Text:
        return "action_ask_expense_amount"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Please enter the expense amount in numbers.")
        return []
    
class ActionAskExpenseDate(Action):
    def name(self) -> Text:
        return "action_ask_expense_date"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Please enter the date of your expenditure.")
        return []
    

class ActionResetExpenseForm(Action):
    def name(self) -> Text:
        return "action_reset_expense_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]

class ActionAskExpenseConfirmation(Action):
    def name(self) -> Text:
        return "action_ask_expense_confirmation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        expense_category = tracker.get_slot("expense_category")
        expense_amount = tracker.get_slot("expense_amount")
        expense_date = tracker.get_slot("expense_date")
        message = f"I will submit the expense of {expense_amount} in {expense_category} category on {expense_date}. \n Please confirm."
        dispatcher.utter_message(text= message)
        return []
    
class ActionSubmitExpenseForm(Action):
    def name(self) -> Text:
        return "action_submit_expense_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        if tracker.get_intent_of_latest_message() == "affirm":
            expense_category = tracker.get_slot("expense_category")
            expense_amount = tracker.get_slot("expense_amount")
            expense_date = tracker.get_slot("expense_date")
            column_value_dict = {"category": expense_category, "amount": expense_amount, "date": expense_date}
            
            sql_server_name = DatabaseConfig.SQL_DATABASE_SERVER_NAME.value
            sql_database_name = DatabaseConfig.SQL_DATABASE_NAME.value
            sql_database_username = DatabaseConfig.SQL_DATABASE_USERNAME.value
            key_vault_url =  DatabaseConfig.KEY_VAULT_URL.value
            sql_database_password_secret_name = DatabaseConfig.SQL_DATABASE_PASSWORD_SECRET_NAME.value
            
            azureKeyVault = AzureKeyVault(key_vault_url)
            sql_database_password = azureKeyVault.get_secret(sql_database_password_secret_name)
            sqlDatabase = SQLDatabase(sql_server_name, sql_database_name, sql_database_username, sql_database_password)
            print(column_value_dict)
            sqlDatabase.insert_data("expense", column_value_dict)
            return []
        else:
            return [AllSlotsReset()]
        
class ActionAskVisulationGroupByType(Action):
    def name(self) -> Text:
        return "action_ask_vis_group_by_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Should the visualisation show trends over time or should it focus on comparing expenses across different spending categories?.")
        return []   
    
class ActionAskVisualisationAggregateType(Action):
    def name(self) -> Text:
        return "action_ask_vis_aggregate_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="What kind of summary would you prefer for the expense amounts?", buttons=[{"payload": "default", "title": "default"}, {"payload": "sum", "title": "sum"}, {"payload": "average", "title": "average"}, {"payload": "minimum", "title": "minimum"}, {"payload": "maximum", "title": "maximum"}])
        return []
    
class ActionAskVisualisationTimePeriod(Action):
    def name(self) -> Text:
        return "action_ask_vis_time_period"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Could you please specify the specific timeframe you're interested in? Please provide the start and end dates for the period you'd like to analyze.")
        return []
    
class ActionSubmitVisualisationForm(Action):
    def name(self) -> Text:
        return "action_submit_visualisation_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        vis_group_by_type = tracker.get_slot("vis_group_by_type")
        vis_aggregate_type = tracker.get_slot("vis_aggregate_type")
        vis_time_period = tracker.get_slot("vis_time_period")
        message = f"Here is the visualisation of {vis_aggregate_type} of expenses over {vis_time_period} grouped by {vis_group_by_type}."

        sqlQuery = SQLQuery(vis_group_by_type, vis_aggregate_type, vis_time_period)
        query = sqlQuery.create()
        print(query)
        sql_server_name = DatabaseConfig.SQL_DATABASE_SERVER_NAME.value
        sql_database_name = DatabaseConfig.SQL_DATABASE_NAME.value
        sql_database_username = DatabaseConfig.SQL_DATABASE_USERNAME.value
        key_vault_url =  DatabaseConfig.KEY_VAULT_URL.value
        sql_database_password_secret_name = DatabaseConfig.SQL_DATABASE_PASSWORD_SECRET_NAME.value
        
        azureKeyVault = AzureKeyVault(key_vault_url)
        sql_database_password = azureKeyVault.get_secret(sql_database_password_secret_name)
        sqlDatabase = SQLDatabase(sql_server_name, sql_database_name, sql_database_username, sql_database_password)
        data = sqlDatabase.get_data(query)
        
        if vis_group_by_type in ["category", "categories"]:
            csvFile = CSVFile(data, ["Expense Categories", f"{vis_aggregate_type.capitalize()} Expense Amount"])
        else:
            csvFile = CSVFile(data, ["Time intervals", f"{vis_aggregate_type.capitalize()} Expense Amount"])
        data_path = csvFile.write()
        dispatcher.utter_message(text= message,image=data_path)
        return []
    
class ValidateVisualisationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_visualisation_form"

    def validate_vis_group_by_type(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if slot_value.lower() in ["time", "categories", "category"]:
            dispatcher.utter_message(text=f"Great, I will group the expenses by {slot_value}.")
            return {"vis_group_by_type": slot_value}
        else:
            dispatcher.utter_message(text=f"Sorry, Can you enter either time or category?")
            return {"vis_group_by_type": None}
        
    def validate_vis_aggregate_type(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if slot_value.lower() in ["sum", "average", "minimum", "maximum"]:
            dispatcher.utter_message(text=f"Great, I will aggregate the expenses {slot_value}.")
            return {"vis_aggregate_type": slot_value}
        else:
            dispatcher.utter_message(text=f"Sorry, Can you enter either sum, average, minimum or maximum?")
            return {"vis_aggregate_type": None}
        
    def validate_vis_time_period(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        if slot_value.lower() == "last month":
            start_date = (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1).strftime('%Y-%m-%d')
            end_date = (datetime.now().replace(day=1) - timedelta(days=1)).strftime('%Y-%m-%d')
            dispatcher.utter_message(text=f"Sure, I will enter the time period as {start_date} to {end_date}.")
            return {"vis_time_period": f"{start_date} to {end_date}"}
        elif slot_value.lower() == "last week":
            start_date = (datetime.now(timezone('Asia/Kolkata')) - timedelta(days=7)).strftime("%Y-%m-%d")
            end_date = datetime.now(timezone('Asia/Kolkata')).strftime("%Y-%m-%d")
            dispatcher.utter_message(text=f"Sure, I will enter the time period as {start_date} to {end_date}.")
            return {"vis_time_period": f"{start_date} to {end_date}"}
        elif slot_value.lower() == "this month":
            start_date = datetime.now(timezone('Asia/Kolkata')).strftime("%Y-%m-01")
            end_date = datetime.now(timezone('Asia/Kolkata')).strftime("%Y-%m-%d")
            dispatcher.utter_message(text=f"Sure, I will enter the time period as {start_date} to {end_date}.")
            return {"vis_time_period": f"{start_date} to {end_date}"}
        elif slot_value.lower() == "this week":
            start_date = (datetime.now(timezone('Asia/Kolkata')) - timedelta(days=datetime.now(timezone('Asia/Kolkata')).weekday())).strftime("%Y-%m-%d")
            end_date = datetime.now(timezone('Asia/Kolkata')).strftime("%Y-%m-%d")
            dispatcher.utter_message(text=f"Sure, I will enter the time period as {start_date} to {end_date}.")
            return {"vis_time_period": f"{start_date} to {end_date}"}
        elif slot_value.lower() == "today":
            date = datetime.now(timezone('Asia/Kolkata')).strftime('%Y-%m-%d')
            dispatcher.utter_message(text=f"Sure, I will enter the time period as {date} to {date}.")
            return {"vis_time_period": f"{date} to {date}"}
        elif slot_value.lower() == "yesterday":
            date = (datetime.now(timezone('Asia/Kolkata')) - timedelta(days=1)).strftime("%Y-%m-%d")
            dispatcher.utter_message(text=f"Sure, I will enter the time period as {date} to {date}.")
            return {"vis_time_period": f"{date} to {date}"}
        elif slot_value.lower() == "day before yesterday":
            date = (datetime.now(timezone('Asia/Kolkata')) - timedelta(days=2)).strftime("%Y-%m-%d")
            dispatcher.utter_message(text=f"Sure, I will enter the time period as {date} to {date}.")
            return {"vis_time_period": f"{date} to {date}"}
        elif slot_value.lower() == "last year":
            start_date = datetime(datetime.now().year - 1, 1, 1).strftime('%Y-%m-%d')
            end_date = (datetime(datetime.now().year, 1, 1) - timedelta(days=1)).strftime('%Y-%m-%d')
            dispatcher.utter_message(text=f"Sure, I will enter the time period as {start_date} to {end_date}.")
            return {"vis_time_period": f"{start_date} to {end_date}"}
        elif slot_value.lower() == "this year":
            start_date = datetime.now(timezone('Asia/Kolkata')).strftime("%Y-01-01")
            end_date = datetime.now(timezone('Asia/Kolkata')).strftime("%Y-%m-%d")
            dispatcher.utter_message(text=f"Sure, I will enter the time period as {start_date} to {end_date}.")
            return {"vis_time_period": f"{start_date} to {end_date}"}        
        elif len(slot_value.split(" to ")) == 2:
            try:
                start_date, end_date = slot_value.split(" to ")
                datetime.strptime(start_date, "%Y-%m-%d")
                datetime.strptime(end_date, "%Y-%m-%d")
                dispatcher.utter_message(text=f"Sure, I will enter the time period as {start_date} to {end_date}.")
                return {"vis_time_period": f"{start_date} to {end_date}"}
            except ValueError:
                dispatcher.utter_message(text=f"Sorry, Can you enter the time period in yyyy-mm-dd to yyyy-mm-dd format?")
                return {"vis_time_period": None}
        else:
            dispatcher.utter_message(text=f"Sorry, Can you enter the time period in yyyy-mm-dd to yyyy-mm-dd format?")
            return {"vis_time_period": None}
        
class ActionResetVisualisationForm(Action):
    def name(self) -> Text:
        return "action_reset_visualisation_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]
