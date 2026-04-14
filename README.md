# 🔐 Cofre de Senhas

> Gerenciador de senhas local com criptografia real e interface gráfica.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Cryptography](https://img.shields.io/badge/Cryptography-Fernet-brightgreen)
![SQLite](https://img.shields.io/badge/Banco-SQLite-lightgrey)
![Local](https://img.shields.io/badge/Uso-Local-orange)
![Licença](https://img.shields.io/badge/Licença-MIT-green)

## Como funciona

Todas as senhas são criptografadas com **Fernet (AES-128)** antes de serem salvas. A chave de criptografia é derivada da sua senha mestra usando **PBKDF2 + SHA256** — isso significa que nenhuma senha fica armazenada em texto puro, e sem a senha mestra é impossível descriptografar os dados.

## Tecnologias

- Python 3.13
- `cryptography` — criptografia Fernet + derivação de chave PBKDF2
- `sqlite3` — banco de dados local (já incluso no Python)

## Estrutura

```
├── app.py            # Interface de linha de comando e fluxo principal
├── criptografia.py   # Geração de chave, criptografia e descriptografia
├── banco_de_dado.py  # Operações CRUD no banco SQLite
└── cofre.db          # Banco de dados local (gerado automaticamente)
```

## Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/cofre-de-senhas.git
cd cofre-de-senhas

# Instale a dependência
pip install cryptography
```

## Como usar

```bash
python app.py
```

Na primeira execução, defina uma senha mestra. Ela será usada para criptografar e descriptografar todas as suas senhas. **Não esqueça ela — não há como recuperar os dados sem a senha mestra.**

## Funcionalidades

- Inserir senha para um serviço
- Ler senha de um serviço
- Atualizar senha de um serviço
- Excluir senha de um serviço

## Segurança

- As senhas são criptografadas antes de serem salvas no banco
- A chave nunca é armazenada em disco
- Sem a senha mestra, os dados são ilegíveis
