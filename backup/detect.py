import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2

model_path = './efficientdet_lite0_fp32.tflite'

BaseOptions = mp.tasks.BaseOptions
DetectionResult = mp.tasks.components.containers.detections.DetectionResult
ObjectDetector = mp.tasks.vision.ObjectDetector
ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode

def print_result(result: DetectionResult, output_image: mp.Image, timestamp_ms: int):
    print('detection result: {}'.format(result))

options = ObjectDetectorOptions(
    base_options=BaseOptions(model_asset_path='/path/to/model.tflite'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    max_results=5,
    result_callback=print_result)


with ObjectDetector.create_from_options(options) as detector:
    # The detector is initialized. Use it here.
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, image = cap.read()
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

        detector.detect_async(mp_image, frame_timestamp_ms)
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
