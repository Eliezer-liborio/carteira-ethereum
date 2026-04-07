import os
import logging
from flask import Flask, render_template, request, jsonify
from eth_account import Account
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Habilita geração de carteiras com frase mnemônica
Account.enable_unaudited_hdwallet_features()

app = Flask(__name__)

# Configura o logger padrão do Python (substitui os print() inseguros)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gerar-carteira", methods=["POST"])
def gerar_carteira():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Corpo da requisição inválido."}), 400

        email = data.get("email", "").strip()
        telefone = data.get("telefone", "").strip()

        if not email or not telefone:
            return jsonify({"success": False, "error": "Email e telefone são obrigatórios."}), 400

        # Geração da carteira com frase mnemônica
        acct, mnemonic = Account.create_with_mnemonic()

        # Log seguro: apenas o endereço público é registrado, NUNCA a chave privada
        logger.info("Carteira gerada para %s | Endereço: %s", email, acct.address)

        return jsonify({
            "success": True,
            "email": email,
            "telefone": telefone,
            "address": acct.address,
            "private_key": acct.key.hex(),
            "mnemonic": mnemonic,
        })

    except Exception as e:
        logger.error("Erro ao gerar carteira: %s", str(e))
        return jsonify({"success": False, "error": "Erro interno no servidor."}), 500


if __name__ == "__main__":
    # O modo debug é controlado pela variável de ambiente FLASK_DEBUG.
    # Em produção, FLASK_DEBUG deve ser "false" (ou simplesmente não definida).
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() in ("true", "1", "t")
    app.run(host="127.0.0.1", port=5000, debug=debug_mode)
