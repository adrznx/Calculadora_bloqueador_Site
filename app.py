from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Caminho do arquivo hosts
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts" if os.name == "nt" else "/etc/hosts"
REDIRECT_IP = "127.0.0.1"

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para bloquear um site
@app.route('/block', methods=['POST'])
def block_site():
    site = request.form['site']

    # Garantir que o site tenha o formato correto
    if not site.startswith("www."):
        site = f"www.{site}"

    # Verificar se o site já está bloqueado
    with open(HOSTS_PATH, 'r') as file:
        hosts_content = file.readlines()

    if any(site in line for line in hosts_content):
        return render_template('message.html', message=f"Site '{site}' já está bloqueado!", back_url='/')

    # Adicionar o site ao arquivo hosts
    with open(HOSTS_PATH, 'a') as file:
        file.write(f"{REDIRECT_IP} {site}\n")

    return render_template('message.html', message=f"Site '{site}' bloqueado com sucesso!", back_url='/')

# Rota para desbloquear um site
@app.route('/unblock', methods=['POST'])
def unblock_site():
    site = request.form['site']

    # Garantir que o site tenha o formato correto
    if not site.startswith("www."):
        site = f"www.{site}"

    # Ler o conteúdo do arquivo hosts
    with open(HOSTS_PATH, 'r') as file:
        hosts_content = file.readlines()

    # Filtrar as linhas que não correspondem ao site
    new_hosts_content = [line for line in hosts_content if site not in line]

    # Escrever o novo conteúdo de volta no arquivo hosts
    with open(HOSTS_PATH, 'w') as file:
        file.writelines(new_hosts_content)

    return render_template('message.html', message=f"Site '{site}' desbloqueado com sucesso!", back_url='/')

if __name__ == "__main__":
    app.run(debug=True)
