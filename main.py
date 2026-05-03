import requests
from bs4 import BeautifulSoup
import random
import time
import csv
from twocaptcha import TwoCaptcha

class ScraperEngine:
    def solve_captcha_logic(self, html_content, url):
        # 2Captcha API Key (You need to get it from their website)
        solver = TwoCaptcha('YOUR_2CAPTCHA_API_KEY') 

        soup = BeautifulSoup(html_content, 'html.parser')
        # Find the ReCaptcha Site Key
        captcha_div = soup.find("div", class_="g-recaptcha")

        if captcha_div:
            site_key = captcha_div.get("data-sitekey")
            print(f"CAPTCHA detected! Site Key: {site_key}")

            try:
                # Request solution (It can take 1-2 minutes)
                result = solver.recaptcha(sitekey=site_key, url=url)
                return result['code']
            except Exception as e:
                print(f"CAPTCHA solving failed: {e}")
            
        return None
    def __init__(self, proxy_file):
        self.proxies = self._load_proxies(proxy_file)
        self.bad_proxies = set()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/13.1.2",
            "Mozilla/5.0 (X11; Linux x86_64) Firefox/110.0"
        ]

    def _load_proxies(self, file_path):
        try:
            with open(file_path, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("Warning: proxies.txt not found. Running without proxies.")
            return []

    def get_valid_proxy(self):
        active = [p for p in self.proxies if p not in self.bad_proxies]
        if not active:
            return None
        proxy = random.choice(active)
        return {"http": proxy, "https": proxy}

    def scrape(self, url):
        max_retries = 5
        for attempt in range(max_retries):
            proxy_dict = self.get_valid_proxy()
            headers = {"User-Agent": random.choice(self.user_agents)}
            
            # Display status
            current_p = list(proxy_dict.values())[0] if proxy_dict else "Local IP"
            print(f"Attempt {attempt+1}: Requesting with {current_p}")

            try:
                # Random Delay to mimic humans
                time.sleep(random.uniform(1, 3))
                
                response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10)

                if response.status_code == 200:
                    print("Success! Page fetched.")
                    return response.text
                
                if response.status_code in [403, 429]:
                    print(f"Blocked or Rate-limited (Status {response.status_code}).")
                    if proxy_dict: self.bad_proxies.add(current_p)
                    
            except Exception as e:
                print(f"Connection Error: {e}")
                if proxy_dict: self.bad_proxies.add(current_p)
                
        return None
    

def solve_captcha_logic(self, html_content, url):
    # 2Captcha API Key (You need to get it from their website)
    solver = TwoCaptcha('YOUR_2CAPTCHA_API_KEY') 
    
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find the ReCaptcha Site Key
    captcha_div = soup.find("div", class_="g-recaptcha")
    
    if captcha_div:
        site_key = captcha_div.get("data-sitekey")
        print(f"CAPTCHA detected! Site Key: {site_key}")
        
        try:
            # Request solution (It can take 1-2 minutes)
            result = solver.recaptcha(sitekey=site_key, url=url)
            return result['code']
        except Exception as e:
            print(f"CAPTCHA solving failed: {e}")
            
    return None
    
def parse_and_save(html):
    if not html:
        print("No content to parse.")
        return

    soup = BeautifulSoup(html, 'html.parser')
    results = []
    quotes = soup.find_all("div", class_="quote")

    for q in quotes:
        data = {
            "Quote": q.find("span", class_="text").text,
            "Author": q.find("small", class_="author").text
        }
        results.append(data)

    # Saving to CSV
    if results:
        with open('results.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Quote", "Author"])
            writer.writeheader()
            writer.writerows(results)
        print(f"Done! {len(results)} items saved to results.csv")

if __name__ == "__main__":
    target_url = "https://quotes.toscrape.com/"
    
    # Initialize Engine
    bot = ScraperEngine("proxies.txt")
    
    # Run Scraper
    page_html = bot.scrape(target_url)
    
    # Parse and Save
    parse_and_save(page_html)