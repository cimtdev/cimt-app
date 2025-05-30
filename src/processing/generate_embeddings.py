import os
import json
import openai
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = "text-embedding-3-small"

def gerar_embeddings(chunks: List[Dict[str, str]], batch_size: int = 100) -> List[Dict[str, str]]:
    from tqdm import tqdm
    resultado = []
    textos = [chunk.get("conteudo") or chunk.get("texto_chunk") or "" for chunk in chunks]
    total = len(textos)
    for i in tqdm(range(0, total, batch_size), desc="Gerando embeddings", unit="batch"):
        batch = textos[i:i+batch_size]
        try:
            resposta = openai.embeddings.create(
                model=EMBEDDING_MODEL,
                input=batch
            )
            embeddings = [item.embedding for item in resposta.data]
        except Exception as e:
            print(f"Erro no batch {i//batch_size+1}: {e}")
            embeddings = [None]*len(batch)
        for idx, chunk in enumerate(chunks[i:i+batch_size]):
            chunk_com_embedding = {
                **chunk,
                "embedding": embeddings[idx]
            }
            resultado.append(chunk_com_embedding)
    return resultado
