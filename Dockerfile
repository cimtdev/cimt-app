FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
# (Adicione outros arquivos essenciais, se houver, como README.md, setup scripts, etc.)

EXPOSE 8501

CMD ["streamlit", "run", "src/app/chat_rag.py"]