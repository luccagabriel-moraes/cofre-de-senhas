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

Todas as senhas são criptografadas com **Fernet (AES-128-CBC + HMAC)** antes de serem salvas no banco. Sem a senha mestra é impossível descriptografar os dados.

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
├── iniciar_cofre.sh  # Script de lançamento
├── cofre.desktop     # Atalho para área de trabalho/menu de aplicativos
└── cofre.db          # Banco de dados local (gerado automaticamente)
```

## Instalação

```bash
# Clone o repositório
git clone https://github.com/LuccaGabriel-Moraes/cofre-de-senhas.git
cd cofre-de-senhas

# Instale as dependências
pip install cryptography PyQt6 keyring --break-system-packages
```

## Como usar

```bash
python3 visual.py
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
- Login com limite de 3 tentativas (app fecha automaticamente ao esgotar)
- Inserir senha para um serviço
- Visualizar senha de um serviço (mostrar/ocultar)
- Atualizar senha de um serviço
- Excluir senha de um serviço
- Interface responsiva (funciona em janela e tela cheia)

## Segurança

- Senha de login protegida pelo cofre nativo do sistema (GNOME Keyring)
- Senhas criptografadas com Fernet antes de serem salvas
- A chave de criptografia nunca é armazenada em disco
- Sem a senha mestra, os dados são completamente ilegíveis

---

## 🖥️ Abrir pelo ícone (sem terminal)

Siga os passos abaixo para abrir o Cofre de Senhas com um clique, igual ao Chrome ou Obsidian.

### Passo único — Rodar dentro da pasta do projeto

```bash
CAMINHO=$(pwd) && cat > cofre.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Cofre de Senhas
Comment=Gerenciador de senhas local
Exec=python3 visual.py
Path=$CAMINHO
Icon=security-high
Terminal=false
Categories=Utility;Security;
EOF
cp cofre.desktop ~/.local/share/applications/
```

Depois procure **"Cofre de Senhas"** no menu de aplicativos — vai aparecer como qualquer outro app instalado.

> **Nota:** Caso queira também na área de trabalho, copie o `cofre.desktop` para `~/Área de trabalho/` e clique com botão direito → Permitir executar.
