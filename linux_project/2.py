import socket
import cv2
import pickle
import struct
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/home/pi/Desktop/output.avi',fourcc, 20.0, (640,480))
class server():
    def __init__(self,host_ip,port):
        socket_address = (host_ip, port)
        server_socket.bind(socket_address)
        server_socket.listen(5)
    def Main(self):
        while True:
            client_socket, addr = server_socket.accept()
            print('GOT CONNECTION FROM:', addr)
            if client_socket:
                vid = cv2.VideoCapture(0)
                while (vid.isOpened()):
                    img, frame = vid.read()

                    a = pickle.dumps(frame)
                    out.write(frame)

                    message = struct.pack("Q", len(a)) + a
                    client_socket.sendall(message)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        client_socket.close()
if __name__ == '__main__':
    try:
        work = server('192.168.68.102',9999)
        work.Main()
    except ConnectionResetError:
        print('连接中断')

