import os
import json
from src.processing.extracting_chunks import processar_pasta_assuntos

BASE_PATH = "./dados"
OUTPUT_PATH = "./saida_json"

def salvar_bloco_em_json(assuntos: dict):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    for assunto, blocos in assuntos.items():
        with open(os.path.join(OUTPUT_PATH, f"{assunto}.json"), "w", encoding="utf-8") as f:
            json.dump(blocos, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    assuntos = processar_pasta_assuntos(BASE_PATH)
    salvar_bloco_em_json(assuntos)
    print(f"✅ Extração concluída. JSONs salvos em {OUTPUT_PATH}/")
