# 🧠 Data Extraction and NLP Project

## 📌 Objective

The main objective of this project is to:

* **Extract article content** from a list of URLs provided in `Input.xlsx`.
* **Perform text analysis** on the extracted content to compute various linguistic and readability metrics.
* **Export results** into the required format specified in `Output Data Structure.xlsx`.

---

## 📥 Input

* **`Input.xlsx`**: Contains URLs and URL\_IDs to scrape.
* **Each article's content** will be saved as a `.txt` file named by its `URL_ID`.

---

## 🧾 Text Extraction

* Extract the **article title** and **main content** (excluding headers, footers, ads, or unrelated content).
* Use any Python web scraping library:

  * `BeautifulSoup`
  * `Selenium`
  * `Scrapy`
  * Or a combination of them
* Output one `.txt` file per article.

---

## 📊 Text Analysis

For each article text, compute the following 14 metrics:

| #  | Metric                 | Description                                         |
| -- | ---------------------- | --------------------------------------------------- |
| 1  | Positive Score         | Count of positive words                             |
| 2  | Negative Score         | Count of negative words                             |
| 3  | Polarity Score         | `(Positive - Negative) / (Positive + Negative + ε)` |
| 4  | Subjectivity Score     | `(Positive + Negative) / Total Words`               |
| 5  | Avg Sentence Length    | Average number of words per sentence                |
| 6  | % of Complex Words     | Percentage of words with more than 2 syllables      |
| 7  | Fog Index              | `0.4 * (Avg Sentence Length + % Complex Words)`     |
| 8  | Avg Words per Sentence | Similar to Avg Sentence Length                      |
| 9  | Complex Word Count     | Total count of complex words                        |
| 10 | Word Count             | Total words after preprocessing                     |
| 11 | Syllables per Word     | Average syllable count per word                     |
| 12 | Personal Pronouns      | Count of words like "I", "we", "my", etc.           |
| 13 | Avg Word Length        | Total characters / Total words                      |

> Definitions are derived from the `Text Analysis.docx`.

---

## 📤 Output

* **Output file format** must follow the structure in `Output Data Structure.xlsx`.
* Include:

  * All columns from `Input.xlsx`
  * All 14 computed metrics listed above

---

## 🛠 Tools & Libraries

* `pandas`
* `numpy`
* `nltk` / `spacy`
* `textblob`
* `re` (for regex)
* `beautifulsoup4` or `selenium` for scraping

---

## 🚀 How to Run

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Extract data from the URLs and perform Text Analysis and save output in **Text_Analysis_Output** Excel:

   ```bash
   python text_analysis.py
   ```

---

## 📂 Project Structure

```
├── Input.xlsx
├── Output Data Structure.xlsx
├── Text Analysis.docx
├── output_articles/
│   ├── Netclan20241017.txt
│   ├── Netclan20241018.txt
│   └── ...
├── MasterDictionary/
│   ├── negative-words.txt
│   ├── positive-words.txt
├── StopWords/
│   ├── StopWords_Auditor.txt
│   ├── StopWords_Currencies.txt
│   └── ...
├── text_analysis.py
├── README.md
├── Text_Analysis_Output.xlsx
└── requirements.txt
```

---
