
import sqlite3
from pathlib import Path

from database import DB_PATH


def inicializar_demo():
    caminho_seed = Path(__file__).resolve().parent / "demo_seed.sql"

    if not caminho_seed.exists():
        return

    # Se o banco já existe, preserva os dados
    if DB_PATH.exists():
        return

    conexao = sqlite3.connect(DB_PATH)

    try:
        script_sql = caminho_seed.read_text(encoding="utf-8")
        conexao.executescript(script_sql)
        conexao.commit()

    except Exception:
        conexao.close()

        # Exclui banco incompleto
        if DB_PATH.exists():
            DB_PATH.unlink()

        raise

    finally:
        conexao.close()
