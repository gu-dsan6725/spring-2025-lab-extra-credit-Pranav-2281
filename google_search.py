
"""
Google Custom Search MCP Server

This script sets up an MCP server to allow querying Google via the Custom Search API,
and extracts readable content from the top results using Readability and BeautifulSoup.
"""

import os
import requests
from typing import List
from dotenv import load_dotenv
from readability import Document
from bs4 import BeautifulSoup

from mcp.server.fastmcp import FastMCP

# Loading the environment variables from a .env file
load_dotenv()

# Retrieving the necessary credentials from environment variables
API_KEY = os.getenv("google_api")
CSE_ID = os.getenv("search_engine")

# Initializing the MCP server with a custom name
mcp = FastMCP("google_custom_search")

def extract_readable_text_from_url(url: str) -> str:
    """
    Fetches the content of a given URL and extracts clean, readable text.

    Args:
        url (str): The URL of the webpage.

    Returns:
        str: Readable text extracted from the main body of the page.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    doc = Document(response.text)
    html_main = doc.summary()

    soup = BeautifulSoup(html_main, "html.parser")
    return soup.get_text(separator="\n", strip=True)


@mcp.tool()
async def google_query_summary(query: str) -> List[str]:
    """
    Uses Google Custom Search API to get and summarize top search results.

    Args:
        query (str): The search term.

    Returns:
        List[str]: A list of clean textual summaries from top search result pages.
    """
    api_endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": API_KEY,
        "cx": CSE_ID,
        "num": 4  # Number of results to retrieve
    }

    try:
        search_response = requests.get(api_endpoint, params=params)
        search_response.raise_for_status()
        search_data = search_response.json()
    except Exception as err:
        return [f"Search failed: {str(err)}"]

    content_list = []

    for idx, result in enumerate(search_data.get("items", []), start=1):
        url = result.get("link", "")
        try:
            cleaned_text = extract_readable_text_from_url(url)
            content_list.append(cleaned_text)
        except Exception as fetch_err:
            content_list.append(f"Failed to extract content from {url}: {str(fetch_err)}")

    return content_list


def start_server():
    """
    Starts the MCP server using standard I/O transport.
    """
    print("MCP Google Search Server is now running...")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    start_server()
