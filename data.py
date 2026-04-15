from news_scraper import NewsScraper
import pandas as pd
import time



# News sources to scrape
# Fox News
sources = [
    {
        "feeds": [
            "https://www.foxnews.com/sitemap.xml?type=articles"
        ],
        "name": "Fox News"
    }
]



# Creating NewsScraper object and scraping sites collected from source feed(s)
# Recording time to run
start = time.perf_counter()
scraper = NewsScraper(sources)
scraper.find_urls()
scraper.scrape()
df = pd.DataFrame(scraper.articles)
df.to_csv("data.csv", index=True)
end = time.perf_counter()

print(f"Time elapsed: {(end - start):.2f} seconds")