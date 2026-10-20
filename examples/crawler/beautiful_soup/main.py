"""                                                                                                                                   
Integration Example: Guará Browser Automation + BeautifulSoup Parsing.                                                                
                                                                                                                                    
This script demonstrates how to use Guará to handle complex browser interactions                                                      
and hand off the resulting static HTML to BeautifulSoup for efficient data extraction.                                                
"""

import pprint

from guara.abstract_transaction import AbstractTransaction
from guara.application import Application
from bs4 import BeautifulSoup
import sys
import requests
class NavigateToPage(AbstractTransaction):
    def do(self, **kwargs):
        url = "http://quotes.toscrape.com"
        # 1. Navigation / HTTP Fetching
        # Instead of opening a browser, we perform a direct network GET request.
        response = requests.get(url, timeout=10)

        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        # 2. HTML Extraction
        # Extract the page source text directly from the HTTP response metadata.
        page_source = response.text
        return page_source


class ExtractData(AbstractTransaction):
    def do(self, page_source):
        try:
            # 3. Beautiful Soup Integration
            # We use 'lxml' for speed, but 'html.parser' is a valid built-in alternative.
            soup = BeautifulSoup(page_source, "lxml")

            # 4. Data Extraction
            # Using BeautifulSoup's navigation methods.
            print("--- Extracting Quotes ---")
            quotes = soup.find_all("span", class_="text")

            for i, quote in enumerate(quotes, 1):
                print(f"{i}: {quote.get_text()}")

            # Extracting the page title
            title_element = soup.find("h1")
            if title_element and title_element.find("a"):
                title = title_element.find("a").get_text()
                print(f"\nScraped site title: {title}")
            else:
                print("\nCould not find the site title.")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during HTTP network transfer: {e}", file=sys.stderr)
        except Exception as e:
            print(f"An error occurred during parsing: {e}", file=sys.stderr)

def run_scraping_task():
    app = Application()
    try:
        app.execute(NavigateToPage)
        data = app.execute(ExtractData, page_source=app.result)
        pprint.pprint(data)
    except Exception as e:
        print(f"An error occurred during automation: {e}", file=sys.stderr)


if __name__ == "__main__":
    run_scraping_task()
