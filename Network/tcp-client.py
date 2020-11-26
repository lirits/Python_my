import socket
if __name__ == '__main__':
    ip = input('请输入服务器IP地址')
    # socket.AF_INET : IPV4
    # socket.SOCK_STREAM : TCP
    tcp_clint_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_clint_socket.connect((ip,9696))
    send_data = 'hello'.encode('utf-8')
    tcp_clint_socket.send(send_data)
    recv_data = tcp_clint_socket.recv(1024)
    print(recv_data.decode('utf-8'))
    tcp_clint_socket.close()
