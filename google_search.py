"""
Google Search MCP Server

This module sets up an MCP server to perform Google search queries
and parse web content from the search results using the Google Search API.
"""

# Importing necessary libraries

import os
import requests
from collections import defaultdict
from datetime import datetime
from typing import List
from dotenv import load_dotenv
from readability import Document
from bs4 import BeautifulSoup
from googlesearch import search
from mcp.server.fastmcp import FastMCP

# Creating an instance of the FastMCP server with the name "google_search"

mcp = FastMCP("google_search")


@mcp.tool()
async def query_google_top_results(params: str) -> list:
    """
    This function executes a search query using Google and return a list of top URLs.

    Parameters:
        params (str): The search term or phrase.

    Returns:
        list: A list of URLs returned by the search engine.
    """
    results = list(search(params))
    return results


@mcp.tool()
async def parse_google_html(params: str) -> str:
    """
    This function fetches and extract plain text content from the given web page URL.

    Parameters:
        params (str): The URL to fetch and parse.

    Returns:
        str: Cleaned and structured text content from the web page.
    """
    response = requests.get(params, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(separator="\n", strip=True)
    return page_text


def main():
    # Starting the MCP server with standard I/O transport
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
