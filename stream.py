from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, send, emit
from time import sleep
import io
import os
from picamera2 import Picamera2
from picamera2.outputs import CircularOutput, FfmpegOutput
from picamera2.encoders import H264Encoder
import ffmpeg
import subprocess

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,threading=True)
camera = None
output = None

@app.route('/')
def index():
    return render_template('stream.html')

@socketio.on('stream')
def start_stream(period):
    global camera, output
    
    if camera and output:
        output.fileoutput = "file.h264"
        output.start()
        sleep(5)
        output.stop()
        output_file_h264 = str(output.fileoutput)[str(output.fileoutput).find("name='") + 6 : str(output.fileoutput).rfind("'>")]
        output_file_mp4 = 'file.mp4'
        #ffmpeg.input(output_file_h264).output(output_file_mp4, vcodec='copy').run()
        command = f'ffmpeg -i {output_file_h264} -c:v copy -y {output_file_mp4}'
        subprocess.run(command, shell=True)
        with open(output_file_mp4, 'rb') as file:
            video_data = file.read()
        emit('streaming_started', {'video_data': video_data}, broadcast=True)
    else :
        camera = Picamera2()
        stream = io.BytesIO()
        encoder = H264Encoder()
        output = CircularOutput() # Flux circulaire pour une diffusion en continu
        camera.start_recording(encoder,output)
        #output.fileoutput=FfmpegOutput("file.mp4", audio=True)
        output.fileoutput = "file.h264"
        output.start()
        sleep(5)
        output.stop()
        """
        output=str(output.fileoutput)[str(output.fileoutput).find("name='") + 6 : str(output.fileoutput).rfind("'>")]
        with open(output, 'rb') as file:
            video_data = file.read()
        """
        output_file_h264 = str(output.fileoutput)[str(output.fileoutput).find("name='") + 6 : str(output.fileoutput).rfind("'>")]
        output_file_mp4 = 'file.mp4'
        #ffmpeg.input(output_file_h264).output(output_file_mp4, vcodec='copy').run()
        command = f'ffmpeg -i {output_file_h264} -c:v copy -y {output_file_mp4}'
        subprocess.run(command, shell=True)
        with open(output_file_mp4, 'rb') as file:
            video_data = file.read()
        emit('streaming_started', {'video_data': video_data}, broadcast=True)


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
