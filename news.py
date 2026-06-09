from newsapi import NewsApiClient
import os
import pandas as pd
import datetime as dt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()



newsapi = NewsApiClient(api_key=os.environ.get("my_api_key"))

# Get top 10 headlines from the US (English language)
top_headlines = newsapi.get_top_headlines(language='en', country='us', page_size=10)

print("=" * 50)
print("TOP 10 HEADLINES")
print("=" * 50)

articles = top_headlines['articles']
for i, article in enumerate(articles, 1):
    print(f"\n{i}. {article['title']}")
    if article.get('description'):
        print(f"   {article['description'][:150]}..." if len(article.get('description', '')) > 150 else f"   {article['description']}")
    print(f"   Source: {article['source']['name']}")
    print(f"   URL: {article['url']}")

