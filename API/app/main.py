from fastapi import FastAPI, HTTPException
from db import get_connection
from models import Produto, Cliente, Pedido

app = FastAPI(title="ERP Sync API", version="1.0")

# ----------------------
# PRODUTOS
# ----------------------
@app.get("/produtos", response_model=list[Produto])
def listar_produtos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID, NOME, PRECO FROM PRODUTOS ROWS 50")
    produtos = [
        {"id": row[0], "nome": row[1], "preco": float(row[2])}
        for row in cur.fetchall()
    ]
    conn.close()
    return produtos


# ----------------------
# CLIENTES
# ----------------------
@app.get("/clientes", response_model=list[Cliente])
def listar_clientes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID, NOME, DOCUMENTO FROM CLIENTES ROWS 50")
    clientes = [
        {"id": row[0], "nome": row[1], "documento": row[2]}
        for row in cur.fetchall()
    ]
    conn.close()
    return clientes


@app.post("/clientes")
def cadastrar_cliente(cliente: Cliente):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO CLIENTES (ID, NOME, DOCUMENTO) VALUES (?, ?, ?)",
        (cliente.id, cliente.nome, cliente.documento)
    )
    conn.commit()
    conn.close()
    return {"status": "ok", "mensagem": "Cliente cadastrado com sucesso"}


@app.put("/clientes/{id}")
def alterar_cliente(id: int, cliente: Cliente):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE CLIENTES SET NOME = ?, DOCUMENTO = ? WHERE ID = ?",
        (cliente.nome, cliente.documento, id)
    )
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    conn.commit()
    conn.close()
    return {"status": "ok", "mensagem": "Cliente atualizado com sucesso"}


# ----------------------
# PEDIDOS (FATURAMENTOS + FATURAMENTOSITENS)
# ----------------------
@app.get("/pedidos", response_model=list[Pedido])
def listar_pedidos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT ID, CLIENTE_ID, TOTAL FROM FATURAMENTOS ROWS 50")
    pedidos = []
    for row in cur.fetchall():
        cur.execute(
            "SELECT PRODUTO_ID, QTD, PRECO_UNIT FROM FATURAMENTOSITENS WHERE PEDIDO_ID = ?",
            (row[0],)
        )
        itens = [
            {"produto_id": item[0], "quantidade": item[1], "preco_unitario": float(item[2])}
            for item in cur.fetchall()
        ]
        pedidos.append(
            {"id": row[0], "cliente_id": row[1], "total": float(row[2]), "itens": itens}
        )
    conn.close()
    return pedidos


@app.post("/pedidos")
def cadastrar_pedido(pedido: Pedido):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO FATURAMENTOS (CLIENTE_ID, TOTAL) VALUES (?, ?) RETURNING ID",
        (pedido.cliente_id, pedido.total)
    )
    pedido_id = cur.fetchone()[0]

    for item in pedido.itens:
        cur.execute(
            "INSERT INTO FATURAMENTOSITENS (PEDIDO_ID, PRODUTO_ID, QTD, PRECO_UNIT) VALUES (?, ?, ?, ?)",
            (pedido_id, item.produto_id, item.quantidade, item.preco_unitario)
        )

    conn.commit()
    conn.close()
    return {"status": "ok", "pedido_id": pedido_id}


@app.put("/pedidos/{id}")
def alterar_pedido(id: int, pedido: Pedido):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE FATURAMENTOS SET CLIENTE_ID = ?, TOTAL = ? WHERE ID = ?",
        (pedido.cliente_id, pedido.total, id)
    )
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    # Atualizar itens (remove e insere de novo)
    cur.execute("DELETE FROM FATURAMENTOSITENS WHERE PEDIDO_ID = ?", (id,))
    for item in pedido.itens:
        cur.execute(
            "INSERT INTO FATURAMENTOSITENS (PEDIDO_ID, PRODUTO_ID, QTD, PRECO_UNIT) VALUES (?, ?, ?, ?)",
            (id, item.produto_id, item.quantidade, item.preco_unitario)
        )

    conn.commit()
    conn.close()
    return {"status": "ok", "mensagem": "Pedido atualizado com sucesso"}


@app.delete("/pedidos/{id}")
def deletar_pedido(id: int):
    conn = get_connection()
    cur = conn.cursor()

    # Verifica se o pedido existe
    cur.execute("SELECT ID FROM FATURAMENTOS WHERE ID = ?", (id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    # Remove itens do pedido
    cur.execute("DELETE FROM FATURAMENTOSITENS WHERE PEDIDO_ID = ?", (id,))
    # Remove cabeçalho do pedido
    cur.execute("DELETE FROM FATURAMENTOS WHERE ID = ?", (id,))

    conn.commit()
    conn.close()
    return {"status": "ok", "mensagem": f"Pedido {id} deletado com sucesso"}