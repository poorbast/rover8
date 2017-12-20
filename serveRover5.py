from flask import Flask, render_template, request, jsonify
import datetime
import sys
import time
import serial
import RPi.GPIO as GPIO
import picamera

sys.path.append(r'/home/pi')

app = Flask(__name__)
print("Grabbing AMA0")
ser = serial.Serial(port = "/dev/ttyAMA0", baudrate=57600)
ser.open()

sleep = .5

@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'Rover 5',
      'time': timeString
      }
   return render_template('main.html', **templateData)
   
@app.route("/cam")
def cam():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'Rover 5',
      'time': timeString
      }
   return render_template('camtest.html', **templateData)
 
@app.route('/test/')
def vid():
   with picamera.PiCamera() as camera:
      stream = io.BytesIO()
      for foo in camera.capture_continuous(stream, format='jpeg'):
         stream.truncate()
         stream.seek(0)
         if process(stream):
            break
  
@app.route("/forward/")
def forward():
  print 'Calling forward A!'
  speed = request.args.get('speed', None)
  print 'Calling forward!' + speed
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(19, GPIO.OUT)
  GPIO.setup(20, GPIO.OUT)
  GPIO.output(19, GPIO.HIGH)
  GPIO.output(20, GPIO.HIGH)
  time.sleep(float(speed))
  GPIO.output(19, GPIO.LOW)
  GPIO.output(20, GPIO.LOW)
  return 'Click.'
  
  
@app.route("/backward/") 
def backward(): 
  print 'Calling backward!' 
  speed = request.args.get('speed', None)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(26, GPIO.OUT)
  GPIO.setup(21, GPIO.OUT)
  GPIO.output(26, GPIO.HIGH)
  GPIO.output(21, GPIO.HIGH)
  time.sleep(float(speed))
  GPIO.output(26, GPIO.LOW)
  GPIO.output(21, GPIO.LOW)
  return 'Click.'


@app.route("/right/")
def right():
  print 'Calling right!'
  speed = request.args.get('speed', None)  
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(20, GPIO.OUT)
  GPIO.setup(26, GPIO.OUT)
  GPIO.output(20, GPIO.HIGH)
  GPIO.output(26, GPIO.HIGH)
  time.sleep(float(speed))
  GPIO.output(20, GPIO.LOW)
  GPIO.output(26, GPIO.LOW)
  return 'Click.'

@app.route("/left/")
def left():
  print 'Calling left!'
  speed = request.args.get('speed', None)    
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(19, GPIO.OUT)
  GPIO.setup(21, GPIO.OUT)
  GPIO.output(19, GPIO.HIGH)
  GPIO.output(21, GPIO.HIGH)
  time.sleep(float(speed))
  GPIO.output(19, GPIO.LOW)
  GPIO.output(21, GPIO.LOW)
  return 'Click.'
  
@app.route("/stop/")
def stop():
  print 'Calling stop!'
  GPIO.output(20, GPIO.LOW)
  GPIO.output(26, GPIO.LOW)
  GPIO.output(19, GPIO.LOW)
  GPIO.output(21, GPIO.LOW)
  return 'Click.'
  

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)

