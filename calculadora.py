import tkinter as tk
from tkinter import ttk
import ipaddress

# Criando a janela principal
janela = tk.Tk()
janela.title("Calculadora IP")
janela.geometry("400x300")

endereco = tk.Label(janela, text="Endereço Ip: ")
endereco.grid(row=0, column=0, padx=50, pady=10)

enderecoip = tk.Entry(janela, width=30)
enderecoip.grid(row=0, column=1, padx=10, pady=10)

mascara = tk.Label(janela, text="Máscara sub-rede")
mascara.grid(row=1, column=0, padx=10, pady=10)

mascararede = tk.Entry(janela, width=30)
mascararede.grid(row=1, column=1, padx=10, pady=10)

resultado = tk.Label(janela, text="", fg="blue")
resultado.grid(row=3, column=0, columnspan=2, pady=10)


def calcular():
    try:
        ip = enderecoip.get()
        mascara = int(mascararede.get())

        rede = ipaddress.IPv4Network(f"{ip}/{mascara}", strict=False)

        endereco_rede = rede.network_address
        primeiro_host = rede.network_address + 1
        ultimo_host = rede.broadcast_address -1
        endereco_broadcast = rede.broadcast_address
        host_por_subredes = rede.num_addresses -2

        primeiro_octeto = int(ip.split('.')[0])
        if 0 <= primeiro_octeto <= 127:
            classe_ip = "Classe A"
        elif 128 <= primeiro_octeto <= 191:
            classe_ip = "Classe B"
        elif 192 <= primeiro_octeto <= 233:
            classe_ip = "Classe C"
        else:
            classe_ip = "IP de Multicast (Classe D) ou de Experimento (Classe E)"

        if ipaddress.ip_address(ip).is_private:
            classificacaoip = "Privado"
        else:
            classificacaoip = "Público"

        bits_subrede = rede.prefixlen -24
        subredes_geradas = 2 ** bits_subrede


        resultado.config(text=f"Endereço de Rede: {endereco_rede}\n"
                         f"Primeiro Host: {primeiro_host}\n"
                         f"Ultimo Host: {ultimo_host}\n"
                         f"Endereço Broadcast: {endereco_broadcast}\n"
                         f"Host por sub redes: {host_por_subredes}\n"
                         f"Classe do IP: {classe_ip}\n"
                         f"Classificação do IP: {classificacaoip}\n"
                         f"Sub Redes Geradas: {subredes_geradas}"
                         )
        
    except ValueError:
        resultado.config(text="Erro: IP ou máscara inválidos!")

        

botao = tk.Button(janela, text="Calcular", width=20, command=calcular)
botao.grid(row=2, column=1, columnspan=2, pady=10)


janela.mainloop()
