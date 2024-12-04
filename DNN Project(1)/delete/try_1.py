# import cv2
# import mediapipe as mp
# import numpy as np
# import os
# import time

# class BrightnessController:
#     def __init__(self):
#         self.brightness_mode = False

#     def calculate_landmark_distance(self, landmark1, landmark2):
#         """Calculate 3D Euclidean distance between two landmarks."""
#         return np.sqrt(
#             (landmark1.x - landmark2.x)**2 + 
#             (landmark1.y - landmark2.y)**2 + 
#             (landmark1.z - landmark2.z)**2
#         )

#     def is_thumb_index_pinched(self, hand_landmarks):
#         """Detect if the thumb and index finger are pinched."""
#         thumb_tip = hand_landmarks.landmark[4]  # Tip of thumb
#         index_tip = hand_landmarks.landmark[8]  # Tip of index finger
#         tip_distance = self.calculate_landmark_distance(thumb_tip, index_tip)
#         return tip_distance < 0.05  # Threshold for pinch detection

#     def adjust_brightness(self, hand_landmarks):
#         """Adjust brightness based on the position of the thumb relative to the index finger."""
#         if self.is_thumb_index_pinched(hand_landmarks):
#             if not self.brightness_mode:
#                 self.brightness_mode = True
#                 print("Brightness control mode activated")
#                 return

#             try:
#                 current_brightness = self.get_current_brightness()
#             except Exception as e:
#                 print(f"Error getting brightness: {e}")
#                 return

#             thumb_tip = hand_landmarks.landmark[4]  # Tip of thumb
#             index_tip = hand_landmarks.landmark[8]  # Tip of index finger
            
#             # Increase brightness if the thumb is higher than the index finger
#             if thumb_tip.y < index_tip.y:  # Thumb is above index finger
#                 new_brightness = min(100, current_brightness + 10)  # Increase brightness
#                 print(f"Increasing brightness to {new_brightness}%")
#             # Decrease brightness if the thumb is lower than the index finger
#             elif thumb_tip.y > index_tip.y:  # Thumb is below index finger
#                 new_brightness = max(0, current_brightness - 10)  # Decrease brightness
#                 print(f"Decreasing brightness to {new_brightness}%")

#             self.set_brightness(new_brightness)

#         else:
#             if self.brightness_mode:
#                 print("Brightness control mode deactivated")
#                 self.brightness_mode = False

#     def get_current_brightness(self):
#         """Get current screen brightness using a Windows-specific method."""
#         try:
#             import subprocess
#             result = subprocess.run(['powershell', 
#                 '(Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightness).CurrentBrightness'], 
#                 capture_output=True, text=True)
#             brightness = int(result.stdout.strip())
#             print(f"Current brightness retrieved: {brightness}%")
#             return brightness
#         except Exception as e:
#             print(f"Error retrieving brightness: {e}")
#             return 50  # Default fallback

#     def set_brightness(self, brightness):
#         """Set screen brightness using a Windows-specific method."""
#         try:
#             os.system(f'powershell (Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{brightness})')
#             print(f"Successfully set brightness to {brightness}%")
#         except Exception as e:
#             print(f"Error setting brightness: {e}")

# def main():
#     # Initialize webcam
#     cap = cv2.VideoCapture(0)
#     cap.set(3, 640)
#     cap.set(4, 480)

#     # Initialize MediaPipe
#     mp_hands = mp.solutions.hands
#     mp_drawing = mp.solutions.drawing_utils

#     # Initialize brightness controller
#     brightness_controller = BrightnessController()

#     # Mediapipe hands setup
#     with mp_hands.Hands(
#         model_complexity=0, 
#         min_detection_confidence=0.7, 
#         min_tracking_confidence=0.7, 
#         max_num_hands=1
#     ) as hands:
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             # Flip and convert frame
#             frame = cv2.flip(frame, 1)
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#             # Process frame
#             results = hands.process(frame_rgb)

#             # Draw and process hand landmarks
#             if results.multi_hand_landmarks:
#                 for hand_landmarks in results.multi_hand_landmarks:
#                     # Draw hand connections
#                     mp_drawing.draw_landmarks(
#                         frame, 
#                         hand_landmarks, 
#                         mp_hands.HAND_CONNECTIONS
#                     )

#                     # Adjust brightness
#                     brightness_controller.adjust_brightness(hand_landmarks)

#             # Display frame
#             cv2.imshow('Precise Brightness Control', frame)

#             # Exit condition
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#     # Cleanup
#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()

# import cv2
# import mediapipe as mp
# import numpy as np

# # Initialize MediaPipe Hands
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
# mp_drawing = mp.solutions.drawing_utils

# # Start video capture
# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#         break

#     # Convert the image to RGB
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = hands.process(image_rgb)

#     # Check if any hand is detected
#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             # Draw hand landmarks
#             mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#             # Get positions of the thumb and index finger
#             thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
#             index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

#             # Calculate the distance between the thumb and index finger
#             thumb_pos = np.array([thumb.x, thumb.y])
#             index_pos = np.array([index_finger.x, index_finger.y])
#             distance = np.linalg.norm(thumb_pos - index_pos)

#             # Map the distance to brightness level
#             brightness = int(max(0, min(255, distance * 255)))  # Scale to 0-255

#             # Apply brightness to the image
#             bright_image = cv2.convertScaleAbs(image, alpha=1, beta=brightness)

#             # Show the adjusted image
#             cv2.imshow('Brightness Control', bright_image)

#     else:
#         cv2.imshow('Brightness Control', image)

#     if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to exit
#         break

# cap.release()
# cv2.destroyAllWindows()




# import cv2
# import numpy as np
# import screen_brightness_control as sbc
# import time

# # Function to adjust brightness based on finger distance
# def adjust_brightness(distance):
#     # Map the distance to a brightness level (0 to 100)
#     brightness = max(0, min(100, distance * 100))  # Scale the distance to 0-100
#     sbc.set_brightness(brightness)
#     print(f"Brightness set to: {brightness}%")

# # Start capturing video from the webcam
# cap = cv2.VideoCapture(0)

# # Initialize variables for finger tracking
# previous_distance = 0

# while True:
#     success, image = cap.read()
#     if not success:
#         break

#     # Convert to RGB for processing
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
#     # For demonstration, we will simulate the finger distance.
#     # In a real implementation, you would use hand tracking to get this value.
#     thumb_pos = np.random.rand(2)  # Simulated thumb position
#     index_pos = np.random.rand(2)  # Simulated index finger position

#     # Calculate the distance between thumb and index finger
#     distance = np.linalg.norm(thumb_pos - index_pos)

#     # Adjust brightness based on the distance
#     if abs(distance - previous_distance) > 0.05:  # Threshold to prevent excessive updates
#         adjust_brightness(distance)
#         previous_distance = distance

#     # Display the webcam feed
#     cv2.imshow('Webcam Feed', image)

#     if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
#         break

# cap.release()
# cv2.destroyAllWindows()




import cv2
import mediapipe as mp
import numpy as np
import screen_brightness_control as sbc

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

def adjust_brightness(distance):
    # Map the distance to a brightness level (0 to 100)
    brightness = max(0, min(100, distance * 100))  # Scale the distance to 0-100
    sbc.set_brightness(brightness)
    print(f"Brightness set to: {brightness}%")

# Start video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Convert the image to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    # Check if any hand is detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get positions of the thumb and index finger
            thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Calculate the distance between thumb and index finger
            thumb_pos = np.array([thumb.x, thumb.y])
            index_pos = np.array([index_finger.x, index_finger.y])
            distance = np.linalg.norm(thumb_pos - index_pos)

            # Adjust brightness based on finger distance
            adjust_brightness(distance)

    # Show the video feed
    cv2.imshow('Webcam Feed', image)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()