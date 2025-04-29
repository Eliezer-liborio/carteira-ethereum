from flask import Flask, render_template, request, jsonify
from eth_account import Account
import secrets

# Habilita geração de carteiras sem precisar usar Metamask
Account.enable_unaudited_hdwallet_features()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar-carteira', methods=['POST'])
def gerar_carteira():
    try:
        data = request.get_json()
        email = data.get('email')
        telefone = data.get('telefone')

        # Gerando carteira com frase mnemônica
        acct, mnemonic = Account.create_with_mnemonic()

        print(f"[+] Carteira gerada para {email} - {telefone}")
        print(f"    Endereço: {acct.address}")
        print(f"    Chave privada: {acct.key.hex()}")
        print(f"    Frase mnemônica: {mnemonic}")

        return jsonify({
            'success': True,
            'email': email,
            'telefone': telefone,
            'address': acct.address,
            'private_key': acct.key.hex(),
            'mnemonic': mnemonic
        })

    except Exception as e:
        print(f"[!] Erro ao gerar carteira: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
