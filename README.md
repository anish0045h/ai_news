# Ai_News

AI News Summarizer is a Python-based project that automatically fetches the latest financial or company-related news articles, cleans and preprocesses the data, and generates concise AI summaries using a trained transformer model.

This project currently runs as a console-based pipeline, and a web interface will be added in the next stage.

User Input (Company Name)
        ↓
 [apidata.py] → Fetches raw articles from APIs
        ↓
 [preprocess.py] → Cleans and filters the text
        ↓
 [summary_model.py] → Generates summarized output


🧰 Technologies Used

Python 3.10+

BeautifulSoup → For web scraping and content extraction

Transformers (Hugging Face) → For the summarization model

Requests → For fetching API data

PyTorch → Backend for the model

Regex (re) → For text cleaning and normalization


📌 Current Status

✅ API integration complete
✅ Data preprocessing complete
✅ Summarization model integrated
🚧 Web interface development — coming next
