import cv2
import numpy as np

fg = 0


d_obj = [0, (0, 0), (0, 0)]

def kvadrit(img) -> cv2.warpPerspective:
    points = ([582, 107], [1429, 28], [550, 963], [1655, 871])
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [1080, 0], [0, 1080], [1080, 1080]])

    M = cv2.getPerspectiveTransform(pts1, pts2)

    dst = cv2.warpPerspective(img, M, (1080, 1080))
    return dst

def detect_object():
    global d_obj
    return d_obj

def getcoord(l1, l2):
    x1, y1 = l1
    x2, y2 = l2

    x = (x1 + x2) / 2
    y = (y1 + y2) / 2

    k = 200 / 1080
    k1 = 200 / 1080
    x_coord = (round(x) / 100) * k
    y_coord = (round(y) / 100) * k1

    return round(x_coord, 2), round(2 - y_coord, 2)



"""
HOST = ("", 9091)

server = socket.socket()
server.bind(HOST)
server.listen(1)
"""

last_coords_p1 = (1, 1)
last_coords_p2 = (1, 1)

moving_cnt, not_moving_cnt = 0, 0
cnt = 0
def cama(frame1):


    global moving_cnt, not_moving_cnt, last_coords_p2 , last_coords_p1, cnt, d_obj

    frame1 = kvadrit(frame1)
    #frame2 = kvadrit(frame2)

    h_min = np.array((90, 85, 85),
                     np.uint8)

    h_max = np.array((255, 255, 255),
                     np.uint8)

    hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

    thresh1 = cv2.inRange(hsv1, h_min, h_max)

    #hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

    #thresh2 = cv2.inRange(hsv2, h_min, h_max)

    #print(moving_cnt, not_moving_cnt)

    # frame1 = cv2.cvtColor(thresh1, cv2.COLOR_GRAY2BGR)

    # frame2 = cv2.cvtColor(thresh2, cv2.COLOR_HSV2BGR)

    #diff = cv2.absdiff(thresh1, thresh2)

    # gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    #blur = cv2.GaussianBlur(diff, (9, 9), 1)

    #_, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    #dilated = cv2.dilate(thresh, None,iterations=5)


    print(moving_cnt, not_moving_cnt)
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
            i += 1

        contour = сontours[maxi]

        if cv2.contourArea(contour) < 700:
            return frame1
        else:

            (x, y, w, h) = cv2.boundingRect(contour)

            last_coords_p1 = (x, y)
            last_coords_p2 = (x + w, y + h)

            cv2.rectangle(frame1, last_coords_p1, last_coords_p2, (0, 255, 0), 2)

            f = 1

            moving_cnt += 1
            not_moving_cnt = 0

        if (moving_cnt > 50):
            d_obj = [1, last_coords_p1, last_coords_p1]


            cv2.rectangle(frame1, last_coords_p1, last_coords_p2, (0, 255, 0), 2)
            print()


        elif (f == 0):

            if (moving_cnt > 30):
                d_obj = [1, last_coords_p1, last_coords_p1]

                cv2.rectangle(frame1, last_coords_p1, last_coords_p2, (0, 255, 0), 2)
                #cv2.imwrite("frame1.png", frame1)



            elif (not_moving_cnt > 15):
                moving_cnt = 0
                not_moving_cnt = 0

            not_moving_cnt += 1

    return frame1

