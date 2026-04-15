from bs4 import BeautifulSoup
import feedparser
import html
import json
import requests



# Class for news scraper
# Uses threading to speed up process
class NewsScraper:

    def __init__(self, sources):
        self.articles = []
        self.sources = sources
        self.urls = []

    def find_urls(self):
        for source in self.sources:
            for feed in source["feeds"]:
                response = requests.get(feed, headers={"User-Agent": "Mozilla/5.0"})
                response_xml = BeautifulSoup(response.text, "xml")
                
                for url in response_xml.find_all("url"):
                    loc = url.find("loc").get_text(strip=True)
                    if loc.startswith("https://www.foxnews.com/politics"):    
                        self.urls.append({
                            "link": loc,
                            "source_name": source["name"]
                        })

    def scrape(self):
        
        # Had an error with title encoding
        def fix_double_encoding(text):
            try:
                return text.encode('ascii', 'ignore').decode('ascii')
            except:
                return text


        for url in self.urls[:2000]:
            response = requests.get(url["link"])
            response.encoding = response.apparent_encoding
            response_decoded = response.content.decode("utf-8", errors="replace")
            response_html = BeautifulSoup(response_decoded, features="lxml")
            title = fix_double_encoding(html.unescape(response_html.select_one("h1").get_text(strip=True))) if response_html.select_one("h1") else None

            # Possible text content containers for Fox News
            selectors = [
                ".article-body",
                ".article-content",
                ".article-text",
                ".article-body-content"
            ]

            body = ""
            for sel in selectors:
                container = response_html.select_one(sel)
                if container:
                    body = container.get_text(" ", strip=True)
                    body = html.unescape(body)
                    break


            # Only add if title and body were found
            if title and body:
                self.articles.append({
                    "body": body,
                    "source_name": url["source_name"],
                    "title": title
                })