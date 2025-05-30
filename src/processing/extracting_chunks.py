import os
import re
from docling.document_converter import DocumentConverter
from tqdm import tqdm
from typing import List, Dict

def extrair_blocos_transcricao(texto: str) -> List[Dict[str, str]]:
    padrao = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\n(.*?)(?=\n\d{2}:\d{2}:\d{2}\.\d{3} -->|\Z)', re.DOTALL)
    blocos = []
    for match in padrao.finditer(texto):
        inicio = match.group(1)
        fim = match.group(2)
        conteudo = match.group(3).replace("\n", " ").strip()
        blocos.append({
            "timestamp_inicio": inicio,
            "timestamp_fim": fim,
            "conteudo": conteudo
        })
    return blocos

def processar_pasta_assuntos(base_path: str) -> Dict[str, List[Dict[str, str]]]:
    assuntos = {}
    pastas = [p for p in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, p))]
    print(f"Encontradas {len(pastas)} pastas para processar.")
    for idx_pasta, pasta in enumerate(pastas, 1):
        pasta_path = os.path.join(base_path, pasta)
        print(f"\n[{idx_pasta}/{len(pastas)}] Processando pasta: {pasta}")
        blocos_por_pdf = []
        arquivos_txt = [a for a in os.listdir(pasta_path) if a.lower().endswith('.txt')]
        total_txt = len(arquivos_txt)
        print(f"  {total_txt} arquivos .txt encontrados.")
        for idx_txt, arquivo in enumerate(tqdm(arquivos_txt, desc=f"  Arquivos .txt em {pasta}", unit="txt"), 1):
            caminho_arquivo = os.path.join(pasta_path, arquivo)
            print(f"    Processando arquivo {idx_txt}/{total_txt}: {arquivo}")
            try:
                with open(caminho_arquivo, "r", encoding="utf-8") as f:
                    texto = f.read()
            except Exception as e:
                print(f"[ERRO] Falha ao ler arquivo txt '{arquivo}': {e}")
                texto = ""
            # Debug: mostrar amostra do texto extraído
            if not texto:
                print(f"[AVISO] Nenhum texto extraído do arquivo '{arquivo}'. Pode estar vazio ou houve erro de leitura.")
            else:
                print(f"[DEBUG] Primeiros 200 caracteres extraídos de '{arquivo}':\n{texto[:200]}\n{'-'*60}")
            blocos = extrair_blocos_transcricao(texto)
            if not blocos:
                print(f"[AVISO] Nenhum bloco encontrado após aplicar a regex em '{arquivo}'.")
            for b in blocos:
                b["arquivo"] = arquivo
            blocos_por_pdf.extend(blocos)
        print(f"  Finalizado: {total_txt} arquivos .txt processados na pasta '{pasta}'.")
        assuntos[pasta] = blocos_por_pdf
    return assuntos
