"""
Debug script : découvrir les endpoints disponibles et corriger le workflow.
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

N8N_URL = os.getenv('N8N_URL').rstrip('/')
N8N_API_KEY = os.getenv('N8N_API_KEY')
HEADERS = {'X-N8N-API-KEY': N8N_API_KEY, 'Content-Type': 'application/json'}
WORKFLOW_ID = "uEfbG8gUKQoBPU4S"


def step1_get_and_fix():
    """Récupère, fixe et pousse le workflow."""
    print("📥 Récupération du workflow...")
    resp = requests.get(f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}", headers=HEADERS)
    resp.raise_for_status()
    wf = resp.json()
    print(f"  OK: '{wf['name']}' v{wf.get('versionCounter','?')}")
    
    # Appliquer les fix
    print("\n🔧 Application des corrections...")
    for node in wf['nodes']:
        if node['name'] == 'Message a model':
            vals = node.get('parameters', {}).get('responses', {}).get('values', [])
            if vals:
                c = vals[0].get('content', '')
                c = c.replace(
                    '{{ $item(0).$node["HTTP Request"].json.data[0].about.name }}',
                    '{{ $node["Split Out"].json.name }}'
                ).replace(
                    '{{ $node["HTTP Request"].json["name"] }}',
                    '{{ $node["Split Out"].json.name }}'
                )
                vals[0]['content'] = c
                print("  ✅ FIX 1: Prompt OpenAI")
            node['onError'] = 'continueErrorOutput'

        if node['name'] == 'Create a draft':
            opts = node.get('parameters', {}).get('options', {})
            if 'sendTo' in opts:
                opts['sendTo'] = '={{ $node["Remove Duplicates"].json.data[0].emails[0].value }}'
                print("  ✅ FIX 2: sendTo Gmail")

    # Construire un payload clean
    # Seuls les champs acceptés par l'API PUT de n8n
    clean_settings = {"executionOrder": wf.get("settings", {}).get("executionOrder", "v1")}
    
    payload = {
        "name": wf["name"],
        "nodes": wf["nodes"],
        "connections": wf["connections"],
        "settings": clean_settings,
    }

    print("\n📤 Push vers n8n...")
    resp = requests.put(
        f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}",
        headers=HEADERS,
        json=payload
    )
    print(f"  PUT status: {resp.status_code}")
    if not resp.ok:
        print(f"  Détails: {resp.text[:500]}")
    else:
        print(f"  ✅ Workflow mis à jour !")
    return resp.ok


def step2_check_api_capabilities():
    """Explore les endpoints disponibles pour déclencher le workflow."""
    print("\n🔍 Test des endpoints de déclenchement...\n")
    
    # Test 1: GET executions (pour voir si l'endpoint existe)
    endpoints = [
        ("GET", f"{N8N_URL}/api/v1/executions?workflowId={WORKFLOW_ID}&limit=3"),
        ("POST", f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}/activate"),
        ("PATCH", f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}/activate"),
    ]
    
    for method, url in endpoints:
        try:
            if method == "GET":
                r = requests.get(url, headers=HEADERS)
            elif method == "POST":
                r = requests.post(url, headers=HEADERS, json={})
            elif method == "PATCH":
                r = requests.patch(url, headers=HEADERS, json={})
            print(f"  {method} {url.replace(N8N_URL, '')} → {r.status_code}")
            if r.ok:
                data = r.json()
                if isinstance(data, dict) and 'data' in data:
                    items = data['data']
                    if isinstance(items, list):
                        for item in items[:3]:
                            if isinstance(item, dict):
                                print(f"    - {json.dumps({k: item[k] for k in list(item.keys())[:4]}, default=str)}")
        except Exception as e:
            print(f"  {method} ... → Erreur: {e}")


def step3_trigger_via_webhook():
    """Tente le déclenchement via webhook de production."""
    print("\n🚀 Tentative de déclenchement via webhook...")
    
    # Le workflow a un schedule trigger + manual trigger
    # Pour déclencher manuellement, on peut utiliser le webhook de test
    # ou l'API d'activation/désactivation
    
    # Essayons POST /api/v1/workflows/{id}/run (n8n 1.x+)
    tests = [
        ("POST", f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}/run", {}),
        ("POST", f"{N8N_URL}/api/v1/executions/run", {"workflowId": WORKFLOW_ID}),
    ]
    
    for method, url, body in tests:
        try:
            r = requests.post(url, headers=HEADERS, json=body)
            print(f"  POST {url.replace(N8N_URL, '')} → {r.status_code}")
            if r.ok:
                print(f"    ✅ {r.text[:300]}")
                return True
            else:
                print(f"    {r.text[:200]}")
        except Exception as e:
            print(f"  → Erreur: {e}")
    
    return False


if __name__ == "__main__":
    print("=" * 60)
    print("🔧 DEBUG & FIX - Scrap domaines")
    print("=" * 60)
    
    ok = step1_get_and_fix()
    step2_check_api_capabilities()
    step3_trigger_via_webhook()
    
    print("\n" + "=" * 60)
