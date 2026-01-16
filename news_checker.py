import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter
import re
import datetime
import matplotlib.pyplot as plt

def check_news():
    url = "https://www.nytimes.com"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"❌ Erreur d'accès : {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        found_titles = []
        #we take all the headlines 
        containers = soup.find_all(['h3', 'h2', 'p'], class_=re.compile("indicate-hover|summary-class|headline"))
        #if not headlines we just take all the line in h2/h3
        if not containers:
            containers = soup.find_all(['h3', 'h2'])

        for item in containers:
            text = item.get_text(strip=True)
            if 20 < len(text) < 150 and text not in found_titles:
                found_titles.append(text)
        
        if not found_titles:
            print("⚠️ No Headlines found.")
            return

        #Here saving and analysing data
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        df = pd.DataFrame(found_titles, columns=["Title"])
        df.to_csv(f"nyt_titles_{today}.csv", index=False)
        #here we look after words most repeated of the day without any of the most common words in english language
        words = re.findall(r'\b[a-z]{4,}\b', " ".join(found_titles).lower())
        stop_words = {'with', 'from', 'that', 'this', 'their', 'they', 'have', 'about', 'says', 'after', 'will'}
        filtered = []
        for w in words:
            if w not in stop_words:
                filtered.append(w)
        
        data = Counter(filtered).most_common(10)
        words_list = [x[0] for x in data]
        counts_list = [x[1] for x in data]

        plt.figure(figsize=(10, 6))
        plt.bar(words_list, counts_list, color='skyblue')
        plt.title(f"Top Trending Words on NYT - {datetime.datetime.now().strftime('%Y-%m-%d')}")
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig(f"{today}.png")
        
        print(f"✅ {len(found_titles)} titles found !")
        print(f"📊 Word of the day : {Counter(filtered).most_common(1)[0][0].upper()}")

    except Exception as e:
        print(f"❌ Error : {e}")

if __name__ == "__main__":
    check_news()