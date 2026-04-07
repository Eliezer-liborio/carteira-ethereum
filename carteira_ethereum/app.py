import os
import logging
import sqlite3
from flask import Flask, render_template, request
from dotenv import load_dotenv
from wallet_generator import gerar_carteira, hash_frase, criptografar_private_key

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Logger seguro — substitui os print() e f"Erro interno: {str(e)}"
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Caminho do banco de dados
db_path = os.getenv("DB_PATH", "usuarios.db")


def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            frase_seg TEXT NOT NULL,
            endereco TEXT NOT NULL,
            chave_privada_criptografada BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/criar", methods=["POST"])
def criar_carteira():
    try:
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        frase = request.form.get("frase", "").strip()

        if not email or not telefone or not frase:
            return "Todos os campos são obrigatórios.", 400

        endereco, private_key, mnemonic = gerar_carteira()
        frase_hash = hash_frase(frase)
        private_key_criptografada = criptografar_private_key(private_key)

        # Salvar no banco de dados com query parametrizada (proteção contra SQL Injection)
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            INSERT INTO usuarios (email, telefone, frase_seg, endereco, chave_privada_criptografada)
            VALUES (?, ?, ?, ?, ?)
        """, (email, telefone, frase_hash, endereco, private_key_criptografada))
        conn.commit()
        conn.close()

        # Log seguro: apenas endereço público é registrado
        logger.info("Carteira criada para %s | Endereço: %s", email, endereco)

        # A chave privada é exibida ao usuário APENAS neste momento (não armazenada em texto claro)
        return render_template("sucesso.html", endereco=endereco, private_key=private_key)

    except Exception as e:
        # Mensagem genérica para o usuário; detalhe interno apenas no log
        logger.error("Erro ao criar carteira: %s", str(e))
        return "Ocorreu um erro interno. Tente novamente.", 500


if __name__ == "__main__":
    init_db()
    # O modo debug é controlado pela variável de ambiente FLASK_DEBUG.
    # Em produção, FLASK_DEBUG deve ser "false" (ou simplesmente não definida).
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() in ("true", "1", "t")
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)
