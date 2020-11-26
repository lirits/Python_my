import socket
if __name__ == '__main__':
    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)#端口复用
    tcp_server_socket.bind(('',9696))
    tcp_server_socket.listen(128)
    service_client_socket, ip_port = tcp_server_socket.accept()
    recv_data = service_client_socket.recv(1024)
    print(recv_data.decode('utf-8'))
    send_data = "ok".encode("gbk")
    service_client_socket.send(send_data)
    service_client_socket.close()
    tcp_server_socket.close()

