import requests
import os
from datetime import datetime
from newspaper import Article, Config
import time
from bs4 import BeautifulSoup
from tqdm import tqdm




newsapi = "e29a28ff98b745f5ad9ea530392d2ab0"
#NEWS_URL = "https://newsapi.org/v2/everything"
gnewsapi = "36b988daa36f37cc41185b1654d6c44e"
fmpapi = "5a69eGVW6nbz3ZSsX2aLlak79DrGVL56"
mediapi = "70f15efed939da60b808bced7b39ef68"

'''
def fetch_full_article(url):
    """Fetch full article text with retries and fallback."""
    try:
        # Skip API or non-HTML links
        if any(x in url for x in ["api.", ".json", "rss", "feed"]):
            return None

        config = Config()
        config.fetch_images = False
        config.memoize_articles = False
        config.browser_user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )

        article = Article(url, config=config)

        # Try newspaper3k first
        try:
            article.download()
            article.parse()
            if article.text and len(article.text.strip()) > 200:
                time.sleep(1.5)  # avoid rate limiting
                return article.text
        except Exception as e:
            print(f"newspaper3k failed: {e}")

        # If newspaper3k fails → fallback using requests
        headers = {"User-Agent": config.browser_user_agent}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.ok and "text/html" in resp.headers.get("Content-Type", ""):
            text = resp.text
            return text[:2000]  # just a raw HTML preview (not parsed)
        return None

    except Exception as e:
        print(f"Error fetching article from {url}: {e}")
        return None
'''
def fetch_full_article_bs(url):
    """Fetch full article content using BeautifulSoup."""
    if not url:
        return None
    
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Try to extract text from <article> or <p> tags
        article_text = ""
        article_tag = soup.find("article")

        if article_tag:
            paragraphs = article_tag.find_all("p")
        else:
            paragraphs = soup.find_all("p")

        article_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

        # Clean up and return if there's meaningful content
        if len(article_text.strip()) > 300:
            return article_text.strip()
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching article: {e}")
        return None
    finally:
        time.sleep(1)


def fetch_all_articles(news_list):
    """Fetch full article text for each news item (list of dicts)."""
    if not isinstance(news_list, list):
        print("⚠️ Expected a list of news articles, but got something else.")
        return []

    for article in tqdm(news_list, desc="Fetching full articles", unit="article"):
        url = article.get("url") if isinstance(article, dict) else None
        if url:
            full_text = fetch_full_article_bs(url)
            article["content"] = full_text if full_text else "Not available"
        else:
            article["content"] = "Not available"
    return news_list


def fetch_from_newsapi(company_name):
    """Fetches news from NewsAPI.org and standardizes the output."""
    print("Fetching from NewsAPI...")
    if not newsapi:
        return []
    
    url = f"https://newsapi.org/v2/everything?q={company_name}&apiKey={newsapi}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        
        # Standardize the data
        standardized_articles = []
        for article in articles:
            standardized_articles.append({
                "title": article.get("title"),
                "url": article.get("url"),
                "source": article.get("source", {}).get("name"),
                "published_at": article.get("publishedAt"),
                "content": None  # to be filled later
            })
        standardized_articles = fetch_all_articles(standardized_articles)
        
        return standardized_articles
    except requests.exceptions.RequestException as e:
        print(f"NewsAPI Error: {e}")
        return []


    
def fetch_from_gnews(company_name):
    """Fetches news from GNews and standardizes the output."""
    print("Fetching from GNews...")
    if not gnewsapi:
        return []
        
    url = f"https://gnews.io/api/v4/search?q={company_name}&lang=en&apikey={gnewsapi}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        
        standardized_articles = []
        for article in articles:
            standardized_articles.append({
                "title": article.get("title"),
                "url": article.get("url"),
                "source": article.get("source", {}).get("name"),
                "published_at": article.get("publishedAt"),
                "content": None
            })
        standardized_articles = fetch_all_articles(standardized_articles)
        
        return standardized_articles
    except requests.exceptions.RequestException as e:
        print(f"GNews Error: {e}")
        return []
'''
def fetch_from_fmp(company_name):
    """Fetches news from Financial Modeling Prep (FMP) and standardizes the output."""
    # Note: FMP works best with stock tickers (e.g., AAPL).
    print("Fetching from FMP...")
    if not fmpapi:
        return []
        
    url = f"https://financialmodelingprep.com/api/v3/stock_news?tickers={company_name}&limit=50&apikey={fmpapi}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json() # FMP returns a list directly
        
        standardized_articles = []
        for article in articles:
            standardized_articles.append({
                "title": article.get("title"),
                "url": article.get("url"),
                "source": article.get("site"),
                "published_at": article.get("publishedDate"),
                "content": fetch_full_article(url) if article.get("url") else None
            })
        return standardized_articles
    except requests.exceptions.RequestException as e:
        print(f"FMP Error: {e}")
        return []
'''   
def fetch_from_mediastack(company_name):
    """Fetches news from Mediastack and standardizes the output."""
    print("Fetching from Mediastack...")
    if not mediapi:
        return []
        
    url = f"http://api.mediastack.com/v1/news?access_key={mediapi}&keywords={company_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("data", [])
        
        standardized_articles = []
        for article in articles:
            standardized_articles.append({
                "title": article.get("title"),
                "url": article.get("url"),
                "source": article.get("source"),
                "published_at": article.get("published_at"),
                "content": None
            })
        standardized_articles = fetch_all_articles(standardized_articles)
        
        return standardized_articles
    except requests.exceptions.RequestException as e:
        print(f"Mediastack Error: {e}")
        return []
    
def get_all_news(company_name):
    """Fetches news from all sources, combines, and cleans the results."""
    # Call all fetcher functions
    all_articles = []
    all_articles.extend(fetch_from_newsapi(company_name))
    all_articles.extend(fetch_from_gnews(company_name))
    #all_articles.extend(fetch_from_fmp(company_name))
    all_articles.extend(fetch_from_mediastack(company_name))
    unique_articles = {article['url']: article for article in all_articles if article['url']}.values()
    # Standardize each article
    standardized_articles = []
    for art in unique_articles:
        standardized_articles.append({
            "title": art.get("title", "No title"),
            "source": art.get("source", "Unknown"),
            "url": art.get("url", None),
            "published": art.get("published_at") or art.get("publishedAt") or "",
            "content": art.get("content") or "Not available"
        })

    # Sort by published date (most recent first)
    sorted_articles = sorted(
        standardized_articles,
        key=lambda x: x['published'] or '',
        reverse=True
    )

    return sorted_articles

'''
if __name__ == "__main__":
    user_input = input("Enter a company name (e.g., Infosys, Apple): ").strip()

    if user_input:
        # Step 1: Fetch metadata from APIs
        final_news_list = get_all_news(user_input)
        print(f"\n--- Found {len(final_news_list)} unique articles for '{user_input}' ---")

        # Step 2: Fetch full article text using BeautifulSoup
        print("\nFetching full articles (please wait)...\n")
        for i, article in enumerate(final_news_list[:10]):  # limit to top 5 for demo
            print(f"\n{i+1}. Title: {article['title']}")
            print(f"   Source: {article['source']}")
            print(f"   URL: {article['url']}")

            # Format the publication date
            try:
                date = datetime.fromisoformat(article['published'].replace('Z', '+00:00'))
                print(f"   Published: {date.strftime('%Y-%m-%d %H:%M')}")
            except (ValueError, TypeError):
                print(f"   Published: {article['published']}")

            # Fetch full content using BeautifulSoup
            url = article.get("url")
            if url:
                full_text = fetch_full_article_bs(url)
                if full_text:
                    article["content"] = full_text
                    print("\n--- Full Article ---")
                    print(full_text[:500])  # print first 1500 chars only
                    print("\n--------------------")
                else:
                    article["content"] = "Not available"
                    print("   Content: Not available")
            else:
                article["content"] = "Not available"
                print("   Content: Not available")
        
        # Step 3: Save all results to JSON file
        filename = f"{user_input.replace(' ', '_')}_articles.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(final_news_list, f, indent=4, ensure_ascii=False)

        print(f"\n✅ All articles saved to '{filename}'")
        
'''
