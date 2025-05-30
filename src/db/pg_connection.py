import os, psycopg2
from dotenv import load_dotenv

load_dotenv()

def conectar_postgres():
    return psycopg2.connect(
        host     = os.getenv("PGHOST"),      # db.<ref>.supabase.co
        port     = os.getenv("PGPORT", 5432),
        dbname   = os.getenv("PGDATABASE"),  # postgres
        user     = os.getenv("PGUSER"),      # postgres
        password = os.getenv("PGPASSWORD"),  # sua senha de DB
        sslmode  = "require"                 # ← obrigatório no Supabase
    )
