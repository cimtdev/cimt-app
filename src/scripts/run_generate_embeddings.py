import os
import json
from processing.generate_embeddings import gerar_embeddings

INPUT_PATH = "./saida_chunks"
OUTPUT_PATH = "./saida_embeddings"

os.makedirs(OUTPUT_PATH, exist_ok=True)

for nome_arquivo in os.listdir(INPUT_PATH):
    if not nome_arquivo.endswith(".json"):
        continue

    caminho_entrada = os.path.join(INPUT_PATH, nome_arquivo)
    with open(caminho_entrada, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    resultado = gerar_embeddings(chunks)

    caminho_saida = os.path.join(OUTPUT_PATH, nome_arquivo)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    print(f"✅ Embeddings gerados: {nome_arquivo} -> {len(resultado)} chunks")
