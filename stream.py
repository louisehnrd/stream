from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, send, emit
from time import sleep
import io
import os
from picamera2 import Picamera2
from picamera2.outputs import CircularOutput
from picamera2.encoders import H264Encoder

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,threading=True)

@app.route('/')
def index():
    return render_template('stream.html')

@socketio.on('stream')
def start_stream(period):
    camera = Picamera2()
    stream = io.BytesIO()
    encoder = H264Encoder()
    output = CircularOutput(buffersize = 150) # Flux circulaire pour une diffusion en continu
    output.fileoutput = "file.h264"
    camera.start_recording(encoder,output)
    emit('streaming_started',{'output': output.fileoutput},broadcast=True)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    send(message, broadcast=True)

@socketio.on('image1')
def handle_image(period):
    print('received period: ' + period)
    src = file = url_for('static', filename='Untitled.jpeg')
    sleep(int(period))
    emit('image',(src,period),broadcast=True)

@socketio.on('image2')
def handle_image(period):
    print('received period: ' + period)
    src = file = url_for('static', filename='Untitled2.jpeg')
    sleep(int(period))
    emit('img',(src,period),broadcast=True)
    

"""
@socketio.on('message')
def handle_test_message(data):
    while True :
        print('received message: ' + data['data'])
        emit('message_back', {'data': 'Test response sent'})
        sleep(5)

@socketio.on('picture')
def send_picture(picture):
    file = os.path.join(os.path.expanduser("~"),"stream", "static", picture['name'])
    with open(file, 'rb') as f:
        print('ouvert')
        image_data = f.read()
        emit('image', {'data': image_data})
"""

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5000)
