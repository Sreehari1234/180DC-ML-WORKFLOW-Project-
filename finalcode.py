import os
import re
import requests
import matplotlib.pyplot as plt
import nltk
from sec_edgar_downloader import Downloader
from nltk.corpus import stopwords

# Download NLTK stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Step 1: Download Microsoft 10-K filings
def download_microsoft_filings():
    dl = Downloader(company_name="Microsoft Corporation", email_address="ssreehari2205@gmail.com")
    dl.get("10-K", "MSFT")
    # Default data directory used by sec-edgar-downloader
    filing_directory = os.path.join(os.getcwd(), "SEC-Edgar-Data", "MSFT", "10-K")
    return filing_directory

# Step 2: Select the 5 most recent filings and clean the text
def get_latest_filings(filing_dir, num_filings=5):
    filings = []
    for root, dirs, files in os.walk(filing_dir):
        for file in sorted(files, reverse=True):  # Sort by date and select the most recent
            if file.endswith(".txt"):
                filings.append(os.path.join(root, file))
            if len(filings) == num_filings:
                break
        if len(filings) == num_filings:
            break
    return filings

def clean_text(text):
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove non-alphanumeric characters
    text = text.lower()  # Convert to lowercase
    words = text.split()
    words = [word for word in words if word not in stop_words]  # Remove stopwords
    return ' '.join(words)

def read_and_clean_filings(filing_paths):
    all_texts = []
    for file_path in filing_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
            cleaned_text = clean_text(raw_text)
            all_texts.append(cleaned_text)
    return all_texts

# Step 3: Get insights using LLM via OpenAI API
def get_insights(api_key, texts):
    insights = []
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    
    query = "Analyze Microsoft's financial performance trends over the past 5 years based on this 10-K filing."

    for text in texts:
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': query + text}]
        }
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        if 'choices' in response_json:
            insight = response_json['choices'][0]['message']['content']
            insights.append(insight)
        else:
            print("Error in response:", response_json)
    
    return insights

# Step 4: Visualize insights 
def plot_insights(years, revenues, profits):
    plt.figure(figsize=(8, 5))
    plt.plot(years, revenues, marker='o', label='Revenue')
    plt.plot(years, profits, marker='o', label='Profit')
    plt.title('Microsoft Revenue and Profit Growth (2019-2023)')
    plt.xlabel('Year')
    plt.ylabel('Amount (in billions)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main Execution
if __name__ == "__main__":
    api_key = 'sk-OSuTSczpmWgk5X7xWecAfLlROHrJqfLxptDe4V5aXET3BlbkFJFRj_lx519-IlMf4fyx11dZXEVY0lMtGREdVgvFgQIA'  # Replace with your OpenAI API key

    # Step 1: Download the filings
    filing_directory = download_microsoft_filings()

    # Step 2: Select and clean the most recent 5 filings
    latest_filing_paths = get_latest_filings(filing_directory, num_filings=5)
    cleaned_texts = read_and_clean_filings(latest_filing_paths)

    # Step 3: Get insights from the cleaned text
    insights = get_insights(api_key, cleaned_texts)
    for idx, insight in enumerate(insights):
        print(f"Insight from 10-K filing {idx+1}:\n{insight}\n")

    # Step 4: Plot insights 
    years = ['2019', '2020', '2021', '2022', '2023']
    revenues = [125, 143, 168, 198, 211]  
    profits = [44, 51, 56, 61, 70]       
    
    plot_insights(years, revenues, profits)
