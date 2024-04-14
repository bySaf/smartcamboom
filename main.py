from flask import Flask, render_template, Response, url_for
from cam_main import cama
import cv2
from threading import Thread
from flask_sock import Sock
from cam_main import detect_object
from nen import bezdarnost
from cam_main import getcoord

ans = 0

app = Flask(__name__)
sock = Sock(app)

cap = cv2.VideoCapture(0)
cnt = 0
@sock.route('/echo')
def echo(sock):
    global cnt
    while True:
        if (detect_object()[0] == 1):
            if (cnt == 1): sock.send("Было обнаружено движение, желаете ли вы отправить коптер для проверки?")
            cnt+=1
            data = sock.receive()
            print(data, type(data))
            if (data == "YES"):
                sock.send("pon")
                print("zbalo", detect_object()[1], detect_object()[2])
                x1, x2 = getcoord(detect_object()[1], detect_object()[2])
                thread1 = Thread(target=bezdarnost, args=(x1, x2))
                thread1.start()

            else:
                sock.send("ni pon")

def capture_video():

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

def capture_video_cv():

    while True:

        ret, frame = cap.read()
        frame2 = cama(frame)
        frame2 = cv2.resize(frame2, (720, 720))
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame2)
        frame2 = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n')
    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(capture_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_cv')
def video_feed_cv():
    return Response(capture_video_cv(), mimetype='multipart/x-mixed-replace; boundary=frame')


# def video_feed_cp():

if __name__ == '__main__':
    app.run(debug=True)

