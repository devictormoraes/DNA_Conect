from app.connection import get_connection

if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("Conexão estabelecida com sucesso!")
        conn.close()
    else:
        print("Falha na conexão.")
