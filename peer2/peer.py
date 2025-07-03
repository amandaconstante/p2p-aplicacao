import socket
import json
import os
import time
import threading

TRACKER_IP = '127.0.0.1' ### alterar para lab
TRACKER_PORTA = 9010
PEER_PORTA = 10002

def listar_arquivos():
    return [f for f in os.listdir() if f.endswith(".txt")]

def registrar_no_tracker(sock_udp, peer_ip):
    arquivos = listar_arquivos()
    msg = {
        "type": "register",
        "peer": [peer_ip, PEER_PORTA],
        "arquivos": arquivos
    }
    sock_udp.sendto(json.dumps(msg).encode(), (TRACKER_IP, TRACKER_PORTA))
    print(f"[PEER] Registrado no Tracker com arquivos: {arquivos}")

def pedir_peers(sock_udp, peer_ip):
    msg = {
        "type": "get_peers",
        "peer": [peer_ip, PEER_PORTA]
    }
    sock_udp.sendto(json.dumps(msg).encode(), (TRACKER_IP, TRACKER_PORTA))

    dados, _ = sock_udp.recvfrom(4096)
    lista = json.loads(dados.decode())

    print(f"[PEER] Conectado com {len(lista)} peers: ")
    for peer in lista:
        print(f"IP: {peer['peer'][0]}, Porta: {peer['peer'][1]}, Arquivos: {peer['arquivos']}")
    return lista

def servidor_tcp():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('', PEER_PORTA))
    servidor.listen()
    print(f"[TCP] Servidor TCP escutando na porta {PEER_PORTA}...")

    while True:
        conn, addr = servidor.accept()
        nome_arquivo = conn.recv(1024).decode()
        print(f"[TCP] Pedido de '{nome_arquivo}' de {addr}")

        if nome_arquivo in listar_arquivos():
            with open(nome_arquivo, 'rb') as f:
                conn.sendall(f.read())
            print(f"[TCP] Arquivo '{nome_arquivo}' enviado.")
        else:
            conn.sendall(b"ERRO: Arquivo nao encontrado.")
            print(f"[TCP] Arquivo '{nome_arquivo}' NÃO encontrado")
        conn.close()

def atualiza_tracker(sock_udp, peer_ip):
    while True:
        arquivos = listar_arquivos()
        msg = {
            "type": "register",
            "peer": [peer_ip, PEER_PORTA],
            "arquivos": arquivos
        }
        sock_udp.sendto(json.dumps(msg).encode(), (TRACKER_IP, TRACKER_PORTA))
        time.sleep(3)

# conectar outro peer e baixar arquivo mais raro
def baixar_arq_mais_raro(lista_peers, arquivos_atuais):
    contador = {}
    for peer in lista_peers:
        for arq in peer["arquivos"]:
            if arq not in arquivos_atuais:
                contador[arq] = contador.get(arq, 0) + 1

    if not contador:
        print("[DOWNLOAD] Nenhum arquivo novo para baixar")
        return
    
    arquivo_raro = min(contador, key=contador.get)
    print(f"[DOWNLOAD] Arquivo mais raro: {arquivo_raro}")

    # escolhe um peer que tenha o mais raro
    for peer in lista_peers:
        if arquivo_raro in peer["arquivos"]:
            ip, porta = peer["peer"][0], peer["peer"][1]
            try:
                print(f"[DOWNLOAD] Conectado a {ip}:{porta} para pedir '{arquivo_raro}'")
                sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_tcp.connect((ip, porta))
                sock_tcp.sendall(arquivo_raro.encode())
                
                conteudo = b""
                while True:
                    parte = sock_tcp.recv(1024)
                    if not parte:
                        break
                    conteudo += parte

                # salva arquivo recebido
                with open(arquivo_raro, "wb") as f:
                    f.write(conteudo)
                print(f"[DOWNLOAD] Arquivo '{arquivo_raro}' salvo com sucesso!\n")
                sock_tcp.close()
                return # Após um download para
            except Exception as e:
                print(f"[ERRO] Falha ao baixar arquivo de {ip}:{porta}. Erro: {e}")
                continue

def sincroniza_arquivos(sock_tracker, peer_ip):
    while True:
        lista_peers = pedir_peers(sock_tracker, peer_ip)
        arquivos_atuais = listar_arquivos()
        baixar_arq_mais_raro(lista_peers, arquivos_atuais)
        time.sleep(5)

def main():
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.bind(('', 0))

    peer_ip = socket.gethostbyname(socket.gethostname())

    threading.Thread(target=servidor_tcp, daemon=True).start()

    registrar_no_tracker(sock_udp, peer_ip)
    time.sleep(1)
    lista_peers = pedir_peers(sock_udp, peer_ip)

    arquivos_atuais = listar_arquivos()

    threading.Thread(target=atualiza_tracker, args=(sock_udp, peer_ip), daemon=True).start()

    # peers continuam procurando/verificando pacotes das conexões
    threading.Thread(target=sincroniza_arquivos, args=(sock_udp, peer_ip), daemon=True).start()

if __name__ == "__main__":
    main()
    while True:
        time.sleep(1)