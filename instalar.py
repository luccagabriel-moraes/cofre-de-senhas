import sys
import os
import subprocess
import platform

PASTA = os.path.dirname(os.path.abspath(__file__))
SISTEMA = platform.system()


def instalar_dependencias():
    print("📦 Instalando dependências...")
    pacotes = ["cryptography", "PyQt6", "keyring"]
    for pacote in pacotes:
        print(f"   → {pacote}")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", pacote, "--break-system-packages", "--quiet"],
            check=False
        )
    print("✅ Dependências instaladas!\n")


def instalar_linux():
    print("🐧 Criando atalho para Linux...")

    script = os.path.join(PASTA, "iniciar_cofre.sh")
    with open(script, "w") as f:
        f.write(f'#!/bin/bash\ncd "{PASTA}"\nexec /usr/bin/python3 visual.py\n')
    os.chmod(script, 0o755)

    icone = os.path.join(PASTA, "icone.png")
    icone_linha = icone if os.path.exists(icone) else "security-high"

    desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Cofre de Senhas
Comment=Gerenciador de senhas local
Exec={script}
Icon={icone_linha}
Terminal=false
Categories=Utility;Security;
"""

    apps_dir = os.path.expanduser("~/.local/share/applications")
    os.makedirs(apps_dir, exist_ok=True)
    desktop_path = os.path.join(apps_dir, "cofre.desktop")

    with open(desktop_path, "w") as f:
        f.write(desktop_content)
    os.chmod(desktop_path, 0o755)

    # Copia também pra área de trabalho
    for nome_desktop in ["Desktop", "Área de trabalho", "Área De Trabalho"]:
        desktop_dir = os.path.join(os.path.expanduser("~"), nome_desktop)
        if os.path.isdir(desktop_dir):
            import shutil
            shutil.copy(desktop_path, desktop_dir)
            os.chmod(os.path.join(desktop_dir, "cofre.desktop"), 0o755)
            print(f"   → Atalho copiado para {desktop_dir}")
            break

    print(f"   → Atalho criado em {desktop_path}")
    print("✅ Atalho instalado! Procure 'Cofre de Senhas' no menu de aplicativos.\n")


def instalar_windows():
    print("🪟 Criando atalho para Windows...")

    bat = os.path.join(PASTA, "iniciar_cofre.bat")
    with open(bat, "w") as f:
        f.write(f'@echo off\ncd /d "{PASTA}"\npython visual.py\n')

    # Cria .lnk na área de trabalho via PowerShell
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    lnk_path = os.path.join(desktop, "Cofre de Senhas.lnk")
    icone = os.path.join(PASTA, "icone.ico")
    icone_linha = f'$s.IconLocation = "{icone}"' if os.path.exists(icone) else ""

    ps_script = f"""
$ws = New-Object -ComObject WScript.Shell
$s = $ws.CreateShortcut("{lnk_path}")
$s.TargetPath = "{bat}"
$s.WorkingDirectory = "{PASTA}"
{icone_linha}
$s.Save()
"""
    subprocess.run(["powershell", "-Command", ps_script], check=False)
    print(f"   → Atalho criado em {lnk_path}")
    print("✅ Atalho instalado! O ícone apareceu na sua área de trabalho.\n")


def main():
    print("=" * 50)
    print("       🔐 Instalador — Cofre de Senhas")
    print("=" * 50)
    print(f"Sistema detectado: {SISTEMA}\n")

    instalar_dependencias()

    if SISTEMA == "Linux":
        instalar_linux()
    elif SISTEMA == "Windows":
        instalar_windows()
    else:
        print(f"⚠️  Sistema '{SISTEMA}' não suportado pelo instalador.")
        print("   Rode manualmente: pip install cryptography PyQt6 keyring")
        print("   Depois: python3 visual.py")

    print("=" * 50)
    print("Instalação concluída! Para abrir o app:")
    if SISTEMA == "Linux":
        print("→ Pelo menu de aplicativos: procure 'Cofre de Senhas'")
        print("→ Pelo terminal: python3 visual.py")
    elif SISTEMA == "Windows":
        print("→ Pelo ícone na área de trabalho")
        print("→ Pelo terminal: python visual.py")
    print("=" * 50)


if __name__ == "__main__":
    main()
