import socket
import cv2
import pickle
import struct

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/home/pi/Desktop/output.avi', fourcc, 30, (640, 480))
def Tcp_connect( host_ip, port):
    socket_address = (host_ip, port)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind(socket_address)
    server_socket.listen(5)

def Main(self):
    while True:

        client_socket, addr = self.server_socket.accept()
        print('GOT CONNECTION FROM:', addr)
        if client_socket:
            vid = cv2.VideoCapture(0)
            frame_id = 0
            while (vid.isOpened()):
                img, frame = vid.read()
                a = pickle.dumps(frame)
                # frame_width = 640
                # frame_height = 480
                # frame_id += 1
                # left_x_up = int(frame_width / frame_id)
                # left_y_up = int(frame_height / frame_id)
                # # 文字坐标
                # word_x = left_x_up + 5
                # word_y = left_y_up + 25
                # name = 'opencv monitor'
                # cv2.putText(frame, '%s' % name, (word_x, word_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (55, 255, 155), 2)
                out.write(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    client_socket.close()
if __name__ == '__main__':
    try:
        Tcp_connect('192.168.68.101', 9999)
        Main()
    except ConnectionResetError:
        print('连接中断')


