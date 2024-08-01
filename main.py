import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import environment as E


def get_search_results(query, num_results):
    params = {
        "engine": "google",
        "q": query,
        "num": num_results,
        "api_key": E.SERPAPI_KEY_ 
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    urls = []
    for result in results.get("organic_results", []):
        link = result.get("link")
        if link:
            urls.append(link)
    
    return urls

def check_url(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code
    except requests.RequestException:
        return None

def main():
    query = "site:.gov.co"
    num_results = 10
    results = get_search_results(query, num_results)

    domains = {"http": [], "https": []}
    for url in results:
        if url.startswith("http://"):
            domains["http"].append(url)
        elif url.startswith("https://"):
            domains["https"].append(url)
    
    for protocol, urls in domains.items():
        print(f"\nChecking {protocol.upper()} URLs:")
        for url in urls:
            status = check_url(url)
            print(f"URL: {url}, Status: {status}")

if __name__ == "__main__":
    main()
