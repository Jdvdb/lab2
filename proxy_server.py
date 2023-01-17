import socket

BYTES_TO_READ = 4096
HOST = "127.0.0.1"
PORT = 8080


def send_request(host, port, request):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))
    s.send(request)
    s.shutdown(socket.SHUT_WR)
    result = s.recv(BYTES_TO_READ)
    full_result = b'' + result

    while len(result) > 0:
        result = s.recv(BYTES_TO_READ)
        full_result += result

    s.close()
    return full_result


def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            request += data

        response = send_request("www.google.com", 80, request)
        conn.sendall(response)


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind socket to address
        server_socket.bind((HOST, PORT))
        # set to listening mode
        server_socket.listen(2)

        conn, addr = server_socket.accept()

        handle_connection(conn, addr)


start_server()
