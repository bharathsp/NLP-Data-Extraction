import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import shutil
import os
import re
import pandas as pd
import string
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
nltk.download('punkt')

# Load Excel file
input_df = pd.read_excel('Input.xlsx')

folder_path = 'output_articles'

# Delete the folder if it exists
if os.path.exists(folder_path):
    shutil.rmtree(folder_path)
    print(f"[DELETED] Folder '{folder_path}'")

# Create output folder if not exists
os.makedirs(folder_path)

# Function to extract title and article text from a given URL
def extract_article_text(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com"
        }

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"[ERROR] Failed to fetch URL: {url} | Status Code: {response.status_code}")
            return None, None

        soup = BeautifulSoup(response.content, 'html.parser')

        # Flexible title extraction
        if soup.find('h1', class_='tdb-title-text'):
            title = soup.find('h1', class_='tdb-title-text').get_text(strip=True)
        elif soup.find('h1'):
            title = soup.find('h1').get_text(strip=True)
        elif soup.title:
            title = soup.title.get_text(strip=True)
        else:
            strong = soup.find(['strong', 'b'])
            title = strong.get_text(strip=True) if strong else "No Title Found"

        # Article text
        content_div = soup.find('div', class_='td-post-content')
        paragraphs = content_div.find_all('p') if content_div else []
        article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])

        return title, article_text

    except Exception as e:
        print(f"[EXCEPTION] {url} - {e}")
        return None, None

# Load stop words from all files in StopWords/
def load_stopwords(folder):
    stopwords = set()
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    stopwords.add(line.strip().lower())
        except UnicodeDecodeError:
            # Retry with latin-1 encoding
            with open(path, 'r', encoding='latin-1') as f:
                for line in f:
                    stopwords.add(line.strip().lower())
    return stopwords

stop_words = load_stopwords('StopWords')


# Load master dictionary
def load_words(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return set(line.strip().lower() for line in file)
    except UnicodeDecodeError:
        # Try with fallback encoding (commonly used: latin-1)
        with open(filepath, 'r', encoding='latin-1') as file:
            return set(line.strip().lower() for line in file)


positive_words = load_words('MasterDictionary/positive-words.txt') - stop_words
negative_words = load_words('MasterDictionary/negative-words.txt') - stop_words

# Count syllables
def count_syllables(word):
    word = word.lower()
    vowels = "aeiou"
    count = 0
    if word.endswith(("es", "ed")):
        word = word[:-2]
    for idx, char in enumerate(word):
        if char in vowels and (idx == 0 or word[idx-1] not in vowels):
            count += 1
    return max(count, 1)

# Count complex words
def count_complex_words(words):
    return sum(1 for word in words if count_syllables(word) > 2)

# Clean and tokenize text
def clean_text(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    clean_words = [w for w in tokens if w not in stop_words]
    return clean_words

# Personal pronoun counter
def count_personal_pronouns(text):
    pronouns = re.findall(r'\b(I|we|my|ours|us)\b', text, re.I)
    return len([p for p in pronouns if p.lower() != 'us'])

# Analyze text
def analyze_text(article_text):
    sentences = sent_tokenize(article_text)
    words = clean_text(article_text)

    pos_score = sum(1 for word in words if word in positive_words)
    neg_score = sum(1 for word in words if word in negative_words)
    polarity = (pos_score - neg_score) / ((pos_score + neg_score) + 1e-6)
    subjectivity = (pos_score + neg_score) / (len(words) + 1e-6)

    avg_sent_len = len(words) / len(sentences) if sentences else 0
    complex_words = count_complex_words(words)
    percent_complex = complex_words / len(words) if words else 0
    fog_index = 0.4 * (avg_sent_len + percent_complex)
    avg_words_per_sent = avg_sent_len
    syllable_per_word = sum(count_syllables(word) for word in words) / len(words) if words else 0
    personal_pronouns = count_personal_pronouns(article_text)
    avg_word_len = sum(len(word) for word in words) / len(words) if words else 0

    return [
        pos_score, neg_score, polarity, subjectivity,
        avg_sent_len, percent_complex, fog_index, avg_words_per_sent,
        complex_words, len(words), syllable_per_word, personal_pronouns,
        avg_word_len
    ]


# Loop through each row and extract text
for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    title, article = extract_article_text(url)

    if title and article:
        output_path = os.path.join('output_articles', f"{url_id}.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(title + "\n\n" + article)
        print(f"[SUCCESS] Saved: {output_path}")
    else:
        print(f"[FAILED] Skipped: {url_id}")

# Final output
output = []

for _, row in input_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    file_path = os.path.join('output_articles', f"{url_id}.txt")

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            full_text = f.read()
        article_data = analyze_text(full_text)
        output.append([url_id, url] + article_data)
    else:
        print(f"[Missing] {file_path}")
        output.append([url_id, url] + [None]*13)

# Output to Excel
columns = [
    'URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
    'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
    'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
    'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'
]

output_df = pd.DataFrame(output, columns=columns)
output_df.to_excel("Text_Analysis_Output.xlsx", index=False)
print("[✓] Text analysis complete. Output saved to Text_Analysis_Output.xlsx.")
