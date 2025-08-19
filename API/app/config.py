import fdb

# Configurações de conexão com o banco Firebird
DB_CONFIG = {
    "host": "localhost",               # IP ou nome do servidor do Firebird
    "database": "C:/caminho/ERP.FDB",  # Caminho completo do arquivo FDB
    "user": "SYSDBA",                  # Usuário do Firebird
    "password": "masterkey"            # Senha do Firebird
}


def get_connection():
    """Retorna uma nova conexão com o banco Firebird"""
    return fdb.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )
