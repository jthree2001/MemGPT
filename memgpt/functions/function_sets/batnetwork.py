import json
from wmill import Windmill
import os


### Functions / tools the agent can use
# All functions should return a response string (or None)
# If the function fails, throw an exception

def web_search(self, search_string: str):
    """
    Search the web for infromation on the search string provided.

    Args:
        search_string (str): String to search for.

    Returns:
        str: Query result string
    """
    # windmill_token = os.getenv("WINDMILL_TOKEN")
    windmill_token = "DngylpNkfbqZeX0mkSUUb4sBSnMalO"
    try:
        wmill_client = Windmill(base_url = "https://windmill.batbro.us", token=windmill_token, workspace="batnetwork")
        result_full = wmill_client.run_script("u/michael/rewoo_execution", args= {"task_input": search_string})
        
        return result_full["response"]["choices"][0]["message"]["content"]
    except Exception as e:
        return {"error": str(e)}
