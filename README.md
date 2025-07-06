# Aplicação P2P com Sockets
### _Trabalho final - Disciplina de Redes de Computadores_

Este projeto implementa uma aplicação peer-to-peer (P2P) para compartilhamento de arquivos .txt entre peers, utilizando sockets UDP e TCP em Python.

### Procedimentos para execução do programa

**1. Ferramentas necessárias:**
- Python 3.x instalado nas máquinas (qualquer versão recente).
- 4 máquinas com mesma rede local funcional.
- Cada peer deve ter no diretório arquivos `.txt` para compartilhar.

**2. Download do projeto:**

   - No diretório: `https://github.com/amandaconstante/p2p-aplicacao` realize o passo Download Zip.
   - Coloque o `tracker.py` em uma máquina (servidor).
   - Coloque os diretórios `peer1`, `peer2` e `peer3` em outras 3 máquinas distintas.

**3. Passos para rodar o servidor (Tracker):**
   - Acesse o terminal na máquina do servidor.
   - Vá até o diretório onde está o `tracker.py`.
   - Execute o comando:

     ```bash
     python tracker.py
     ```

   - O Tracker ficará escutando conexões na porta 9010.

**4. Passos para rodar cada Peer:**
   - Em cada máquina de peer, vá até o terminal do diretório do respectivo peer (`peer1/`, `peer2/` e `peer3/`).
   - Verifique se existem arquivos `.txt` no diretório.
   - Execute:

     ```bash
     python peer.py
     ```

   - Cada peer:
     - Se registra no Tracker via UDP.
     - Cria um servidor TCP para envio de arquivos.
     - Se conecta a outros peers (conexão TCP) para baixar o arquivo mais raro.
     - Atualiza sua lista de arquivos periodicamente ao Tracker.
     - Sincroniza downloads a cada 5 segundos.
       
---

## Observações

- O IP do `TRACKER_IP` nos scripts dos peers deve ser ajustado para o IP real da máquina que executa o `tracker.py`.
- As portas dos peers (`PEER_PORTA`) devem ser diferentes entre si (ex: 10001, 10002, 10003).
- Os testes devem ser realizados com arquivos `.txt` diferentes entre os peers inicialmente, para permitir a troca.



