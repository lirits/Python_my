import socket
import cv2
import pickle
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/home/pi/Desktop/output.avi', fourcc, 30, (640, 480))
class server():
    def __init__(self, host_ip, port):
        socket_address = (host_ip, port)
        server_socket.bind(socket_address)
        server_socket.listen(5)

    def Main(self):
        while True:
            client_socket, addr = server_socket.accept()
            print('GOT CONNECTION FROM:', addr)
            if client_socket:
                vid = cv2.VideoCapture(0)
                frame_id = 0
                while (vid.isOpened()):
                    img, frame = vid.read()

                    a = pickle.dumps(frame)
                    # fps_video=int(vid.get(cv2.CAP_PROP_FPS))
                    # print('fps:',fps_video) 30
                    # frame_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
                    # frame_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    # print(frame_width,frame_height) 640 480
                    frame_width = 640
                    frame_height = 480

                    frame_id += 1
                    left_x_up = int(frame_width / frame_id)
                    left_y_up = int(frame_height / frame_id)
                    right_x_down = int(left_x_up + frame_width / 10)
                    right_y_down = int(left_y_up + frame_height / 10)
                    # 文字坐标
                    word_x = left_x_up + 5
                    word_y = left_y_up + 25
                    # cv2.rectangle(frame, (left_x_up, left_y_up), (right_x_down, right_y_down), (55, 255, 155), 5)
                    name = 'opencv monitor'
                    cv2.putText(frame, '%s' % name, (word_x, word_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (55, 255, 155), 2)
                    out.write(frame)

                    message = struct.pack("Q", len(a)) + a
                    client_socket.sendall(message)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        client_socket.close()


if __name__ == '__main__':
    try:
        work = server('192.168.68.101', 9999)
        work.Main()
    except ConnectionResetError:
        print('连接中断')


