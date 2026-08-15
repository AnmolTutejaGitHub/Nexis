from tavily import TavilyClient
import os

def web_search(query):
    try:
        tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = tavily_client.search(query)
        return f"{response}"
    except Exception as e:
        return f"Error: {str(e)[:500]}"
