import socket
import json
# import threading

# dicionário
# formato: `{(ip, porta): ["a.txt", "b.txt"]}`
peers = {}

#def handle_tracker():
trackerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
trackerSocket.bind(("0.0.0.0", 9010)) # porta fixa do tracker

print("[TRACKER] Aguardando mensagem na porta 9010...");

while True: 
    data, addr = trackerSocket.recvfrom(4096)
    msg = json.loads(data.decode())

    if msg["type"] == "register":
        peer_id = tuple(msg["peer"])
        arquivos = msg["arquivos"]
        peers[peer_id] = arquivos
        print(f"[TRACKER] Peer registrado: {peer_id} com arquivos {arquivos}")

    elif msg["type"] == "get_peers":
        solicitante = tuple(msg["peer"])
        lista = [
            {"peer": list(k), "arquivos": v}
            for k, v in peers.items()
            if k != solicitante
        ]
        trackerSocket.sendto(json.dumps(lista[:3]).encode(), addr)

# roda tracker em uam threar (poderia ser o main direto tb)
# threading.Thread(target=handle_tracker).start()