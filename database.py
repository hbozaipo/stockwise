
import sqlite3
from pathlib import Path

# Localização do banco de dados
DB_PATH = Path(__file__).resolve().parent / "stockwise.db"


# ==========================================
# 1. CONEXÃO COM O BANCO
# ==========================================

def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


# ==========================================
# 2. CRIAÇÃO DAS TABELAS
# ==========================================

def criar_tabelas():
    
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco_custo REAL NOT NULL
                    CHECK (preco_custo >= 0),
                preco_venda REAL NOT NULL
                    CHECK (preco_venda >= 0),
                quantidade INTEGER NOT NULL DEFAULT 0
                    CHECK (quantidade >= 0),
                estoque_minimo INTEGER NOT NULL DEFAULT 5
                    CHECK (estoque_minimo >= 0)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL
                    CHECK (tipo IN ('ENTRADA', 'SAIDA')),
                quantidade INTEGER NOT NULL
                    CHECK (quantidade > 0),
                data_movimentacao TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (produto_id)
                    REFERENCES produtos(id)
            )
        """)
        
        # Tabela de vendas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_venda TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,
                valor_total REAL NOT NULL
                    CHECK (valor_total >= 0)
            )
        """)
    
        # Produtos de cada venda
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens_venda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venda_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL
                    CHECK (quantidade > 0),
                preco_unitario REAL NOT NULL
                    CHECK (preco_unitario >= 0),
                custo_unitario REAL NOT NULL
                    CHECK (custo_unitario >= 0),
                FOREIGN KEY (venda_id)
                    REFERENCES vendas(id),
                FOREIGN KEY (produto_id)
                    REFERENCES produtos(id)
            )
        """)
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS
            idx_produtos_nome_unico
            ON produtos (LOWER(TRIM(nome)))
        """)

        conexao.commit()

    finally:
        conexao.close()


# ==========================================
# 3. CADASTRAR PRODUTO
# ==========================================

def cadastrar_produto(nome, custo, venda, quantidade, minimo):
    nome = nome.strip()
    
    if not nome:
        raise ValueError("O nome do produto é obrigatório.")
    
    if produto_ja_existe(nome):
        raise ValueError(
            f"O produto '{nome}' já está cadastrado!"
        )
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO produtos (
                nome,
                preco_custo,
                preco_venda,
                quantidade,
                estoque_minimo
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            nome,
            custo,
            venda,
            quantidade,
            minimo
        ))

        conexao.commit()

        return cursor.lastrowid

    finally:
        conexao.close()


# ==========================================
# 4. LISTAR PRODUTOS
# ==========================================

def listar_produtos():
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                nome,
                preco_custo,
                preco_venda,
                quantidade,
                estoque_minimo
            FROM produtos
            ORDER BY nome
        """)

        return cursor.fetchall()

    finally:
        conexao.close()


# ==========================================
# 5. EDITAR PRODUTO
# ==========================================

def atualizar_produto(
    id_produto, nome, custo, venda, minimo
):
    nome = nome.strip()
    
    if not nome:
        raise ValueError("O nome do produto é obrigatório.")
    
    if produto_ja_existe(nome, ignorar_id=id_produto):
        raise ValueError(
            f"Já existe outro produto chamado '{nome}'."
        )
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE produtos
            SET
                nome = ?,
                preco_custo = ?,
                preco_venda = ?,
                estoque_minimo = ?
            WHERE id = ?
        """, (
            nome,
            custo,
            venda,
            minimo,
            id_produto
        ))

        atualizado = cursor.rowcount > 0

        conexao.commit()

        return atualizado

    finally:
        conexao.close()

# ==========================================
# 6. REPOR ESTOQUE
# ==========================================

def repor_estoque(id_produto, quantidade):
    if quantidade <= 0:
        raise ValueError(
            "A quantidade deve ser maior que zero."
        )

    conexao = conectar()

    try:
        cursor = conexao.cursor()

        # Inicia uma transação
        cursor.execute("BEGIN IMMEDIATE")

        # Atualiza o estoque do produto
        cursor.execute("""
            UPDATE produtos
            SET quantidade = quantidade + ?
            WHERE id = ?
        """, (quantidade, id_produto))

        if cursor.rowcount == 0:
            raise ValueError("Produto não encontrado.")

        # Registra a movimentação
        cursor.execute("""
            INSERT INTO movimentacoes_estoque (
                produto_id,
                tipo,
                quantidade
            )
            VALUES (?, 'ENTRADA', ?)
        """, (id_produto, quantidade))

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


# ==========================================
# 7. CONSULTAR MOVIMENTAÇÕES
# ==========================================

def listar_movimentacoes():
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                m.id,
                p.nome,
                m.tipo,
                m.quantidade,
                m.data_movimentacao
            FROM movimentacoes_estoque m
            JOIN produtos p
                ON p.id = m.produto_id
            ORDER BY m.id DESC
        """)

        return cursor.fetchall()

    finally:
        conexao.close()
        

# ==========================================
# 8. REGISTRAR VENDA
# ==========================================

def registrar_venda(carrinho):
    """
    carrinho = [
        (id_produto, quantidade),
        (id_produto, quantidade)
    ]
    """

    if not carrinho:
        raise ValueError("O carrinho está vazio.")

    ids = [id_produto for id_produto, _ in carrinho]

    if len(ids) != len(set(ids)):
        raise ValueError("Existem produtos repetidos no carrinho.")

    for id_produto, quantidade in carrinho:
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("Quantidade inválida.")

    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("BEGIN IMMEDIATE")

        itens = []
        total_centavos = 0

        # Verifica os produtos e calcula a venda
        for id_produto, quantidade in carrinho:

            cursor.execute("""
                SELECT nome, preco_custo,
                       preco_venda, quantidade
                FROM produtos
                WHERE id = ?
            """, (id_produto,))

            produto = cursor.fetchone()

            if produto is None:
                raise ValueError(
                    f"Produto {id_produto} não encontrado."
                )

            nome, custo, preco, estoque = produto

            if quantidade > estoque:
                raise ValueError(
                    f"Estoque insuficiente para {nome}. "
                    f"Disponível: {estoque}"
                )

            # Calcula em centavos para evitar
            # acumular erros de ponto flutuante
            preco_centavos = round(preco * 100)

            total_centavos += preco_centavos * quantidade

            itens.append((
                id_produto,
                quantidade,
                preco,
                custo
            ))

        valor_total = total_centavos / 100

        # Salva a venda
        cursor.execute("""
            INSERT INTO vendas (valor_total)
            VALUES (?)
        """, (valor_total,))

        id_venda = cursor.lastrowid

        # Registra os itens e desconta do estoque
        for id_produto, quantidade, preco, custo in itens:

            cursor.execute("""
                INSERT INTO itens_venda (
                    venda_id,
                    produto_id,
                    quantidade,
                    preco_unitario,
                    custo_unitario
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                id_venda,
                id_produto,
                quantidade,
                preco,
                custo
            ))

            cursor.execute("""
                UPDATE produtos
                SET quantidade = quantidade - ?
                WHERE id = ?
                  AND quantidade >= ?
            """, (
                quantidade,
                id_produto,
                quantidade
            ))

            if cursor.rowcount != 1:
                raise ValueError(
                    "Não foi possível atualizar o estoque."
                )

            cursor.execute("""
                INSERT INTO movimentacoes_estoque (
                    produto_id,
                    tipo,
                    quantidade
                )
                VALUES (?, 'SAIDA', ?)
            """, (
                id_produto,
                quantidade
            ))

        conexao.commit()

        return id_venda

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


# ==========================================
# 9. HISTÓRICO DE VENDAS
# ==========================================

def listar_vendas():
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                v.id,
                v.data_venda,
                v.valor_total,
                SUM(i.quantidade),
                SUM(
                    i.quantidade *
                    (i.preco_unitario - i.custo_unitario)
                )
            FROM vendas v
            JOIN itens_venda i
                ON i.venda_id = v.id
            GROUP BY
                v.id,
                v.data_venda,
                v.valor_total
            ORDER BY v.id DESC
        """)

        return cursor.fetchall()

    finally:
        conexao.close()


# ==========================================
# 10. DETALHES DE UMA VENDA
# ==========================================

def listar_itens_venda(id_venda):
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                p.nome,
                i.quantidade,
                i.preco_unitario,
                i.quantidade * i.preco_unitario
            FROM itens_venda i
            JOIN produtos p
                ON p.id = i.produto_id
            WHERE i.venda_id = ?
            ORDER BY i.id
        """, (id_venda,))

        return cursor.fetchall()

    finally:
        conexao.close()


# ==========================================
# 11. INDICADORES DO DASHBOARD
# ==========================================

def indicadores_dashboard():
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        # Informações do estoque atual
        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(quantidade), 0),
                COALESCE(
                    SUM(quantidade * preco_custo), 0
                ),
                COALESCE(
                    SUM(
                        CASE
                            WHEN quantidade <= estoque_minimo
                            THEN 1
                            ELSE 0
                        END
                    ), 0
                )
            FROM produtos
        """)

        estoque = cursor.fetchone()

        # Informações das vendas
        cursor.execute("""
            SELECT
                COUNT(DISTINCT v.id),
                COALESCE(SUM(i.quantidade), 0),
                COALESCE(
                    SUM(i.quantidade * i.preco_unitario), 0
                ),
                COALESCE(
                    SUM(
                        i.quantidade *
                        (i.preco_unitario - i.custo_unitario)
                    ), 0
                )
            FROM vendas v
            JOIN itens_venda i
                ON v.id = i.venda_id
        """)

        vendas = cursor.fetchone()

        return {
            "total_produtos": estoque[0],
            "unidades_estoque": estoque[1],
            "investimento_estoque": estoque[2],
            "estoque_baixo": estoque[3],
            "total_vendas": vendas[0],
            "unidades_vendidas": vendas[1],
            "faturamento": vendas[2],
            "lucro_bruto": vendas[3]
        }

    finally:
        conexao.close()


# ==========================================
# 12. DADOS DOS GRÁFICOS
# ==========================================

def dados_graficos():
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        # Faturamento por dia
        cursor.execute("""
            SELECT
                DATE(v.data_venda),
                ROUND(
                    SUM(
                        i.quantidade * i.preco_unitario
                    ), 2
                )
            FROM vendas v
            JOIN itens_venda i
                ON v.id = i.venda_id
            GROUP BY DATE(v.data_venda)
            ORDER BY DATE(v.data_venda)
        """)

        faturamento_diario = cursor.fetchall()

        # Cinco produtos mais vendidos
        cursor.execute("""
            SELECT
                p.nome,
                SUM(i.quantidade) AS total_vendido
            FROM itens_venda i
            JOIN produtos p
                ON p.id = i.produto_id
            GROUP BY p.id, p.nome
            ORDER BY total_vendido DESC, p.nome
            LIMIT 5
        """)

        mais_vendidos = cursor.fetchall()

        # Produtos que precisam de reposição
        cursor.execute("""
            SELECT
                nome,
                quantidade,
                estoque_minimo
            FROM produtos
            WHERE quantidade <= estoque_minimo
            ORDER BY quantidade ASC, nome
        """)

        estoque_baixo = cursor.fetchall()

        return {
            "faturamento_diario": faturamento_diario,
            "mais_vendidos": mais_vendidos,
            "estoque_baixo": estoque_baixo
        }

    finally:
        conexao.close()

def produto_ja_existe(nome, ignorar_id=None):
    conexao = conectar()

    try:
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id
            FROM produtos
            WHERE LOWER(TRIM(nome)) = LOWER(TRIM(?))
              AND (? IS NULL OR id != ?)
            LIMIT 1
        """, (nome, ignorar_id, ignorar_id))

        return cursor.fetchone() is not None

    finally:
        conexao.close()