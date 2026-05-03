# Web_Scraper_with_Proxy_Rotation

A powerful and robust Python-based web scraper designed to extract data efficiently while bypassing common bot detection mechanisms. This project specifically scrapes quotes and authors from [quotes.toscrape.com](https://quotes.toscrape.com/) and saves them into a structured CSV format.

## 🚀 Features

* **HTML Parsing**: Uses `BeautifulSoup` for precise data extraction.
* **Proxy Rotation**: Automatically rotates through a list of proxies from `proxies.txt` to avoid IP blocking.
* **User-Agent Randomization**: Mimics different browsers (Chrome, Firefox, Safari) to stay undetected.
* **CAPTCHA Solving**: Integrated with `2Captcha` API to automatically solve Google ReCaptcha.
* **Error Handling**: Built-in retry mechanism for failed requests and connection errors.
* **Data Export**: Saves scraped data (Quotes & Authors) directly into a `results.csv` file.

## 🛠️ Requirements

Before running the project, ensure you have Python installed. You will need to install the following libraries:

```bash
pip install requests beautifulsoup4 twocaptcha
