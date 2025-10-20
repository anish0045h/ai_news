# Ai_News

AI News Summarizer is a Python-based project that automatically fetches the latest financial or company-related news articles, cleans and preprocesses the data, and generates concise AI summaries using a trained transformer model.

This project currently runs as a console-based pipeline, and a web interface will be added in the next stage.

🚀 Key Features

-> Dynamic News Fetching: Gathers real-time news articles from multiple web APIs based on a user-provided company name.

-> Intelligent Text Cleaning: Automatically strips raw HTML, advertisement boilerplate, and other non-content elements to extract pure article text.

-> State-of-the-Art Summarization: Leverages a pre-trained Transformer model from Hugging Face to produce high-quality, abstractive summaries.

-> Modular Pipeline: Each step of the process (data fetching, preprocessing, and modeling) is separated into its own module for easy maintenance and testing.

⚙️ How It Works
The project follows a simple, three-step data pipeline:

User Input (Company Name)
        ->
[apidata.py] → Fetches raw articles from APIs
        ->
[preprocess.py] → Cleans and filters the text
        ->
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
