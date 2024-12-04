# import cv2
# import mediapipe as mp
# import numpy as np
# from AppOpener import open
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# import pyautogui
# import os

# # Mediapipe setup
# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils

# # Dictionary to map recognized gestures to specific apps
# apps = {
#     'A': 'whatsapp',  # Opens WhatsApp for 'A'
#     'B': 'telegram',  # Opens Telegram for 'B'
#     'C': 'chrome'     # Opens Chrome for 'C'
# }

# # Volume control setup using pycaw
# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))

# # Get volume range
# minVol, maxVol, _ = volume.GetVolumeRange()

# # Function to calculate Euclidean distance between two points
# def calculate_distance(point1, point2):
#     return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# # Function to recognize hand gestures
# def recognize_gesture(hand1, hand2):
#     if hand1 and hand2:
#         # Gesture A: Both hands, thumbs and index fingers close together (Open Apps)
#         thumb_distance = calculate_distance(hand1.landmark[4], hand2.landmark[4])
#         index_distance = calculate_distance(hand1.landmark[8], hand2.landmark[8])
        
#         if thumb_distance < 0.1 and index_distance < 0.1:
#             return 'A'
        
#         # Gesture B: Hands far apart (Next media track / Shutdown)
#         if thumb_distance > 0.4 and index_distance > 0.4:
#             return 'B'

#         # Gesture C: Hands forming "C" shape (Previous track)
#         thumb1_to_index1 = calculate_distance(hand1.landmark[4], hand1.landmark[8])
#         thumb2_to_index2 = calculate_distance(hand2.landmark[4], hand2.landmark[8])
        
#         if thumb1_to_index1 > 0.2 and thumb2_to_index2 > 0.2:
#             return 'C'

#     if hand1:
#         # Gesture D: Thumb and index finger close together (Volume control)
#         thumb_tip = hand1.landmark[4]
#         index_tip = hand1.landmark[8]
#         thumb_to_index_distance = calculate_distance(thumb_tip, index_tip)

#         if thumb_to_index_distance < 0.1:
#             return 'D', thumb_to_index_distance  # Also return distance for volume adjustment

#         # Gesture E: Thumb and index finger forming "L" shape (Brightness control)
#         if hand1.landmark[4].x < hand1.landmark[8].x:  # Thumb is left of index finger
#             return 'E', thumb_to_index_distance

#         # Gesture F: Index finger pointing upward (Mouse control)
#         if hand1.landmark[8].y < hand1.landmark[6].y:
#             return 'F', None

#         # Gesture G: Thumb and index quick tap (Mouse click)
#         if calculate_distance(thumb_tip, index_tip) < 0.05:
#             return 'G', None
        
#         # Gesture H: Palms together (System Lock)
#         if hand2 and calculate_distance(hand1.landmark[0], hand2.landmark[0]) < 0.05:
#             return 'H', None

#     return None, None

# # Function to adjust volume based on thumb and index finger distance
# def adjust_volume(distance):
#     global volume, minVol, maxVol
#     vol = np.interp(distance, [0.05, 0.3], [minVol, maxVol])
#     volume.SetMasterVolumeLevel(vol, None)
#     print(f"Volume adjusted: {vol}")

# # Function to adjust brightness based on thumb and index finger distance
# def adjust_brightness(distance):
#     brightness = int(np.interp(distance, [0.05, 0.3], [0, 100]))
#     os.system(f"powershell (Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{brightness})")
#     print(f"Brightness adjusted: {brightness}%")

# # Function to control mouse movement and clicking
# def control_mouse(hand):
#     if hand:
#         screen_width, screen_height = pyautogui.size()
#         x, y = int(hand.landmark[8].x * screen_width), int(hand.landmark[8].y * screen_height)
#         pyautogui.moveTo(x, y)
#         print(f"Mouse moved to: {x}, {y}")

# # Trigger app based on gesture
# def trigger_app(gesture, last_opened_app):
#     if gesture in apps and last_opened_app != apps[gesture]:
#         open(apps[gesture], match_closest=True)
#         print(f"Opening {apps[gesture]}...")
#         return apps[gesture]
#     return last_opened_app

# # Webcam setup
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)

# with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2) as hands:
#     last_gesture = None
#     consecutive_gesture_frames = 0
#     last_opened_app = None

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame = cv2.flip(frame, 1)
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = hands.process(frame_rgb)

#         if results.multi_hand_landmarks:
#             hand1 = results.multi_hand_landmarks[0] if len(results.multi_hand_landmarks) > 0 else None
#             hand2 = results.multi_hand_landmarks[1] if len(results.multi_hand_landmarks) > 1 else None

#             for hand_landmarks in results.multi_hand_landmarks:
#                 mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#             gesture, thumb_to_index_distance = recognize_gesture(hand1, hand2)

#             if gesture:
#                 if gesture == last_gesture:
#                     consecutive_gesture_frames += 1
#                 else:
#                     consecutive_gesture_frames = 0
#                     last_gesture = gesture

#                 if consecutive_gesture_frames > 10:
#                     print(f"Recognized Gesture: {gesture}")
#                     if gesture in ['A', 'B', 'C']:  # Open apps/media control
#                         last_opened_app = trigger_app(gesture, last_opened_app)
#                     elif gesture == 'D' and thumb_to_index_distance:
#                         adjust_volume(thumb_to_index_distance)
#                     elif gesture == 'E' and thumb_to_index_distance:
#                         adjust_brightness(thumb_to_index_distance)
#                     elif gesture == 'F':
#                         control_mouse(hand1)
#                     elif gesture == 'H':
#                         os.system("rundll32.exe user32.dll,LockWorkStation")

#                     consecutive_gesture_frames = 0

#         cv2.imshow('Gesture Control System', frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# cap.release()
# cv2.destroyAllWindows()




import cv2
import mediapipe as mp
import numpy as np
from AppOpener import open
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import pyautogui
import os

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

# Function to recognize hand gestures
def recognize_gesture(hand1, hand2):
    # Default return values
    gesture = None
    thumb_to_index_distance = None

    if hand1 and hand2:
        # Gesture A: Both hands, thumbs and index fingers close together (Open Apps)
        thumb_distance = calculate_distance(hand1.landmark[4], hand2.landmark[4])
        index_distance = calculate_distance(hand1.landmark[8], hand2.landmark[8])
        
        if thumb_distance < 0.1 and index_distance < 0.1:
            return 'A', None
        
        # Gesture B: Hands far apart (Next media track / Shutdown)
        if thumb_distance > 0.4 and index_distance > 0.4:
            return 'B', None

        # Gesture C: Hands forming "C" shape (Previous track)
        thumb1_to_index1 = calculate_distance(hand1.landmark[4], hand1.landmark[8])
        thumb2_to_index2 = calculate_distance(hand2.landmark[4], hand2.landmark[8])
        
        if thumb1_to_index1 > 0.2 and thumb2_to_index2 > 0.2:
            return 'C', None

    if hand1:
        # Gesture D: Thumb and index finger close together (Volume control)
        thumb_tip = hand1.landmark[4]
        index_tip = hand1.landmark[8]
        thumb_to_index_distance = calculate_distance(thumb_tip, index_tip)

        if thumb_to_index_distance < 0.1:
            return 'D', thumb_to_index_distance

        # Gesture E: Thumb and index finger forming "L" shape (Brightness control)
        if hand1.landmark[4].x < hand1.landmark[8].x:  # Thumb is left of index finger
            return 'E', thumb_to_index_distance

        # Gesture F: Index finger pointing upward (Mouse control)
        if hand1.landmark[8].y < hand1.landmark[6].y:
            return 'F', None

        # Gesture G: Thumb and index quick tap (Mouse click)
        if calculate_distance(thumb_tip, index_tip) < 0.05:
            return 'G', None
        
        # Gesture H: Palms together (System Lock)
        if hand2 and calculate_distance(hand1.landmark[0], hand2.landmark[0]) < 0.05:
            return 'H', None

    return gesture, thumb_to_index_distance

# Function to adjust volume based on thumb and index finger distance
def adjust_volume(distance):
    global volume, minVol, maxVol
    vol = np.interp(distance, [0.05, 0.3], [minVol, maxVol])
    volume.SetMasterVolumeLevel(vol, None)
    print(f"Volume adjusted: {vol}")

# Function to adjust brightness based on thumb and index finger distance
def adjust_brightness(distance):
    brightness = int(np.interp(distance, [0.05, 0.3], [0, 100]))
    os.system(f"powershell (Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{brightness})")
    print(f"Brightness adjusted: {brightness}%")

# Function to control mouse movement and clicking
def control_mouse(hand):
    if hand:
        screen_width, screen_height = pyautogui.size()
        x, y = int(hand.landmark[8].x * screen_width), int(hand.landmark[8].y * screen_height)
        pyautogui.moveTo(x, y)
        print(f"Mouse moved to: {x}, {y}")

# Trigger app based on gesture
def trigger_app(gesture, last_opened_app):
    if gesture in apps and last_opened_app != apps[gesture]:
        open(apps[gesture], match_closest=True)
        print(f"Opening {apps[gesture]}...")
        return apps[gesture]
    return last_opened_app

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=2) as hands:
    last_gesture = None
    consecutive_gesture_frames = 0
    last_opened_app = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            hand1 = results.multi_hand_landmarks[0] if len(results.multi_hand_landmarks) > 0 else None
            hand2 = results.multi_hand_landmarks[1] if len(results.multi_hand_landmarks) > 1 else None

            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            gesture, thumb_to_index_distance = recognize_gesture(hand1, hand2)

            if gesture:
                if gesture == last_gesture:
                    consecutive_gesture_frames += 1
                else:
                    consecutive_gesture_frames = 0
                    last_gesture = gesture

                if consecutive_gesture_frames > 10:
                    print(f"Recognized Gesture: {gesture}")
                    if gesture in ['A', 'B', 'C']:  # Open apps/media control
                        last_opened_app = trigger_app(gesture, last_opened_app)
                    elif gesture == 'D' and thumb_to_index_distance is not None:
                        adjust_volume(thumb_to_index_distance)
                    elif gesture == 'E' and thumb_to_index_distance is not None:
                        adjust_brightness(thumb_to_index_distance)
                    elif gesture == 'F':
                        control_mouse(hand1)
                    elif gesture == 'H':
                        os.system("rundll32.exe user32.dll,LockWorkStation")

                    consecutive_gesture_frames = 0

        cv2.imshow('Gesture Control System', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()