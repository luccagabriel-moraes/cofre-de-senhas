import sys
import keyring
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from cryptography.fernet import InvalidToken
from criptografia import gerar_chave, criptografar, descriptografar
from banco_de_dado import inicializar_banco, adicionar_senha, retornar_todos_servicos


# ──────────────────────────────────────────────
#  HELPERS
# ──────────────────────────────────────────────
def criar_label_aviso_red():
    aviso = QLabel(" ")
    aviso.setAlignment(Qt.AlignmentFlag.AlignCenter)
    aviso.setFixedSize(270, 25)
    aviso.setFont(QFont("Arial", 10, QFont.Weight.Bold))
    aviso.setStyleSheet("color: red; border: none;")
    return aviso

def keyring_get(service, key):
    try:
        return keyring.get_password(service, key)
    except Exception:
        return None

def keyring_set(service, key, value):
    try:
        keyring.set_password(service, key, value)
    except Exception:
        pass


# ──────────────────────────────────────────────
#  TELA CADASTRO
# ──────────────────────────────────────────────
def criar_tela_cadastro(stack: QStackedWidget, app: QApplication):
    tela = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    frame = QFrame()
    frame.setFixedSize(350, 280)
    frame.setObjectName("frame")
    frame.setStyleSheet("""
        QFrame#frame {
            background-color: rgba(255, 255, 255, 20);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 50);
        }
        QLabel, QLineEdit, QPushButton { border: none; }
    """)

    layout_frame = QVBoxLayout()
    aviso = criar_label_aviso_red()

    label = QLabel("cadastre a senha para acessar o cofre")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setFont(QFont("Arial", 10, QFont.Weight.Bold))

    campo1 = QLineEdit()
    campo1.setEchoMode(QLineEdit.EchoMode.Password)
    campo1.setFixedWidth(200)
    campo1.setPlaceholderText("Digite sua senha...")
    campo1.setStyleSheet("QLineEdit { border: 1px solid rgba(255,255,255,100); border-radius: 5px; padding: 5px; }")

    campo2 = QLineEdit()
    campo2.setEchoMode(QLineEdit.EchoMode.Password)
    campo2.setFixedWidth(200)
    campo2.setPlaceholderText("Confirme sua senha...")
    campo2.setStyleSheet("QLineEdit { border: 1px solid rgba(255,255,255,100); border-radius: 5px; padding: 5px; }")

    botao = QPushButton("Cadastrar")
    botao.setFixedWidth(200)
    botao.setStyleSheet("QPushButton { border: 1px solid rgba(255,255,255,200); border-radius: 5px; padding: 5px; }")

    layout_frame.addStretch()
    layout_frame.addWidget(aviso, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(5)
    layout_frame.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(10)
    layout_frame.addWidget(campo1, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(5)
    layout_frame.addWidget(campo2, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(5)
    layout_frame.addWidget(botao, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addStretch()
    frame.setLayout(layout_frame)
    layout.addWidget(frame)
    tela.setLayout(layout)

    def confirmar():
        if not campo1.text() or not campo2.text():
            aviso.setText("Preencha ambos os campos.")
        elif campo1.text() != campo2.text():
            aviso.setText("As senhas não coincidem.")
            campo1.clear(); campo2.clear()
        elif len(campo1.text()) < 6:
            aviso.setText("Mínimo de 6 caracteres.")
            campo1.clear(); campo2.clear()
        else:
            keyring_set("cofre-de-senhas", "login", campo1.text())
            stack.setCurrentIndex(1)

    botao.clicked.connect(confirmar)
    campo1.returnPressed.connect(campo2.setFocus)
    campo2.returnPressed.connect(confirmar)
    return tela


# ──────────────────────────────────────────────
#  TELA LOGIN
# ──────────────────────────────────────────────
def criar_tela_login(stack: QStackedWidget, app: QApplication):
    tela = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    frame = QFrame()
    frame.setFixedSize(350, 250)
    frame.setObjectName("frame")
    frame.setStyleSheet("""
        QFrame#frame {
            background-color: rgba(255, 255, 255, 20);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 50);
        }
        QLabel, QLineEdit, QPushButton { border: none; }
    """)

    layout_frame = QVBoxLayout()
    aviso = criar_label_aviso_red()

    label = QLabel("senha para acessar o cofre")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setFont(QFont("Arial", 10, QFont.Weight.Bold))

    campo = QLineEdit()
    campo.setEchoMode(QLineEdit.EchoMode.Password)
    campo.setFixedWidth(200)
    campo.setPlaceholderText("Digite sua senha...")
    campo.setStyleSheet("QLineEdit { border: 1px solid rgba(255,255,255,100); border-radius: 5px; padding: 5px; }")

    botao = QPushButton("Entrar")
    botao.setFixedWidth(200)
    botao.setStyleSheet("QPushButton { border: 1px solid rgba(255,255,255,200); border-radius: 5px; padding: 5px; }")

    layout_frame.addStretch()
    layout_frame.addWidget(aviso, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(10)
    layout_frame.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(5)
    layout_frame.addWidget(campo, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(5)
    layout_frame.addWidget(botao, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addStretch()
    frame.setLayout(layout_frame)
    layout.addWidget(frame)
    tela.setLayout(layout)

    tentativas = [0]

    def verificar():
        if tentativas[0] >= 3:
            return
        senha_salva = keyring_get("cofre-de-senhas", "login")
        if campo.text() == senha_salva:
            campo.clear()
            stack.setCurrentIndex(2)
        else:
            tentativas[0] += 1
            restantes = 3 - tentativas[0]
            campo.clear()
            if restantes > 0:
                aviso.setText(f"Senha incorreta. {restantes} tentativa(s) restante(s).")
            else:
                aviso.setText("Número máximo de tentativas atingido.")
                botao.setEnabled(False)
                QTimer.singleShot(3000, app.quit)

    botao.clicked.connect(verificar)
    campo.returnPressed.connect(verificar)
    return tela


# ──────────────────────────────────────────────
#  ESTILOS COMPARTILHADOS
# ──────────────────────────────────────────────
CARD_STYLE = """
    QFrame#card {
        background-color: rgba(255, 255, 255, 15);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 40);
    }
    QLabel { border: none; }
    QPushButton {
        border: 1px solid rgba(255, 255, 255, 120);
        border-radius: 5px;
        padding: 4px 10px;
        color: white;
    }
    QPushButton:hover { background-color: rgba(255, 255, 255, 30); }
"""

FIELD_STYLE = "QLineEdit { border: 1px solid rgba(255,255,255,100); border-radius: 5px; padding: 4px; }"


# ──────────────────────────────────────────────
#  CARD de serviço existente
# ──────────────────────────────────────────────
def criar_card_servico(servico: str, senha_crip, chave: bytes) -> QFrame:
    card = QFrame()
    card.setFixedHeight(65)
    card.setObjectName("card")
    card.setStyleSheet(CARD_STYLE)

    row = QHBoxLayout()
    row.setContentsMargins(15, 0, 15, 0)

    label_nome = QLabel(servico)
    label_nome.setFont(QFont("Arial", 11, QFont.Weight.Bold))
    label_nome.setFixedWidth(200)

    label_senha = QLabel("••••••••")
    label_senha.setFont(QFont("Arial", 11))
    label_senha.setStyleSheet("color: rgba(255,255,255,150); border: none;")

    btn = QPushButton("Mostrar")
    btn.setFixedWidth(80)
    btn.setCheckable(True)

    def toggle(checked):
        if checked:
            try:
                dado = senha_crip if isinstance(senha_crip, bytes) else senha_crip.encode()
                texto = descriptografar(dado, chave)
                label_senha.setText(texto)
                label_senha.setStyleSheet("color: white; border: none;")
            except (InvalidToken, Exception):
                label_senha.setText("[chave incorreta]")
                label_senha.setStyleSheet("color: red; border: none;")
            btn.setText("Ocultar")
        else:
            label_senha.setText("••••••••")
            label_senha.setStyleSheet("color: rgba(255,255,255,150); border: none;")
            btn.setText("Mostrar")

    btn.toggled.connect(toggle)
    row.addWidget(label_nome)
    row.addWidget(label_senha, stretch=1)
    row.addWidget(btn)
    card.setLayout(row)
    return card


# ──────────────────────────────────────────────
#  CARD de adicionar serviço
# ──────────────────────────────────────────────
def criar_card_adicionar(chave_ref: list, on_salvo) -> QFrame:
    card = QFrame()
    card.setFixedHeight(55)
    card.setObjectName("card")
    card.setStyleSheet(CARD_STYLE)

    layout_card = QVBoxLayout()
    layout_card.setContentsMargins(15, 8, 15, 8)
    layout_card.setSpacing(8)

    # ── linha do título e botão toggle ──
    row_titulo = QHBoxLayout()
    lbl = QLabel("+ Adicionar serviço")
    lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold))
    lbl.setStyleSheet("color: rgba(255,255,255,180); border: none;")

    btn_toggle = QPushButton("Abrir")
    btn_toggle.setFixedWidth(70)
    btn_toggle.setCheckable(True)

    row_titulo.addWidget(lbl)
    row_titulo.addStretch()
    row_titulo.addWidget(btn_toggle)

    # ── formulário ──
    form = QWidget()
    form.setVisible(False)
    row_form = QHBoxLayout()
    row_form.setContentsMargins(0, 0, 0, 0)
    row_form.setSpacing(8)

    aviso = QLabel(" ")
    aviso.setFixedWidth(110)
    aviso.setStyleSheet("color: red; font-size: 10px; border: none;")

    campo_servico = QLineEdit()
    campo_servico.setPlaceholderText("Serviço (ex: Gmail)")
    campo_servico.setFixedWidth(160)
    campo_servico.setStyleSheet(FIELD_STYLE)

    campo_senha = QLineEdit()
    campo_senha.setPlaceholderText("Senha")
    campo_senha.setEchoMode(QLineEdit.EchoMode.Password)
    campo_senha.setFixedWidth(150)
    campo_senha.setStyleSheet(FIELD_STYLE)

    btn_salvar = QPushButton("Salvar")
    btn_salvar.setFixedWidth(65)

    row_form.addWidget(aviso)
    row_form.addWidget(campo_servico)
    row_form.addWidget(campo_senha)
    row_form.addWidget(btn_salvar)
    row_form.addStretch()
    form.setLayout(row_form)

    layout_card.addLayout(row_titulo)
    layout_card.addWidget(form)
    card.setLayout(layout_card)

    def abrir_fechar(checked):
        form.setVisible(checked)
        btn_toggle.setText("Fechar" if checked else "Abrir")
        card.setFixedHeight(110 if checked else 55)

    def salvar():
        servico = campo_servico.text().strip()
        senha   = campo_senha.text()
        chave   = chave_ref[0]
        if not servico:
            aviso.setText("Informe o serviço.")
            return
        if not senha:
            aviso.setText("Informe a senha.")
            return
        senha_crip = criptografar(senha, chave)
        adicionar_senha(servico, senha_crip)
        campo_servico.clear()
        campo_senha.clear()
        aviso.setText(" ")
        btn_toggle.setChecked(False)
        on_salvo()

    btn_toggle.toggled.connect(abrir_fechar)
    btn_salvar.clicked.connect(salvar)
    campo_senha.returnPressed.connect(salvar)
    return card


# ──────────────────────────────────────────────
#  TELA MENU
# ──────────────────────────────────────────────
def criar_tela_menu() -> QWidget:
    tela = QWidget()
    stack_interno = QStackedWidget()

    # ══ Etapa 0: input da senha mestra ══
    tela_senha = QWidget()
    layout_senha = QVBoxLayout()
    layout_senha.setAlignment(Qt.AlignmentFlag.AlignCenter)

    frame = QFrame()
    frame.setFixedSize(350, 220)
    frame.setObjectName("frame")
    frame.setStyleSheet("""
        QFrame#frame {
            background-color: rgba(255, 255, 255, 20);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 50);
        }
        QLabel, QLineEdit, QPushButton { border: none; }
    """)

    layout_frame = QVBoxLayout()
    aviso = criar_label_aviso_red()

    label = QLabel("Digite a senha mestra do cofre")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setFont(QFont("Arial", 10, QFont.Weight.Bold))

    campo_mestra = QLineEdit()
    campo_mestra.setEchoMode(QLineEdit.EchoMode.Password)
    campo_mestra.setFixedWidth(200)
    campo_mestra.setPlaceholderText("Senha mestra...")
    campo_mestra.setStyleSheet("QLineEdit { border: 1px solid rgba(255,255,255,100); border-radius: 5px; padding: 5px; }")

    botao = QPushButton("Confirmar")
    botao.setFixedWidth(200)
    botao.setStyleSheet("QPushButton { border: 1px solid rgba(255,255,255,200); border-radius: 5px; padding: 5px; }")

    layout_frame.addStretch()
    layout_frame.addWidget(aviso, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(5)
    layout_frame.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(10)
    layout_frame.addWidget(campo_mestra, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(5)
    layout_frame.addWidget(botao, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addStretch()
    frame.setLayout(layout_frame)
    layout_senha.addWidget(frame)
    tela_senha.setLayout(layout_senha)

    # ══ tela com os cards ══
    tela_cards = QWidget()
    layout_principal = QVBoxLayout()
    layout_principal.setAlignment(Qt.AlignmentFlag.AlignTop)
    layout_principal.setContentsMargins(40, 30, 40, 20)
    layout_principal.setSpacing(10)

    titulo = QLabel("🔒 Cofre de Senhas")
    titulo.setFont(QFont("Arial", 16, QFont.Weight.Bold))
    titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout_principal.addWidget(titulo)
    layout_principal.addSpacing(5)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setStyleSheet("""
        QScrollArea { border: none; background: transparent; }
        QScrollBar:vertical {
            background: rgba(255,255,255,10); width: 6px; border-radius: 3px;
        }
        QScrollBar::handle:vertical {
            background: rgba(255,255,255,80); border-radius: 3px;
        }
    """)

    container = QWidget()
    container.setStyleSheet("background: transparent;")
    layout_cards = QVBoxLayout()
    layout_cards.setAlignment(Qt.AlignmentFlag.AlignTop)
    layout_cards.setSpacing(10)
    layout_cards.setContentsMargins(0, 0, 10, 0)
    container.setLayout(layout_cards)
    scroll.setWidget(container)
    layout_principal.addWidget(scroll)
    tela_cards.setLayout(layout_principal)

    chave_ref = [None]

    def recarregar_cards():
        # limpa tudo
        for i in reversed(range(layout_cards.count())):
            w = layout_cards.itemAt(i).widget()
            if w:
                w.deleteLater()

        # um card por serviço
        for servico, senha_crip in retornar_todos_servicos():
            layout_cards.addWidget(criar_card_servico(servico, senha_crip, chave_ref[0]))

        # card de adicionar serviço
        layout_cards.addWidget(criar_card_adicionar(chave_ref, recarregar_cards))

    def confirmar_senha_mestra():
        texto = campo_mestra.text()
        if not texto:
            aviso.setText("Digite a senha mestra.")
            return

        chave_ref[0] = gerar_chave(texto)
        campo_mestra.clear()
        aviso.setText(" ")
        recarregar_cards()
        stack_interno.setCurrentIndex(1)

    botao.clicked.connect(confirmar_senha_mestra)
    campo_mestra.returnPressed.connect(confirmar_senha_mestra)

    stack_interno.addWidget(tela_senha)  
    stack_interno.addWidget(tela_cards)   

    layout_tela = QVBoxLayout()
    layout_tela.setContentsMargins(0, 0, 0, 0)
    layout_tela.addWidget(stack_interno)
    tela.setLayout(layout_tela)
    return tela


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
def validar_primeiro_acesso():
    return keyring_get("cofre-de-senhas", "login") is None


def main():
    inicializar_banco()
    app = QApplication(sys.argv)

    janela = QWidget()
    janela.setWindowTitle("Cofre de Senhas")
    janela.setFixedSize(800, 600)

    stack = QStackedWidget(janela)
    stack.setFixedSize(800, 600)

    stack.addWidget(criar_tela_cadastro(stack, app))  # índice 0
    stack.addWidget(criar_tela_login(stack, app))     # índice 1
    stack.addWidget(criar_tela_menu())                # índice 2

    stack.setCurrentIndex(0 if validar_primeiro_acesso() else 1)

    janela.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()