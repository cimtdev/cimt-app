from db.pg_connection import conectar_postgres
import traceback

try:
    conn = conectar_postgres()
    print("✅ Conectado!", conn.get_dsn_parameters()["host"])
    conn.close()
except Exception as e:
    print("❌ Falhou na conexão:")
    traceback.print_exc()