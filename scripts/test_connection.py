import os
import requests
from dotenv import load_dotenv

# Charger les variables depuis le fichier .env
load_dotenv()

N8N_URL = os.getenv('N8N_URL')
N8N_API_KEY = os.getenv('N8N_API_KEY')

def test_connection():
    if not N8N_URL or not N8N_API_KEY:
        print("❌ Erreur : N8N_URL ou N8N_API_KEY n'est pas défini dans le fichier .env")
        return

    # Nettoyer l'URL
    url = N8N_URL.rstrip('/')
    api_url = f"{url}/api/v1/workflows"
    
    headers = {
        'X-N8N-API-KEY': N8N_API_KEY
    }

    print(f"Connexion à {api_url}...")
    
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('data', []))
            print(f"✅ Succès ! Connexion établie.")
            print(f"📊 Nombre de workflows trouvés : {count}")
            for wf in data.get('data', [])[:5]:
                print(f" - {wf['name']} (ID: {wf['id']})")
        else:
            print(f"❌ Échec : Code {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Erreur lors de la requête : {e}")

if __name__ == "__main__":
    test_connection()
