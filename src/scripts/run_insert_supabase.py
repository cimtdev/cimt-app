import os
from processing.insert_into_supabase import inserir_chunks

INPUT_PATH = "./saida_embeddings"

for nome_arquivo in os.listdir(INPUT_PATH):
    if not nome_arquivo.endswith(".json"):
        continue

    assunto = nome_arquivo.replace("_chunks.json", "").replace(".json", "")
    caminho = os.path.join(INPUT_PATH, nome_arquivo)
    inserir_chunks(caminho, assunto)
