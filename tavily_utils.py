import requests
import os

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def get_ground_location_insight(lat, lon):
    if not TAVILY_API_KEY:
        raise ValueError("Missing TAVILY_API_KEY")
    query = f"What's notable or interesting at latitude {lat:.4f}, longitude {lon:.4f}?"
    response = requests.post(
        "https://api.tavily.com/search",
        headers={"Authorization": f"Bearer {TAVILY_API_KEY}"},
        json={"query": query, "search_depth": "advanced", "include_answer": True}
    )
    results = response.json()
    return results.get("results", [])