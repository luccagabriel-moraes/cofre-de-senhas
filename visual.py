import sys
import keyring
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

def criar_tela_cadastro(stack: QStackedWidget, app: QApplication):
    tela_cadastro = QWidget()
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
        QLabel, QLineEdit, QPushButton {
            border: none;
        }
    """)


    layout_frame = QVBoxLayout()
    aviso = criar_label_aviso_red()

    label1 = QLabel("cadastre a senha para acessar o cofre")
    label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label1.setFont(QFont("Arial", 10, QFont.Weight.Bold))

    campo_senha1 = QLineEdit()
    campo_senha1.setEchoMode(QLineEdit.EchoMode.Password)
    campo_senha1.setFixedWidth(200)
    campo_senha1.setPlaceholderText("Digite sua senha...")
    campo_senha1.setStyleSheet("""
        QLineEdit {
            border: 1px solid rgba(255, 255, 255, 100);
            border-radius: 5px;
            padding: 5px;
        }
    """)

    campo_senha2 = QLineEdit()
    campo_senha2.setEchoMode(QLineEdit.EchoMode.Password)
    campo_senha2.setFixedWidth(200)
    campo_senha2.setPlaceholderText("Confirme sua senha...")
    campo_senha2.setStyleSheet("""
        QLineEdit {
            border: 1px solid rgba(255, 255, 255, 100);
            border-radius: 5px;
            padding: 5px;
        }
    """)

    botao = QPushButton("Entrar")
    botao.setFixedWidth(200)
    botao.setStyleSheet("""
        QPushButton {
            border: 1px solid rgba(255, 255, 255, 200);
            border-radius: 5px;
            padding: 5px;
        }
    """)
    
    layout_frame.addStretch()
    layout_frame.addWidget(aviso, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(10)
    layout_frame.addWidget(label1, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(10)
    layout_frame.addWidget(campo_senha1, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(5)
    layout_frame.addWidget(campo_senha2, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(5)
    layout_frame.addWidget(botao, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addStretch()
    frame.setLayout(layout_frame)

    layout.addWidget(frame)
    tela_cadastro.setLayout(layout)

    def verificar_senha_cadastro():
        if campo_senha1.text() != campo_senha2.text():
            aviso.setText("As senhas não coincidem.")
            campo_senha1.clear()
            campo_senha2.clear()
        elif campo_senha1.text() == "" or campo_senha2.text() == "":
            aviso.setText("Por favor, preencha ambos os campos.")
        elif len(campo_senha1.text()) < 6:
            aviso.setText("A senha deve ter pelo menos 6 caracteres.")
            campo_senha1.clear()
            campo_senha2.clear()
        else:
            keyring.set_password("cofre-de-senhas", "login", campo_senha1.text())
            stack.setCurrentIndex(1)


    botao.clicked.connect(lambda: verificar_senha_cadastro())
    campo_senha1.returnPressed.connect(lambda: campo_senha2.setFocus())
    campo_senha2.returnPressed.connect(lambda: campo_senha1.setFocus() or verificar_senha_cadastro())
    return tela_cadastro

def criar_label_aviso_red():
    aviso = QLabel(" ")
    aviso.setAlignment(Qt.AlignmentFlag.AlignCenter)
    aviso.setFixedSize(270, 25)
    aviso.setFont(QFont("Arial", 10, QFont.Weight.Bold))
    aviso.setStyleSheet("color: red; border: none;")
    return aviso



def criar_tela_login(stack: QStackedWidget, app: QApplication):
    tela_login = QWidget()
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
        QLabel, QLineEdit, QPushButton {
            border: none;
        }
    """)

    layout_frame = QVBoxLayout()

    aviso = criar_label_aviso_red()

    label = QLabel("senha para acessar o cofre")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setFont(QFont("Arial", 10, QFont.Weight.Bold))

    campo_senha = QLineEdit()
    campo_senha.setEchoMode(QLineEdit.EchoMode.Password)
    campo_senha.setFixedWidth(200)
    campo_senha.setStyleSheet("""
        QLineEdit {
            border: 1px solid rgba(255, 255, 255, 100);
            border-radius: 5px;
            padding: 5px;
        }
    """)

    botao = QPushButton("Entrar")
    botao.setFixedWidth(200)
    botao.setStyleSheet("""
        QPushButton {
            border: 1px solid rgba(255, 255, 255, 200);
            border-radius: 5px;
            padding: 5px;
        }
    """)

    layout_frame.addStretch()
    layout_frame.addWidget(aviso, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(10)
    layout_frame.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(5)
    layout_frame.addWidget(campo_senha, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addSpacing(5)
    layout_frame.addWidget(botao, alignment=Qt.AlignmentFlag.AlignCenter)
    layout_frame.addStretch()
    frame.setLayout(layout_frame)

    layout.addWidget(frame)
    tela_login.setLayout(layout)

    tentativas = [0]

    def verificar_login():
        senha_salva = keyring.get_password("cofre-de-senhas", "login")
        if tentativas[0] >= 3:
            return

        if campo_senha.text() == senha_salva:
            stack.setCurrentIndex(2)
        else:
            tentativas[0] += 1
            restantes = 3 - tentativas[0]
            campo_senha.clear()
            if restantes > 0:
                aviso.setText(f"Senha incorreta. {restantes} tentativa(s) restante(s).")
            else:
                aviso.setText("Número máximo de tentativas atingido.")
                botao.setEnabled(False)
                QTimer.singleShot(3000, app.quit)

    botao.clicked.connect(lambda: verificar_login())
    campo_senha.returnPressed.connect(lambda: verificar_login())

    return tela_login

def criar_tela_menu():
    tela = QWidget()
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label = QLabel("Bem vindo ao cofre!")
    label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
    layout.addWidget(label)
    tela.setLayout(layout)
    return tela

def validar_primeiro_acesso():
    return keyring.get_password("cofre-de-senhas", "login") is None


def main():
    app = QApplication(sys.argv)

    janela = QWidget()
    janela.setWindowTitle("Cofre de Senhas")
    janela.setFixedSize(800, 600)

    stack = QStackedWidget(janela)
    stack.setFixedSize(800, 600)

    stack.addWidget(criar_tela_cadastro(stack, app))          # índice 0
    stack.addWidget(criar_tela_login(stack, app))  # índice 1
    stack.addWidget(criar_tela_menu())              # índice 2

    if validar_primeiro_acesso():
        stack.setCurrentIndex(0)
    else:
        stack.setCurrentIndex(1) 
    janela.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()