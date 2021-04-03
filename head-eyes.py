"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
import dlib
import move

from gaze_tracking import GazeTracking
from Headpose_Detection import headpose

# _face_detector is used to detect faces
_face_detector = dlib.get_frontal_face_detector()

# _predictor is used to get facial landmarks of a given face
model_path = './gaze_tracking/trained_models/shape_predictor_68_face_landmarks.dat'
_predictor = dlib.shape_predictor(model_path)

# Initialize head pose detection
hpd = headpose.HeadposeDetection(1, model_path)

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

control = move.Move()

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    frame = cv2.flip(frame, 1)
    # landmark Detection
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _faces = _face_detector(frame_gray, 0)
    if len(_faces) > 0 and _faces[0].left() > 0 and _faces[0].right() < frame.shape[1] and _faces[0].top() > 0:
        _landmarks = _predictor(frame_gray, _faces[0])

        frame, angles = hpd.process_image(frame, im_gray=frame_gray, faces=_faces, landmarks=_landmarks, beta=0.85)
        control.move(angles)
        
        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame_gray, faces=_faces, landmarks=_landmarks)

        frame = gaze.annotated_frame(frame)
        text = ""

        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"

        cv2.putText(frame, text, (190, 60), cv2.FONT_HERSHEY_DUPLEX, 0.8, (147, 58, 31), 2)

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (190, 90), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 255), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (190, 125), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 255), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
