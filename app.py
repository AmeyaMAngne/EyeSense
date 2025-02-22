from flask import Flask, render_template, Response
import cv2
import pyttsx3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def gen_frames():
    video = cv2.VideoCapture(0)
    facedetect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("Trainer.yml")

    name_list = ["", "Ameya"]

    engine = pyttsx3.init()

    while True:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facedetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if conf > 50:
                name = name_list[serial]
                cv2.putText(frame, name, (x, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)
                engine.say("Recognized person is " + name)
                engine.runAndWait()
            else:
                cv2.putText(frame, "Unknown", (x, y - 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)
                engine.say("Unknown person")
                engine.runAndWait()

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(debug=True)
