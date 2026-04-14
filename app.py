from criptografia import gerar_chave, criptografar, descriptografar
from banco_de_dado import inicializar_banco, adicionar_senha, ler_senhas, atualizar_senha, deletar_senha

def main():
    senha_mestra = input("Digite a senha mestre: ")
    chave = gerar_chave(senha_mestra)
    inicializar_banco()
    while True:
        print("1. Inserir senha")
        print("2. Ler senha")
        print("3. Atualizar senha")
        print("4. Excluir senha")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            inserir_senha(chave)
        elif opcao == "2":
            ler_senha(chave)
        elif opcao == "3":
            update_senha(chave)
        elif opcao == "4":
            excluir_senha()
        elif opcao == "5":
            break
        else:
            print("Opção inválida. Tente novamente.")


def inserir_senha(chave: bytes):
    try:
        servico = input("Digite o nome do serviço: ")
        senha = input("Digite a senha: ")
        senha_crip = criptografar(senha, chave)
        adicionar_senha(servico, senha_crip)
        print("Senha adicionada com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar senha: {e}")


def ler_senha(chave: bytes):
    try:
        servico = input("Digite o nome do serviço: ")
        resultado = ler_senhas(servico)
        if resultado:
            senha = descriptografar(resultado[2], chave)
            print(f"A senha para {servico} é: {senha}")
        else:
            print("Serviço não encontrado.")
    except Exception as e:
        print(f"Erro ao ler senha: {e}")

def update_senha(chave: bytes):
    try:
        servico = input("Digite o nome do serviço: ")
        nova_senha = input("Digite a nova senha: ")
        senha_crip = criptografar(nova_senha, chave)
        atualizar_senha(servico, senha_crip)
        print("Senha atualizada com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar senha: {e}")

def excluir_senha():
    try:
        servico = input("Digite o nome do serviço: ")
        deletar_senha(servico)
        print("Senha excluída com sucesso!")
    except Exception as e:
        print(f"Erro ao excluir senha: {e}")

if __name__ == "__main__":
    main()