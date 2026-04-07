import os
import bcrypt
from eth_account import Account
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Carrega as variáveis definidas no arquivo .env
load_dotenv()


def _carregar_fernet() -> Fernet:
    """
    Carrega a chave mestra de criptografia a partir da variável de ambiente
    FERNET_SECRET_KEY. Levanta um erro explícito caso a variável não esteja
    definida, evitando que a aplicação suba em estado inseguro.
    """
    chave = os.getenv("FERNET_SECRET_KEY")
    if not chave:
        raise EnvironmentError(
            "A variável de ambiente FERNET_SECRET_KEY não está definida. "
            "Gere uma chave com: "
            "python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\" "
            "e adicione ao arquivo .env"
        )
    return Fernet(chave.encode())


# Instância única do Fernet, carregada uma vez na inicialização do módulo
fernet = _carregar_fernet()


def gerar_carteira() -> tuple:
    """
    Gera um novo par de chaves Ethereum (endereço público e chave privada).
    Retorna uma tupla (endereco, private_key, mnemonic).
    """
    account = Account.create()
    endereco = account.address
    private_key = account._private_key.hex()
    mnemonic = ""
    return endereco, private_key, mnemonic


def hash_frase(frase: str) -> bytes:
    """
    Gera um hash seguro (bcrypt) da frase de segurança do usuário.
    O salt é gerado automaticamente pelo bcrypt a cada chamada.
    """
    return bcrypt.hashpw(frase.encode("utf-8"), bcrypt.gensalt())


def verificar_frase(frase: str, frase_hash: bytes) -> bool:
    """
    Verifica se uma frase de segurança corresponde ao hash armazenado.
    """
    return bcrypt.checkpw(frase.encode("utf-8"), frase_hash)


def criptografar_private_key(private_key: str) -> bytes:
    """
    Criptografa a chave privada usando a chave mestra Fernet carregada
    da variável de ambiente. O resultado é seguro para armazenar em banco
    de dados, pois sem a FERNET_SECRET_KEY o valor é indecifrável.
    """
    return fernet.encrypt(private_key.encode("utf-8"))


def descriptografar_private_key(private_key_criptografada: bytes) -> str:
    """
    Descriptografa a chave privada usando a chave mestra Fernet.
    Levanta cryptography.fernet.InvalidToken se a chave ou os dados
    estiverem corrompidos.
    """
    return fernet.decrypt(private_key_criptografada).decode("utf-8")
