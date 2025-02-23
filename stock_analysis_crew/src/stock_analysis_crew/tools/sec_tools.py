import os
from typing import Any, Optional
from sec_api import QueryApi  # Make sure to have sec_api installed
import requests
import html2text
import re

class SEC10KTool:
    name: str = "Search in the specified 10-K form"
    description: str = "A tool that can be used to fetch a query from a 10-K form for a specified company."

    def __init__(self, stock_name: Optional[str] = None):
        self.stock_name = stock_name
        if stock_name is not None:
            self.description = f"Fetches {stock_name}'s latest 10-K SEC form's content as a txt file."

    def get_10k_url_content(self) -> Optional[str]:
        """Fetches the URL content as txt of the latest 10-K form for the given stock name."""
        try:
            queryApi = QueryApi(api_key=os.environ['SEC_API_API_KEY'])
            query = {
                "query": {
                    "query_string": {
                        "query": f"ticker:{self.stock_name} AND formType:\"10-K\""
                    }
                },
                "from": "0",
                "size": "1",
                "sort": [{ "filedAt": { "order": "desc" }}]
            }
            filings = queryApi.get_filings(query)['filings']
            if not filings:
                return None

            url = filings[0]['linkToFilingDetails']
            headers = {
                "User-Agent": "crewai.com bisan@crewai.com",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            h = html2text.HTML2Text()
            h.ignore_links = False
            text = h.handle(response.content.decode("utf-8"))
            return re.sub(r"[^a-zA-Z$0-9\s\n]", "", text)
        except requests.exceptions.HTTPError:
            return None
        except Exception:
            return None


class SEC10QTool:
    name: str = "Search in the specified 10-Q form"
    description: str = "A tool that can be used to fetch a query from a 10-Q form for a specified company."

    def __init__(self, stock_name: Optional[str] = None):
        self.stock_name = stock_name
        if stock_name is not None:
            self.description = f"Fetches {stock_name}'s latest 10-Q SEC form's content as a txt file."

    def get_10q_url_content(self) -> Optional[str]:
        """Fetches the URL content as txt of the latest 10-Q form for the given stock name."""
        try:
            queryApi = QueryApi(api_key=os.environ['SEC_API_API_KEY'])
            query = {
                "query": {
                    "query_string": {
                        "query": f"ticker:{self.stock_name} AND formType:\"10-Q\""
                    }
                },
                "from": "0",
                "size": "1",
                "sort": [{ "filedAt": { "order": "desc" }}]
            }
            filings = queryApi.get_filings(query)['filings']
            if not filings:
                return None

            url = filings[0]['linkToFilingDetails']
            headers = {
                "User-Agent": "crewai.com bisan@crewai.com",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            h = html2text.HTML2Text()
            h.ignore_links = False
            text = h.handle(response.content.decode("utf-8"))
            return re.sub(r"[^a-zA-Z$0-9\s\n]", "", text)
        except requests.exceptions.HTTPError:
            return None
        except Exception:
            return None