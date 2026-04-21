# 🔐 Cofre de Senhas
 
> Gerenciador de senhas local com criptografia real e interface gráfica.
 
![Python](https://img.shields.io/badge/Python-3.13-blue)
![Cryptography](https://img.shields.io/badge/Cryptography-Fernet-brightgreen)
![SQLite](https://img.shields.io/badge/Banco-SQLite-lightgrey)
![PyQt6](https://img.shields.io/badge/Interface-PyQt6-purple)
![Local](https://img.shields.io/badge/Uso-Local-orange)
![Licença](https://img.shields.io/badge/Licença-MIT-green)
 
## Como funciona
 
O cofre tem dois níveis de proteção:
 
1. **Senha de login** — salva com segurança no cofre nativo do sistema operacional via `keyring` (GNOME Keyring no Linux). Necessária para abrir o app.
2. **Senha mestra** — nunca armazenada em lugar nenhum. Usada para derivar a chave Fernet via PBKDF2 + SHA256. Necessária para criptografar e descriptografar as senhas salvas.
Todas as senhas são criptografadas com **Fernet (AES-128)** antes de serem salvas no banco. Sem a senha mestra é impossível descriptografar os dados.
 
## Tecnologias
 
- Python 3.13
- `cryptography` — criptografia Fernet + derivação de chave PBKDF2
- `sqlite3` — banco de dados local (já incluso no Python)
- `keyring` — armazenamento seguro da senha de login no SO
- `PyQt6` — interface gráfica
## Estrutura
 
```
├── visual.py         # Interface gráfica (login, cadastro, menu)
├── app.py            # Interface de linha de comando (legado)
├── criptografia.py   # Geração de chave, criptografia e descriptografia
├── banco_de_dado.py  # Operações CRUD no banco SQLite
└── cofre.db          # Banco de dados local (gerado automaticamente)
```
 
## Instalação
 
```bash
# Clone o repositório
git clone https://github.com/LuccaGabriel-Moraes/cofre-de-senhas.git
cd cofre-de-senhas
 
# Instale as dependências
pip install cryptography PyQt6 keyring
```
 
## Como usar
 
```bash
python visual.py
```
 
**Primeira execução:** o app exibe uma tela de cadastro para você criar sua senha de login. Nas próximas vezes vai direto para o login.
 
**Importante:** não esqueça a senha mestra — ela nunca é armazenada em lugar nenhum e não há como recuperar os dados sem ela.
 
## Fluxo do app
 
```
1. Abre o app
2. Digite a senha de LOGIN  →  verificada no keyring do sistema
3. Digite a senha MESTRA    →  deriva a chave Fernet na memória
4. Acessa as senhas criptografadas no banco
```
 
## Funcionalidades
 
- Cadastro de senha de login na primeira execução
- Login com limite de 3 tentativas
- Inserir senha para um serviço
- Ler senha de um serviço
- Atualizar senha de um serviço
- Excluir senha de um serviço
## Segurança
 
- Senha de login protegida pelo cofre nativo do sistema (GNOME Keyring)
- Senhas criptografadas com Fernet antes de serem salvas
- A chave de criptografia nunca é armazenada em disco
- Sem a senha mestra, os dados são completamente ilegíveis
