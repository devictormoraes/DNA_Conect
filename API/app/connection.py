import fdb
from app import config

def get_connection():
    try:
        conn = fdb.connect(
            host=config.DB_HOST,
            port=int(config.DB_PORT),
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Erro na conexão com o banco: {e}")
        return None
