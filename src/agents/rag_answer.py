import os
import openai
import json
from supabase import create_client
from dotenv import load_dotenv
from db.pg_connection import conectar_postgres

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
supabase = create_client("https://yignltxsqnbuvtobhtbw.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlpZ25sdHhzcW5idXZ0b2JodGJ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg2MDY3MjQsImV4cCI6MjA2NDE4MjcyNH0.JphhO_MXwaSuRHWat21nt3g73BnupsK4NAiTiqg5_TQ")
EMBEDDING_MODEL = "text-embedding-3-small"
GPT_MODEL = "gpt-3.5-turbo"  # ou "gpt-3.5-turbo" para reduzir custo

def gerar_embedding_pergunta(pergunta: str):
    resposta = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=pergunta
    )
    return resposta["data"][0]["embedding"]

def buscar_documentos_similares(vetor, k=5):
    conn = conectar_postgres()
    cur = conn.cursor()

    vetor_str = ",".join([str(x) for x in vetor])
    query = f"""
        SELECT assunto, timestamp, texto_chunk
        FROM document_chunks
        ORDER BY embedding <-> '[{vetor_str}]'::vector
        LIMIT {k};
    """

    cur.execute(query)
    resultados = cur.fetchall()
    cur.close()
    conn.close()

    docs = []
    for assunto, timestamp, texto_chunk in resultados:
        docs.append({
            "assunto": assunto,
            "timestamp": timestamp,
            "texto_chunk": texto_chunk
        })
    return docs

def montar_prompt(pergunta, documentos):
    contexto = "\n---\n".join(
        f"[{doc['assunto']} | {doc['timestamp']}]: {doc['texto_chunk']}" for doc in documentos
    )
    return f"""Você é um assistente especializado nos conteúdos do curso CIMT.

Baseando-se nos trechos abaixo, responda com linguagem clara, prática e objetiva. Se não souber, diga "não sei com base nos dados fornecidos".

Contexto:
{contexto}

Pergunta: {pergunta}
"""

def responder_pergunta(pergunta: str) -> str:
    vetor = gerar_embedding_pergunta(pergunta)
    docs = buscar_documentos_similares(vetor)
    prompt = montar_prompt(pergunta, docs)
    resposta = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "Você é um assistente da CIMT."},
            {"role": "user", "content": prompt}
        ]
    )
    return resposta.choices[0].message.content
