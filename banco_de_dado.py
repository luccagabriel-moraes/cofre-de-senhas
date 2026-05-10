import sqlite3

def inicializar_banco():
    try:
        print("Inicializando banco de dados...")
        conn = sqlite3.connect("cofre.db")
        cursor = conn.cursor()
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS senhas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,   
                        servico TEXT,
                        senha TEXT
                    )
                """)
        conn.commit()
        print("Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

def adicionar_senha(servico: str, senha: str):
    conn = sqlite3.connect("cofre.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO senhas (servico, senha) VALUES (?, ?)", (servico, senha))
    conn.commit()
    conn.close()

def ler_senhas(servico: str):
    conn = sqlite3.connect("cofre.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM senhas WHERE servico = ?", (servico,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def retornar_todos_servicos():
    conn = sqlite3.connect("cofre.db")
    cursor = conn.cursor()
    cursor.execute("SELECT servico, senha FROM senhas")
    resultado = cursor.fetchall() 
    conn.close()
    return resultado

def atualizar_senha(servico: str, senha_crip: bytes):
    conn = sqlite3.connect("cofre.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE senhas SET senha = ? WHERE servico = ?", (senha_crip, servico))
    conn.commit()
    conn.close()

def deletar_senha(servico: str):
    conn = sqlite3.connect("cofre.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM senhas WHERE servico = ?", (servico,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    inicializar_banco()