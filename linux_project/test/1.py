import socket
import cv2
import pickle
import struct
import threading

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/home/pi/Desktop/output.avi', fourcc, 30, (640, 480))
def Main():
    while True:
        #if client_socket:
        vid = cv2.VideoCapture(0)
        while (vid.isOpened()):
            img, frame = vid.read()
            a = pickle.dumps(frame)
            out.write(frame)
            if client_socket:
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)
            else:
                continue
                # key = cv2.waitKey(1) & 0xFF
                # if key == ord('q'):
                #     client_socket.close()
    server_socket.close()
if __name__ == '__main__':
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        server_socket.bind(('',9999))
        server_socket.listen(5)
        while True:
            client_socket, addr = server_socket.accept()
            print('GOT CONNECTION FROM:', addr)
            test = threading.Thread(target=Main())
            test.setDaemon(True)
            test.start()
    except ConnectionResetError:
        print('连接中断')


