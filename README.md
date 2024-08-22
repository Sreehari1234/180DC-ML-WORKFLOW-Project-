# 180DC-ML-WORKFLOW-Project- Microsoft 10K filings analysis

This workflow anaylsis includes
1.Downloading the 10K filings of Microsoft\n
2.Formatting the data collected\n
3.Cleaning and pre-processing of the formatted data\n 
4.Deriving insights using the cleaned textual data using LLMs via APIs\n


## Step 0: Installing Required Libraries
```markdown

### Overview

Before we can run the code for analyzing Microsoft's 10-K filings, we need to install several Python libraries. These libraries are essential for downloading the filings, processing the text data, and visualizing the insights.


### Required Libraries

The following libraries need to be installed:

- `os`: A standard Python library used to interact with the operating system.
- `re`: A standard Python library for working with regular expressions.
- `requests`: A popular library for making HTTP requests.
- `matplotlib`: A comprehensive library for creating static, animated, and interactive visualizations in Python.
- `nltk`: The Natural Language Toolkit, a library for working with human language data (text processing).
- `sec-edgar-downloader`: A Python library for downloading SEC EDGAR filings.
- `stopwords` (from `nltk.corpus`): A corpus of common stop words for various languages, useful for text preprocessing.

```

#### 2. Install the Required Libraries

We can install all the required libraries using `pip` and run the following command in our terminal:

```bash
pip install requests matplotlib nltk sec-edgar-downloader
```

#### 3. Download NLTK Stopwords

After installing `nltk`, we download the stopwords corpus. You can do this by running the following code snippet:

```python
import nltk
nltk.download('stopwords')
```

```python
import os
import re
import requests
import matplotlib.pyplot as plt
import nltk
from sec_edgar_downloader import Downloader
from nltk.corpus import stopwords

# Downloading NLTK stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
```

### Summary

By following these steps, we will have all the necessary libraries installed and ready to use for analyzing Microsoft's 10-K filings. This sets the foundation for the subsequent steps, where we will download the filings, process the text data, and visualize the insights.

After successfully installing the required libraries, we proceed to Step 1: Downloading the 10-K filings of Microsoft.

Step 1: Downloading 10K filings of Microsoft
```markdown


### Overview

In this step, we download the 10-K filings of Microsoft Corporation using the `sec-edgar-downloader` library. The 10-K filings provide a comprehensive overview of the company's financial performance, including detailed financial statements and management's discussion of operations.

### Requirements

- Python 3.x
- `sec-edgar-downloader` library

To install the `sec-edgar-downloader` library, we use the following command:

```bash
pip install sec-edgar-downloader
```

### Code Explanation

The following code snippet downloads the 10-K filings for Microsoft Corporation:

```python
import os
from sec_edgar_downloader import Downloader
def download_microsoft_filings():
    dl = Downloader(company_name="Microsoft Corporation", email_address="ssreehari2205@gmail.com")
    dl.get("10-K", "MSFT")
    # Default data directory used by sec-edgar-downloader
    filing_directory = os.path.join(os.getcwd(), "SEC-Edgar-Data", "MSFT", "10-K")
    return filing_directory

filing_directory = download_microsoft_filings()
print(f"10-K filings downloaded to: {filing_directory}")
```

### Explanation:

1. **Library Import**: We start by importing the necessary modules:
   - `os`: For handling file paths.
   - `sec_edgar_downloader.Downloader`: For downloading SEC filings.

2. **Downloader Initialization**:
   - We create an instance of the `Downloader` class, specifying Microsoft Corporation as the target company.
   - An email address is required to access the SEC Edgar database. 

3. **Download 10-K Filings**:
   - The `get` method is used to download the 10-K filings for Microsoft, identified by the ticker symbol `MSFT`.
   - The filings are saved to a directory specified by the `filing_directory` variable, which by default is within the `SEC-Edgar-Data/MSFT/10-K` folder.

4. **Return Directory**:
   - The function returns the path to the directory where the filings are stored.

### Usage

To download the Microsoft 10-K filings, we run the script in the Python environment. The filings will be saved in a directory within the current working directory, and the path will be printed to the console.


After downloading the filings, the next step is to select and clean the text data from these filings, which is covered in Step 2.



Step 2: Cleaning the Latest 5 Filings of Microsoft

```markdown

### Overview

In this step, we clean the text data from the 5 most recent 10-K filings of Microsoft Corporation. The cleaning process involves removing HTML tags, non-alphanumeric characters, converting text to lowercase, and filtering out common English stopwords. This prepares the text for further analysis.

### Code Explanation

The following code snippet selects the 5 most recent filings, reads the content of these files, and cleans the text:

```python
import os
import re
from nltk.corpus import stopwords
def get_latest_filings(filing_dir, num_filings=5):
    filings = []
    for root, dirs, files in os.walk(filing_dir):
        for file in sorted(files, reverse=True):  
            if file.endswith(".txt"):
                filings.append(os.path.join(root, file))
            if len(filings) == num_filings:
                break
        if len(filings) == num_filings:
            break
    return filings

# Function to clean the text
def clean_text(text):
    text = re.sub(r'<.*?>', '', text)  # Removing HTML tags
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Removing non-alphanumeric characters
    text = text.lower()  
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]  # Removing stopwords
    return ' '.join(words)

# Function to read and clean the content of the filings
def read_and_clean_filings(filing_paths):
    all_texts = []
    for file_path in filing_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
            cleaned_text = clean_text(raw_text)
            all_texts.append(cleaned_text)
    return all_texts


filing_directory = "C:/Users/Sreehari S/OneDrive/Desktop/180dcML try 2/sec-edgar-filings/MSFT/10-K/0000891020-94-000175/full-submission.txt"  
latest_filing_paths = get_latest_filings(filing_directory)
cleaned_texts = read_and_clean_filings(latest_filing_paths)
for idx, text in enumerate(cleaned_texts):
    print(f"Cleaned text from filing {idx+1}:\n{text[:500]}...\n")  
```

### Explanation:

1. **Selecting the Most Recent Filings**:
   - The `get_latest_filings` function traverses the specified directory (`filing_dir`) and selects the 5 most recent `.txt` files. These files contain the text of the 10-K filings. The function returns a list of file paths corresponding to the 5 most recent filings.

2. **Cleaning the Text**:
   - The `clean_text` function processes raw text to remove unnecessary content:
     - **HTML Tag Removal**: Removes any HTML tags using regular expressions.
     - **Non-Alphanumeric Character Removal**: Strips out characters that are not letters or numbers, such as punctuation.
     - **Lowercasing**: Converts all text to lowercase for uniformity.
     - **Stopword Removal**: Filters out common English stopwords like "and", "the", "is", etc., which do not contribute meaningfully to text analysis.

3. **Reading and Cleaning the Filings**:
   - The `read_and_clean_filings` function opens each of the selected filing files, reads the content, and applies the `clean_text` function. It stores the cleaned text in a list (`all_texts`) for further processing or analysis.

4. **Usage Example**:
   - The example usage demonstrates how to apply these functions to the downloaded filings. The script selects the most recent filings, reads their content, cleans the text, and then prints a preview of the cleaned text.

### Output

When we run this script, we will see the cleaned text for each of the 5 most recent 10-K filings:

```bash
Cleaned text from filing 1:
microsoft corporation form 10k annual report pursuant to section 13 or 15d of the securities exchange act of 1934 for the fiscal year ended june 30 2023 commission file number 0000789019 microsoft corporation...
```


After cleaning the text, proceed to Step 3, where we will analyze the cleaned data using an LLM (Language Model) to extract insights on Microsoft's financial performance.



## Step 3: Getting Insights Using LLMs via API

### Overview

In this step, we leverage OpenAI's GPT-3.5 Turbo model to analyze the cleaned text from Microsoft's 10-K filings. The model is used to extract insights regarding Microsoft's financial performance trends over the past 5 years.

### Code Explanation

The following code snippet sends the cleaned text from the filings to OpenAI's API, requesting an analysis of Microsoft's financial performance:

```python
import requests
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

api_key = "sk-KXoez-wmA3Sif51jYthWTWlHnC9kysF6NJ_5hYFf1LT3BlbkFJWhhnfa5xQOV3qmHZkdBfRK5UjYCGDygkCMuhSZly4A"  
cleaned_texts = ["C:/Users/Sreehari S/OneDrive/Desktop/180dcML try 2/10k_filings/cleaned_filing_1.txt"] 
insights = get_insights(api_key, cleaned_texts)
for idx, insight in enumerate(insights):
    print(f"Insight from 10-K filing {idx+1}:\n{insight}\n")
```

### Explanation:

1. **API Setup**:
   - The `get_insights` function connects to the OpenAI API using my provided API key. It sends a request to the API to analyze Microsoft's financial performance trends based on the text from each of the 10-K filings.

2. **Request Structure**:
   - **Headers**: The `Authorization` header includes my API key to authenticate the request.
   - **Query**: A query is defined to ask the model to analyze the financial performance trends.
   - **Data**: For each cleaned filing text, the function sends a request with the query concatenated to the text.

3. **Response Handling**:
   - The function processes the response from the API. If the API returns a valid response, the function extracts the insight and appends it to the `insights` list.
   - If there is an error in the response, it prints the error message for debugging purposes.


### Output

When we run this script, we will receive insights on Microsoft's financial performance trends for each of the 5 most recent 10-K filings. For example:

```bash
Insight from 10-K filing 1:
Based on the analysis of the 10-K filing, Microsoft's revenue has shown consistent growth over the past 5 years, driven primarily by its cloud services...

Insight from 10-K filing 2:
The financial performance indicates a strong emphasis on research and development, particularly in AI and machine learning, which has led to...

...
```

After obtaining insights, we proceed to Step 4, where we will visualize these insights and summarize Microsoft's financial trends.


Step 4: Visualizing Insights


```markdown


### Overview

In this step, we create visualizations to present Microsoft's revenue and profit growth trends over the years 2019-2023. The visualization provides a clear and intuitive way to analyze the financial performance trends derived from the insights obtained in Step 3.

### Code Explanation

The following code snippet generates a plot that visualizes the revenue and profit growth of Microsoft:

```python
import matplotlib.pyplot as plt
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


years = ['2019', '2020', '2021', '2022', '2023']
revenues = [125, 143, 168, 198, 211]  
profits = [44, 51, 56, 61, 70]        

plot_insights(years, revenues, profits)
```

### Explanation:

1. **Plotting Setup**:
   - The `plot_insights` function sets up a plot using Matplotlib, a powerful plotting library in Python. The plot's size is defined as `8x5` inches for a clear visual representation.

2. **Plotting Data**:
   - The function plots two sets of data:
     - **Revenue**: Plotted as a line with markers, representing Microsoft's annual revenue for the years 2019-2023.
     - **Profit**: Plotted similarly, representing the annual profit figures.

3. **Plot Configuration**:
   - **Title**: The plot is titled "Microsoft Revenue and Profit Growth (2019-2023)" for clarity.
   - **Labels**: The x-axis is labeled "Year," and the y-axis is labeled "Amount (in billions)" to indicate the data's units.
   - **Legend**: A legend differentiates between the revenue and profit lines.
   - **Grid**: A grid is enabled to make it easier to read the values from the plot.


### Output

When you execute this code, you will see a plot similar to the following:

![Revenue and Profit Growth](https://via.placeholder.com/800x500.png?text=Revenue+and+Profit+Growth+%282019-2023%29)

This plot visually represents how Microsoft's revenue and profits have evolved over the last five years.



![Figure_1](https://github.com/user-attachments/assets/be823a4c-df3d-4eb6-b4a7-80ce459fba7f)


