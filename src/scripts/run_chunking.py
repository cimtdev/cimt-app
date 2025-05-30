import os
import json
from processing.chunk_by_tokens import chunk_blocos

INPUT_PATH = "./saida_json"
OUTPUT_PATH = "./saida_chunks"

def processar_chunks():
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    for nome_arquivo in os.listdir(INPUT_PATH):
        if not nome_arquivo.endswith(".json"):
            continue

        assunto = nome_arquivo.replace(".json", "")
        caminho_entrada = os.path.join(INPUT_PATH, nome_arquivo)

        with open(caminho_entrada, "r", encoding="utf-8") as f:
            blocos = json.load(f)

        chunks = chunk_blocos(blocos, max_tokens=200)

        caminho_saida = os.path.join(OUTPUT_PATH, f"{assunto}_chunks.json")
        with open(caminho_saida, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)

        print(f"✅ {assunto}: {len(chunks)} chunks salvos em {caminho_saida}")

if __name__ == "__main__":
    processar_chunks()
