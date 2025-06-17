import os


def get_html_path(file_name):
    """Retorna o caminho absoluto para arquivos HTML em assets/html/"""
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "assets", "html", file_name)
    )


def get_html_temp_path(file_name):
    """Retorna o caminho absoluto para arquivos HTML em assets/html/"""
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "assets", "html", "templates", file_name
        )
    )


def ensure_login_page_exists():
    """Verifica e cria o arquivo login.html caso não exista"""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    html_dir = os.path.join(root_dir, "assets", "html")
    login_path = os.path.join(html_dir, "login.html")

    if not os.path.exists(login_path):
        os.makedirs(html_dir, exist_ok=True)
        with open(login_path, "w", encoding="utf-8") as f:
            f.write(_default_login_html())
        print(f"[✔] Arquivo criado: {login_path}")

    return login_path.replace("\\", "/")


def read_html_template(filename):
    """Lê o conteúdo de um arquivo HTML de template"""
    template_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "assets", "html", "templates")
    )
    path = os.path.join(template_dir, filename)

    if not os.path.isfile(path):
        raise FileNotFoundError(f"Template HTML não encontrado: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _default_login_html():
    """Conteúdo HTML padrão da página de login"""
    return read_html_template("login_template.html")
