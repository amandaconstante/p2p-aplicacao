import socket
import json
import time
import threading

# dicionário
# formato: `{(ip, porta): ["a.txt", "b.txt"]}`
peers = {}
TIMEOUT = 10 # segundos sem atualização do peer, considera desconectado

trackerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
trackerSocket.bind(("0.0.0.0", 9010)) # porta fixa do tracker

print("[TRACKER] Aguardando mensagem na porta 9010...")

def remove_inativos():
    while True:
        agora = time.time()
        inativos = [peer for peer, dados in peers.items() if agora - dados["ultimo_update"] > TIMEOUT]

        for peer in inativos:
            print(f"[TRACKER] Removendo peer inativo: {peer}")
            del peers[peer]
        
        time.sleep(5)

# inicia thread de análise de inatividade de peers
threading.Thread(target=remove_inativos, daemon=True).start()

while True: 
    data, addr = trackerSocket.recvfrom(4096) # dados brutos, ip + prota de origem
    msg = json.loads(data.decode())

    peer_ip = addr[0]
    peer_porta = msg["peer"][1]
    peer_id = (peer_ip, peer_porta)

    if msg["type"] == "register":
        arquivos = msg["arquivos"]
        peers[peer_id] = {
            "arquivos": arquivos,
            "ultimo_update": time.time()
        }
        print(f"[TRACKER] Peer registrado: {peer_id} com arquivos {arquivos}")

    elif msg["type"] == "get_peers":
        solicitante = peer_id
        lista = [
            {"peer": list(k), "arquivos": v["arquivos"]}
            for k, v in peers.items()
            if k != solicitante
        ]
        trackerSocket.sendto(json.dumps(lista[:3]).encode(), addr)
        print(f"[TRACKER] Enviou lista de peers para {solicitante}")