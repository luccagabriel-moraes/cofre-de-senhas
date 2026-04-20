import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QStackedWidget, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


def main():
    app = QApplication(sys.argv)
    janela = QWidget()
    janela.setWindowTitle("Cofre de Senhas")
    janela.setFixedSize(800, 600)

    stack = QStackedWidget(janela)
    stack.setFixedSize(800, 600)

    # Tela de login
    tela_login = QWidget()
    layout_login = QVBoxLayout()
    layout_login.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Frame transparente
    frame = QFrame()
    frame.setFixedSize(350, 250)
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
    frame.setObjectName("frame")

    layout_frame = QVBoxLayout()
    layout_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)

    label = QLabel("senha para acessar o cofre")
    label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    campo_senha = QLineEdit()
    campo_senha.setEchoMode(QLineEdit.EchoMode.Password)
    campo_senha.setFixedWidth(200)

    botao = QPushButton("Entrar")
    botao.setFixedWidth(200)

    layout_frame.addWidget(label)
    layout_frame.addSpacing(10)
    layout_frame.addWidget(campo_senha)
    layout_frame.addSpacing(10)
    layout_frame.addWidget(botao)
    frame.setLayout(layout_frame)

    layout_login.addWidget(frame)
    tela_login.setLayout(layout_login)

    # Tela de senhas
    tela_menu = QWidget()
    layout_menu = QVBoxLayout()
    layout_menu.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label_menu = QLabel("Bem vindo ao cofre!")
    layout_menu.addWidget(label_menu)
    tela_menu.setLayout(layout_menu)

    # Índice das telas
    stack.addWidget(tela_login)
    stack.addWidget(tela_menu)

    def verificar():
        try:
            if campo_senha.text() == "senha123":
                stack.setCurrentIndex(1)
            else:
                label.setText("Senha incorreta. Tente novamente.")
        except Exception as e:
            label.setText(f"Erro: {str(e)}")

    botao.clicked.connect(lambda: verificar())

    janela.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()