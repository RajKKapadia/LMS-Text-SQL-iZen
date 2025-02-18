from datetime import datetime
from typing import Dict, List


def get_sql_tool(database_schema_string: str) -> List[Dict]:
    sql_tool = [
        {
            "type": "function",
            "function": {
                "name": "ask_database",
                "description": "Use this function to answer user questions about Production data. Input should be a fully formed MySQL query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": f"""MySQL query extracting info to answer the user"s question.
MySQL should be written using this database schema:
{database_schema_string}
Today"s date is: {datetime.now().strftime("%Y-%m-%d")}
The query should be returned in plain text, not in JSON.
Don"t assume any column names that are not in the database schema."""
                        }
                    },
                    "required": ["query"],
                },
            }
        }
    ]

    return sql_tool


def get_chat_completion_prompt(query: str, formated_chat_history: List[Dict]) -> str:
    chat_completion_prompt = f"""Consider yourself as a helpful data analyst. A user has asked a question: {query}, 
in the context of the following chat history: {formated_chat_history}, politely reply that you don"t have the answer for the question."""

    return chat_completion_prompt


def get_format_sql_response_messages(sql_response: str) -> List[Dict]:
    formatted_sql_response_messages = [
        {"role": "system", "content": "Consider yourself as a helpful data analyst. You help user get information about the data and answer their question."},
        {"role": "user", "content": f"""Convert the following MySQL data into natural language conversation, 
keep the response short and concise and never mention id of the MySQL data. SQL data: {sql_response}"""}
    ]

    return formatted_sql_response_messages


def get_chat_completion_request_system_message() -> Dict:
    system_message = {
        "role": "system", "content": "You are a data analyst. You help user get information about the database."}

    return system_message
