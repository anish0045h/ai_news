from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from preprocess import preprocess_articles

# Load your fine-tuned BART model
model_path  = r"C:\Users\anish\OneDrive\Desktop\ai_summary\my_bart_summarizer\my_bart_summarizer"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)


def summarize_text(text, max_len=200, min_len=40):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=max_len,
        min_length=min_len,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

if __name__ == "__main__":
    company = input("Enter company name: ").strip()
    cleaned_articles = preprocess_articles(company)

    print(f"\n✅ Found {len(cleaned_articles)} cleaned articles for '{company}'\n")

    for i, article in enumerate(cleaned_articles[:3]):  # summarize first 3
        summary = summarize_text(article)
        print(f"--- Summary {i+1} ---\n{summary}\n")