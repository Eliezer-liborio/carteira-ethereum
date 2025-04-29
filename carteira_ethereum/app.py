from flask import Flask, render_template, request
import sqlite3
import os
from wallet_generator import gerar_carteira, hash_frase, criptografar_private_key, salvar_em_arquivo

app = Flask(__name__)

# Banco de dados
db_path = 'usuarios.db'

def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            frase_seg TEXT NOT NULL,
            endereco TEXT NOT NULL,
            chave_privada_criptografada TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/criar', methods=['POST'])
def criar_carteira():
    try:
        email = request.form['email']
        telefone = request.form['telefone']
        frase = request.form['frase']

        endereco, private_key, mnemonic = gerar_carteira()
        frase_hash = hash_frase(frase)
        private_key_criptografada = criptografar_private_key(private_key)

        # Salvar no banco
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO usuarios (email, telefone, frase_seg, endereco, chave_privada_criptografada)
            VALUES (?, ?, ?, ?, ?)
        ''', (email, telefone, frase_hash, endereco, private_key_criptografada))
        conn.commit()
        conn.close()

        # Atualizar arquivo .cap
        dados = f"Email: {email} | Telefone: {telefone} | Endereço: {endereco} | PrivateKey: {private_key}"
        salvar_em_arquivo(dados)

        return render_template('sucesso.html', endereco=endereco, private_key=private_key)

    except Exception as e:
        return f"Erro interno: {str(e)}"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
