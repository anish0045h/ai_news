from apidata import get_all_news
import re

def clean_article(text, lowercase=False):
    """
    A multi-step pipeline to clean messy article text scraped from financial news sites.
    """

    if not isinstance(text, str) or not text.strip():
        return ""

    # 1. Remove boilerplate
    boilerplate_patterns = [
        r'\(catch all the business news.*?\)',
        r'subscribe to the economic times prime.*',
        r'get businessline apps on',
        r'connect with us',
        r'to enjoy additional benefits',
        r"\(what's moving sensex and nifty.*?\)",
        r'zdnet\'s recommendations are based on.*',
        r'when you click through from our site.*',
        r'advertisement'
    ]
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # 2. Line-based cleanup
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r'^[+-]?\s?\d{1,3}(?:,\d{3})*(?:\.\d+)?$', stripped):  # numeric garbage
            continue
        if 'photo credit' in stripped.lower():
            continue
        cleaned_lines.append(stripped)

    text = ' '.join(cleaned_lines)

    # 3. Normalization
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s.,?!₹$%–-]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    if lowercase:
        text = text.lower()

    return text


def preprocess_articles(company_name):
    """Fetches, cleans, and returns only cleaned article text."""
    articles = get_all_news(company_name)
    preprocessed_data = []

    for art in articles:
        cleaned_content = clean_article(art.get("content", ""))
        if cleaned_content:  # ignore empty ones
            preprocessed_data.append(cleaned_content)

    return preprocessed_data
'''
if __name__ == "__main__":
    company = input("Enter company name: ").strip()
    if not company:
        print("Please enter a company name.")
    else:
        cleaned_articles = preprocess_articles(company)
        print(f"\n✅ Total cleaned articles: {len(cleaned_articles)}\n")
        for i, text in enumerate(cleaned_articles[:3]):  # show first 3
            print(f"--- Article {i+1} ---\n{text[:5000]}...\n")
'''