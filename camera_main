import cv2
import numpy as np
import socket

def kvadrit(img):
    img = cv2.resize(img, (2560, 1440))
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [1440, 0], [0, 1440], [1440, 1440]])

    M = cv2.getPerspectiveTransform(pts1, pts2)

    dst = cv2.warpPerspective(img, M, (1440, 1440))
    return dst


points = ([520, 0], [2050, 0], [350, 1440], [2420, 1440])

last_coords_p1 = (1, 1)
last_coords_p2 = (1, 1)

moving_cnt, not_moving_cnt = 0, 0


cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()
ret, frame2 = cap.read()

frame1 = kvadrit(frame1)
frame2 = kvadrit(frame2)

while cap.isOpened():
    f = 0

    diff = cv2.absdiff(frame1,
                       frame2)


    blur = cv2.GaussianBlur(diff, (9, 9), 0)

    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)


    h_min = np.array((90, 85, 85), np.uint8)
    h_max = np.array((255, 255, 255), np.uint8)

    thresh1 = cv2.inRange(thresh, h_min, h_max)

    сontours, _ = cv2.findContours(thresh1, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)

    if (len(сontours) > 0):

        max = -1
        maxi = 0
        i = 0

        for contour in сontours:
            if (cv2.contourArea(contour) > max):
                max = cv2.contourArea(contour)
                maxi = i
            i+=1

        contour = сontours[maxi]

        if cv2.contourArea(contour) < 700:
            pass
        else:

            (x, y, w, h) = cv2.boundingRect(contour)

            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame1, ("Status: " + "Moving"), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3,
                        cv2.LINE_AA)

            last_coords_p1 = (x, y)
            last_coords_p2 = (x + w, y + h)
            f = 1

            moving_cnt += 1
            not_moving_cnt = 0

        if (moving_cnt > 1000):
            print("Обнаржуно движение:")

            cv2.rectangle(frame1, last_coords_p1, last_coords_p2, (0, 255, 0), 2)
            cv2.imwrite("frame1.png", frame1)
            break

        elif (f == 0):

            if (moving_cnt > 500):
                print("Было обнаржуно движение,:")
                cv2.rectangle(frame1, last_coords_p1, last_coords_p2, (0, 255, 0), 2)
                cv2.imwrite("frame1.png", frame1)
                break

            elif (not_moving_cnt > 300):
                moving_cnt = 0
                not_moving_cnt = 0

            not_moving_cnt += 1

    cv2.imshow("frame1", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    frame2 = kvadrit(frame2)
    if cv2.waitKey(40) == 27:
        break

cap.release()
cv2.destroyAllWindows()

x1, y1 = last_coords_p1
x2, y2 = last_coords_p2
x = (x1 + x2)/2
y = (y1 + y2)/2
k = 300/1440
x = (round(x)/100) * k - 0.5
y = (round(y)/100) * k - 0.5

x, y = 1, 1
text = f"{x} {y}"

HOST = ("", 9090)

server = socket.socket()
server.bind(HOST)
server.listen(1)
print("I am waiting lol")

while True:
    conn, addr = server.accept()
    print("Connected to - ", addr)
    res = text.encode()
    conn.send(res)
    conn.close()
    break

