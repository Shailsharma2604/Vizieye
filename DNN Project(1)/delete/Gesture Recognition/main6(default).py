import cv2
import mediapipe as mp
import numpy as np
from AppOpener import open
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Mediapipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Dictionary to map recognized gestures to specific apps
apps = {
    'A': 'whatsapp',  # Opens WhatsApp for 'A'
    'B': 'telegram',  # Opens Telegram for 'B'
    'C': 'chrome'     # Opens Chrome for 'C'
}

# Volume control setup using pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get volume range
minVol, maxVol, _ = volume.GetVolumeRange()

# Function to calculate Euclidean distance between two points
def calculate_distance(point1, point2):
    return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# Function to recognize hand gestures based on landmarks of both hands
def recognize_gesture(hand1, hand2):
    if hand1 and hand2:
        # Get important landmarks
        hand1_thumb_tip = hand1.landmark[4]
        hand1_index_tip = hand1.landmark[8]
        hand2_thumb_tip = hand2.landmark[4]
        hand2_index_tip = hand2.landmark[8]

        # Gesture A: Thumbs and Index fingers of both hands close together
        thumb_distance = calculate_distance(hand1_thumb_tip, hand2_thumb_tip)
        index_distance = calculate_distance(hand1_index_tip, hand2_index_tip)

        if thumb_distance < 0.1 and index_distance < 0.1:
            return 'A'  # Gesture "A"

        # Gesture B: Hands far apart
        if thumb_distance > 0.4 and index_distance > 0.4:
            return 'B'  # Gesture "B"

        # Gesture C: Hands forming a "C" shape with both thumbs spread out
        thumb1_to_index1 = calculate_distance(hand1_thumb_tip, hand1_index_tip)
        thumb2_to_index2 = calculate_distance(hand2_thumb_tip, hand2_index_tip)

        if thumb1_to_index1 > 0.2 and thumb2_to_index2 > 0.2:
            return 'C'  # Gesture "C"
    
    if hand1:  # Use thumb and index finger distance for volume control
        thumb_tip = hand1.landmark[4]
        index_tip = hand1.landmark[8]
        thumb_to_index_distance = calculate_distance(thumb_tip, index_tip)
        return thumb_to_index_distance  # Return distance for volume control

    return None

# Function to adjust volume based on thumb and index finger distance
def adjust_volume(distance):
    global volume, minVol, maxVol
    normalized_distance = np.clip(distance, 0.05, 0.3)  # Normalizing the distance
    vol = np.interp(normalized_distance, [0.05, 0.3], [minVol, maxVol])  # Map the distance to volume level
    volume.SetMasterVolumeLevel(vol, None)
    print(f"Volume adjusted: {vol}")

# Function to trigger app opening based on recognized gesture
def trigger_app(gesture, last_opened_app):
    if gesture in apps and last_opened_app != apps[gesture]:
        open(apps[gesture], match_closest=True)  # Open the app
        print(f'Opening {apps[gesture]}...')
        return apps[gesture]
    return last_opened_app

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Mediapipe Hands model
with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2) as hands:
    last_gesture = None
    consecutive_gesture_frames = 0
    last_opened_app = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Flip the frame for natural hand movement
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame.shape

        # Process the hand landmarks
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            hand1 = results.multi_hand_landmarks[0] if len(results.multi_hand_landmarks) > 0 else None
            hand2 = results.multi_hand_landmarks[1] if len(results.multi_hand_landmarks) > 1 else None

            # Draw landmarks for both hands
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Recognize gesture when both hands are present or adjust volume with one hand
            if hand1 and hand2:
                gesture = recognize_gesture(hand1, hand2)
                if isinstance(gesture, str):  # Gesture for app control
                    if gesture == last_gesture:
                        consecutive_gesture_frames += 1
                    else:
                        consecutive_gesture_frames = 0
                        last_gesture = gesture

                    # Only trigger app after stable gesture detection over 10 frames
                    if consecutive_gesture_frames > 10:
                        print(f"Recognized Gesture: {gesture}")
                        last_opened_app = trigger_app(gesture, last_opened_app)
                        consecutive_gesture_frames = 0
            elif hand1:  # Adjust volume if only one hand is detected
                distance = recognize_gesture(hand1, None)
                if isinstance(distance, float):  # Volume control
                    adjust_volume(distance)

        # Show frame
        cv2.imshow('Hand Gesture App Controller & Volume Control', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
