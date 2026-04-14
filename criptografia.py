from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64

def main():
    senha_mestra = input("Digite a senha mestre: ")
    chave = gerar_chave(senha_mestra)
    print (chave)
    senha = input("senha: ")
    senha_crip = criptografar(senha, chave)
    print (f"senha crip: {senha_crip}")
    senha_normal = descriptografar(senha_crip, chave)
    print (f"senha sem crip: {senha_normal}")

def gerar_chave(senha_mestra: str) -> bytes:
    salt = base64.urlsafe_b64decode("M0BOKqwqEK1J0AAsmdp2ww==")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return base64.urlsafe_b64encode(kdf.derive(senha_mestra.encode()))


def criptografar(senha_sem_criptografia: str, chave: bytes) -> bytes:
    f = Fernet(chave)
    return f.encrypt(senha_sem_criptografia.encode())


def descriptografar(senha_criptografada: bytes, chave: bytes) -> str:
    f = Fernet(chave)
    return f.decrypt(senha_criptografada).decode()


if __name__ == "__main__":
    main()