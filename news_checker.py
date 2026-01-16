import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter
import re
import datetime
import os 

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
        
        # Le NYT place ses titres dans des balises 'p', 'h3' ou 'span' avec des classes spécifiques
        # On va chercher tous les textes à l'intérieur des liens d'articles
        found_titles = []
        
        # On cible les conteneurs de titres les plus fréquents au NYT
        containers = soup.find_all(['h3', 'h2', 'p'], class_=re.compile("indicate-hover|summary-class|headline"))
        
        if not containers:
            # Plan B : On prend toutes les balises h3 et h2 sans distinction si le plan A échoue
            containers = soup.find_all(['h3', 'h2'])

        for item in containers:
            text = item.get_text(strip=True)
            # Un titre fait généralement entre 20 et 150 caractères
            if 20 < len(text) < 150 and text not in found_titles:
                found_titles.append(text)
        
        if not found_titles:
            print("⚠️ Toujours rien. Le NYT bloque peut-être les requêtes directes.")
            return

        # --- SAUVEGARDE ET ANALYSE ---
        df = pd.DataFrame(found_titles, columns=["Title"])
        df.to_csv(f"nyt_titles_{datetime.datetime.now().strftime('%Y-%m-%d')}.csv", index=False)
        
        words = re.findall(r'\b[a-z]{4,}\b', " ".join(found_titles).lower())
        stop_words = {'with', 'from', 'that', 'this', 'their', 'they', 'have', 'about', 'says', 'after', 'will'}
        filtered = [w for w in words if w not in stop_words]
        
        print(f"✅ {len(found_titles)} titres extraits !")
        print(f"📊 Top mot : {Counter(filtered).most_common(1)[0][0].upper()}")

    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    print("--- Démarrage du Monitoring ---")
    check_news()