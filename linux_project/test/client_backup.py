import socket
import cv2
import pickle
import struct
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/Users/liritwang/Downloads/image/output.avi',fourcc, 30.0, (640,480))
class Main():
    def __init__(self,host_ip,port):
        self.host_ip = host_ip
        self.port = port
        self.frame_id = 0
    def tcpConnect(self):
        client_socket.connect((self.host_ip, self.port))
        self.data = b""
        self.payload_size = struct.calcsize("Q")
    def camera(self):
        while True:
            while len(self.data) < self.payload_size:
                packet = client_socket.recv(4 * 1024)
                if not packet: break
                self.data += packet
            packed_msg_size = self.data[:self.payload_size]

            self.data = self.data[self.payload_size:]

            msg_size = struct.unpack("Q", packed_msg_size)[0]


            while len(self.data) < msg_size:
                self.data += client_socket.recv(4 * 1024)
            frame_data = self.data[:msg_size]
            self.data = self.data[msg_size:]
            frame = pickle.loads(frame_data)
            frame_width = 640
            frame_height = 480

            self.frame_id += 1
            left_x_up = int(frame_width / self.frame_id)
            left_y_up = int(frame_height / self.frame_id)

            # 文字坐标
            word_x = left_x_up + 5
            word_y = left_y_up + 25

            name = 'opencv monitor'
            cv2.putText(frame, '%s' % name, (word_x, word_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (55, 255, 155), 2)
            out.write(frame)

            cv2.imshow("Zhang xu", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        client_socket.close()
if __name__ == '__main__':
    work = Main('192.168.68.101',9999)
    work.tcpConnect()
    work.camera()