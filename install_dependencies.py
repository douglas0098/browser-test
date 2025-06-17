import os
import platform
import subprocess
import sys


def verificar_python():
    print(f"✔ Python versão: {sys.version}")


def instalar_pip():
    try:
        import pip

        print("✔ pip já está instalado.")
    except ImportError:
        print("❗ pip não encontrado. Tentando instalar...")
        try:
            subprocess.check_call([sys.executable, "-m", "ensurepip"])
            print("✔ pip instalado com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao instalar pip: {e}")
            sys.exit(1)


def instalar_dependencias():
    if not os.path.exists("requirements.txt"):
        print("❌ Arquivo requirements.txt não encontrado.")
        sys.exit(1)

    print("🔧 Instalando dependências do requirements.txt...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Todas as dependências foram instaladas.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        sys.exit(1)


def detectar_sistema():
    so = platform.system()
    print(f"🖥️ Sistema operacional detectado: {so}")
    return so


def main():
    detectar_sistema()
    verificar_python()
    instalar_pip()
    instalar_dependencias()

if __name__ == "__main__":
    main()