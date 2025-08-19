# connection.py
import fdb
import config


def get_connection():
    try:
        conn = fdb.connect(
            host=config.DB_HOST,
            port=int(config.DB_PORT),
            database=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            charset='UTF8'
        )
        print("✅ Conexão com Firebird estabelecida com sucesso!")
        return conn
    except Exception as e:
        print("❌ Erro ao conectar ao banco:", e)
        return None
