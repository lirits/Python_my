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
            classfier = cv2.CascadeClassifier(
                '/Users/liritwang/Google Drive/Code/haarcascades/haarcascade_frontalface_default.xml')
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
            grey = cv2.cvtColor(frame,cv2.COLOR_BGR2BGRA)
            faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
            num = 0
            path_name = '/Users/liritwang/Downloads/image'
            catch_pic_num =100
            color = (0, 255, 0)
            if len(faceRects) > 0:  # 大于0则检测到人脸
                for faceRect in faceRects:  # 单独框出每一张人脸
                    x, y, w, h = faceRect

                # 将当前帧保存为图片
                    img_name = "%s/%d.jpg" % (path_name, num)
                    # print(img_name)
                    image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                    cv2.imwrite(img_name, image, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

                    num += 1
                    if num > (catch_pic_num):  # 如果超过指定最大保存数量退出循环
                        break

                    # 画出矩形框
                    cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)

                    # 显示当前捕捉到了多少人脸图片了，这样站在那里被拍摄时心里有个数，不用两眼一抹黑傻等着
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, 'face_num:%d' % (num), (x + 30, y + 30), font, 1, (255, 0, 255), 4)
            if num > (catch_pic_num): break

            # 显示图像
            cv2.imshow('test', frame)
            c = cv2.waitKey(10)
            if c & 0xFF == ord('q'):
                break

if __name__ == '__main__':
    work = Main('192.168.68.101',9999)
    work.tcpConnect()
    work.camera()