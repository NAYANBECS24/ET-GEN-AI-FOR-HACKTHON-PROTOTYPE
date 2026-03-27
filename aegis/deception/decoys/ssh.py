import socket


def run_mock_ssh(host: str = "0.0.0.0", port: int = 2222):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    print(f"Mock SSH server listening on {host}:{port}")
    while True:
        client, addr = sock.accept()
        client.sendall(b"SSH-2.0-OpenSSH_9.2p1 Ubuntu-2\r\n")
        _ = client.recv(1024)
        client.sendall(b"Permission denied, please try again.\n")
        print(f"Captured command attempt from {addr}")
        client.close()


if __name__ == "__main__":
    run_mock_ssh()
