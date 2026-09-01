import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def estrai_tempo_reale_asf():
    try:
        # INCOLLA QUI L'URL DELLA TUA FERMATA TROVATO SU MOOVIT
        url = "INCOLLA_QUI_L_URL_DI_MOOVIT_DELLA_TUA_FERMATA"
        
        # Fingiamo di essere un browser normale per evitare blocchi
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Cerca l'elemento grafico di Moovit che contiene il tempo reale del primo bus in arrivo
        # (La classe 'live-time' o simile identifica il countdown testuale)
        elemento_tempo = soup.find('div', class_='next-arrival-time') or soup.find('span', class_='live-time')
        
        if elemento_tempo:
            return elemento_tempo.text.strip()
        else:
            return "In orario (Vedi tabella)"
            
    except Exception as e:
        return "Non disponibile (GPS offline)"

def main():
    tempo_reale = estrai_tempo_reale_asf()
    
    dati_bus = {
        "linea": "C145",
        "aggiornato_alle": datetime.now().strftime("%H:%M"),
        "stato_realtime": tempo_reale
    }
    
    os.makedirs("output", exist_ok=True)
    with open("output/realtime.json", "w") as f:
        json.dump(dati_bus, f, indent=2)

if __name__ == "__main__":
    main()
  
