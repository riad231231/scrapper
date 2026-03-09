import os
import requests
import json
import sys
from dotenv import load_dotenv

load_dotenv()

N8N_URL = os.getenv('N8N_URL')
N8N_API_KEY = os.getenv('N8N_API_KEY')

def export_workflow(workflow_id):
    if not N8N_URL or not N8N_API_KEY:
        print("❌ Erreur : Configuration manquante dans le .env")
        return

    url = f"{N8N_URL.rstrip('/')}/api/v1/workflows/{workflow_id}"
    headers = {'X-N8N-API-KEY': N8N_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            workflow_data = response.json()
            
            # Créer le dossier exports s'il n'existe pas
            os.makedirs('exports', exist_ok=True)
            
            filename = f"exports/{workflow_data['name'].replace(' ', '_')}_{workflow_id}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(workflow_data, f, indent=4, ensure_ascii=False)
            
            print(f"✅ Workflow '{workflow_data['name']}' exporté avec succès dans : {filename}")
            return filename
        else:
            print(f"❌ Échec de l'export (Code {response.status_code})")
            print(response.text)
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/export_workflow.py <workflow_id>")
    else:
        export_workflow(sys.argv[1])
