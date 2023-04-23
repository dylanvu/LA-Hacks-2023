#dog
import cv2
import mediapipe as mp
import numpy as np
import RPi.GPIO as GPIO
import time
import socketio


GPIO.setmode(GPIO.BOARD)
# ledPIN = 11
# this is 11 = GPIO17
GPIO.setup(ledPIN, GPIO.OUT)

serverURL = 'https://distinctwarlikerefactoring.caseytran4.repl.co/'

# sio = socketio.Client()

global switch
switch = True

# @sio.event
# def connect():
#   print("Connected")
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
  min_detection_confidence=0.5,
  min_tracking_confidence=0.5) as pose:
  frameNum = 0

  # boolean state to check
  # functions to debug connection
  print("Ready to begin capture")
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # determine if there are any landmarks, meaning that there are people present
    if results.pose_landmarks is None:
      print("No landmarks found")
      frameNum = 0
    elif switch is True:
      frameNum = frameNum + 1
      print("Person detected - frame " + str(frameNum))
      if frameNum > 5:
          for i in range(50):
              print("Flashing on - " + str(i))
              GPIO.output(ledPIN, True)
              time.sleep(0.05)
              print("Flashing off - " + str(i))
              GPIO.output(ledPIN, False)
              time.sleep(0.05)
          print("Done with flashing")
          frameNum = 0
    else:
      print("Switch is off")

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if switch is True:
      mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # # Flip the image horizontally for a selfie-view display.
    # cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    # if cv2.waitKey(5) & 0xFF == 27:
    #   break

cap.release()
GPIO.cleanup()
  # quit()

# @sio.on("Status: ")
# def receive_data(data):
#     global switch
#     switch = data

# sio.connect(serverURL)