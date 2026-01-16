import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter
import re
import datetime

def check_news():
    url = "https://www.nytimes.com/international/" 
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = soup.find_all('p') 
        
        if os.path.exists("history.txt"):
            with open("history.txt", "r", encoding="utf-8") as f:
                history = f.read().splitlines()
        else:
            history = []

        new_count = 0
        with open("history.txt", "a", encoding="utf-8") as f:
            for art in articles:
                title = art.get_text(strip=True)
                
                if title not in history and len(title) > 5:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    f.write(f"{title}\n")
                    print(f"🆕 Nouveau titre trouvé : {title}")
                    new_count += 1
        
        if new_count == 0:
            print("😴 Rien de neuf depuis la dernière vérification.")
        else:
            print(f"✅ {new_count} nouveaux articles ajoutés à l'historique.")

    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    print("--- Démarrage du Monitoring ---")
    check_news()