import os
import json
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def inserir_chunks(arquivo_json: str, assunto: str):
    with open(arquivo_json, "r", encoding="utf-8") as f:
        dados = json.load(f)

    registros = []
    for item in dados:
        registros.append({
            "assunto": assunto,
            "timestamp": f"{item['timestamp_inicio']} - {item['timestamp_fim']}",
            "texto_chunk": item["texto_chunk"],
            "embedding": item["embedding"]
        })

    # Envia em lotes de 100
    for i in range(0, len(registros), 100):
        batch = registros[i:i+100]
        response = supabase.table("document_chunks").insert(batch).execute()
        print(f"🚀 Inseridos {len(batch)} registros para {assunto}")
