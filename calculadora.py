import tkinter as tk
from tkinter import ttk
import ipaddress

# Criando a janela principal
janela = tk.Tk()
janela.title("Calculadora IP")
janela.geometry("500x400")

# Aplicando estilo ao app
style = ttk.Style()
style.theme_use("clam")  # Tema estilizado
style.configure("TLabel", font=("Helvetica", 12), padding=5, background="#f0f0f0")
style.configure("TButton", font=("Helvetica", 10, "bold"), padding=5, background="#4CAF50", foreground="white")
style.map("TButton", background=[("active", "#45a049")])
style.configure("TEntry", padding=5, font=("Helvetica", 10))

janela.configure(bg="#f0f0f0")  # Cor de fundo da janela

# Labels e Entradas
endereco = ttk.Label(janela, text="Endereço IP:")
endereco.grid(row=0, column=0, padx=20, pady=10, sticky="E")

enderecoip = ttk.Entry(janela, width=30)
enderecoip.grid(row=0, column=1, padx=20, pady=10)

mascara = ttk.Label(janela, text="Máscara Sub-rede:")
mascara.grid(row=1, column=0, padx=20, pady=10, sticky="E")

mascararede = ttk.Entry(janela, width=30)
mascararede.grid(row=1, column=1, padx=20, pady=10)

resultado = ttk.Label(janela, text="", foreground="blue", anchor="center", justify="left", background="#f0f0f0")
resultado.grid(row=3, column=0, columnspan=2, pady=20)

# Função de cálculo
def calcular():
    try:
        ip = enderecoip.get()
        mascara = int(mascararede.get())

        rede = ipaddress.IPv4Network(f"{ip}/{mascara}", strict=False)

        endereco_rede = rede.network_address
        primeiro_host = rede.network_address + 1
        ultimo_host = rede.broadcast_address - 1
        endereco_broadcast = rede.broadcast_address
        host_por_subredes = rede.num_addresses - 2

        primeiro_octeto = int(ip.split('.')[0])
        if 0 <= primeiro_octeto <= 127:
            classe_ip = "Classe A"
        elif 128 <= primeiro_octeto <= 191:
            classe_ip = "Classe B"
        elif 192 <= primeiro_octeto <= 223:
            classe_ip = "Classe C"
        else:
            classe_ip = "IP de Multicast (Classe D) ou de Experimento (Classe E)"

        if ipaddress.ip_address(ip).is_private:
            classificacaoip = "Privado"
        else:
            classificacaoip = "Público"

        bits_subrede = rede.prefixlen - 24 if rede.prefixlen > 24 else 0
        subredes_geradas = 2 ** bits_subrede if bits_subrede > 0 else 1

        resultado.config(text=f"Endereço de Rede: {endereco_rede}\n"
                         f"Primeiro Host: {primeiro_host}\n"
                         f"Último Host: {ultimo_host}\n"
                         f"Endereço Broadcast: {endereco_broadcast}\n"
                         f"Hosts por Sub-rede: {host_por_subredes}\n"
                         f"Classe do IP: {classe_ip}\n"
                         f"Classificação do IP: {classificacaoip}\n"
                         f"Sub-redes Geradas: {subredes_geradas}")

    except ValueError:
        resultado.config(text="Erro: IP ou máscara inválidos!", foreground="red")

# Botão
botao = ttk.Button(janela, text="Calcular", command=calcular)
botao.grid(row=2, column=0, columnspan=2, pady=10)

# Executando a aplicação
janela.mainloop()
