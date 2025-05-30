import tiktoken
from typing import List, Dict

def chunk_blocos(blocos: List[Dict[str, str]], max_tokens: int = 200) -> List[Dict[str, str]]:
    enc = tiktoken.get_encoding("cl100k_base")
    chunks = []
    buffer = []
    total_tokens = 0
    timestamp_inicio = None

    for bloco in blocos:
        tokens = len(enc.encode(bloco["conteudo"]))
        if total_tokens + tokens > max_tokens:
            if buffer:
                texto_chunk = " ".join([b["conteudo"] for b in buffer])
                chunks.append({
                    "texto_chunk": texto_chunk,
                    "timestamp_inicio": timestamp_inicio,
                    "timestamp_fim": buffer[-1]["timestamp_fim"],
                    "origem_arquivo": buffer[-1]["arquivo"]
                })
            buffer = [bloco]
            total_tokens = tokens
            timestamp_inicio = bloco["timestamp_inicio"]
        else:
            if not buffer:
                timestamp_inicio = bloco["timestamp_inicio"]
            buffer.append(bloco)
            total_tokens += tokens

    if buffer:
        texto_chunk = " ".join([b["conteudo"] for b in buffer])
        chunks.append({
            "texto_chunk": texto_chunk,
            "timestamp_inicio": timestamp_inicio,
            "timestamp_fim": buffer[-1]["timestamp_fim"],
            "origem_arquivo": buffer[-1]["arquivo"]
        })

    return chunks
