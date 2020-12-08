import cv2
from flask import Flask, render_template, Response

face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./data/haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('./data/mouth.xml')
nose_cascade = cv2.CascadeClassifier('./data/haarcascade_mcs_nose.xml')

cap = cv2.VideoCapture(0)

app = Flask(__name__)

def gen():
    
    while True:
        [nx, ny, nw, nh] = [0, 0, 0, 0]
        NARIZ = [0, 0, 0, 0]
        
        rect, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        nose = nose_cascade.detectMultiScale(gray, 1.2, 25)
        for (nx, ny, nw, nh) in nose:
            cv2.rectangle(img, (nx, ny), (nx + nw, ny + nh), (255, 255, 0), 2)
            NARIZ = [nx, ny, nw, nh]

        eyes = eye_cascade.detectMultiScale(gray, 1.2, 5)
        for (ex, ey, ew, eh) in eyes:
                        
            if NARIZ == [0, 0, 0, 0] :
                cv2.putText(img, "SI TIENE TAPABOCAS" + str(NARIZ), (ex, ey - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
                cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)
            else:
                cv2.putText(img, "NO TIENE TAPABOCAS", (ex, ey - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 1)
                cv2.putText(img, "ALERTA", (10, 25),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        
        cv2.imwrite('caras.jpg', img)
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + open('caras.jpg', 'rb').read() + b'\r\n')
        
    cap.release()

@app.route('/')
def index():
    """Video streaming"""
    return render_template('index.html')
    

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run() 