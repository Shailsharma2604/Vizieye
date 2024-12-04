# import cv2
# import mediapipe as mp
# import numpy as np
# import screen_brightness_control as sbc
# import tkinter as tk
# from PIL import Image, ImageTk
# import threading

# # Initialize MediaPipe Hands
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
# mp_drawing = mp.solutions.drawing_utils

# def adjust_brightness(distance):
#     # Map the distance to a brightness level (0 to 100)
#     brightness = max(0, min(100, distance * 100))  # Scale the distance to 0-100
#     sbc.set_brightness(brightness)
#     print(f"Brightness set to: {brightness}%")

# class BrightnessControlApp:
#     def __init__(self, window, window_title):
#         self.window = window
#         self.window.title(window_title)

#         self.video_source = 0  # Webcam source
#         self.vid = cv2.VideoCapture(self.video_source)

#         # Set up the canvas to display the video feed
#         self.canvas = tk.Canvas(window, width=640, height=480)
#         self.canvas.pack()

#         # Initialize the button to close the window
#         self.btn_quit = tk.Button(window, text="Quit", width=10, command=self.quit)
#         self.btn_quit.pack()

#         # Start the video update loop
#         self.update_video()

#         self.window.mainloop()

#     def update_video(self):
#         ret, frame = self.vid.read()
#         if ret:
#             # Convert the frame to RGB for MediaPipe processing
#             image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results = hands.process(image_rgb)

#             if results.multi_hand_landmarks:
#                 for hand_landmarks in results.multi_hand_landmarks:
#                     # Draw hand landmarks
#                     mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#                     # Get positions of the thumb and index finger
#                     thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
#                     index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

#                     # Calculate the distance between thumb and index finger
#                     thumb_pos = np.array([thumb.x, thumb.y])
#                     index_pos = np.array([index_finger.x, index_finger.y])
#                     distance = np.linalg.norm(thumb_pos - index_pos)

#                     # Adjust brightness based on finger distance
#                     adjust_brightness(distance)

#             # Convert the image to a format that Tkinter can use
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image = Image.fromarray(frame_rgb)
#             photo = ImageTk.PhotoImage(image=image)

#             # Update the canvas with the new image
#             self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
#             self.window.after(10, self.update_video)  # Schedule the next video update

#     def quit(self):
#         self.vid.release()
#         self.window.quit()

# # Create a Tkinter window and pass it to the BrightnessControlApp class
# root = tk.Tk()
# app = BrightnessControlApp(root, "Brightness Control with Hand Gestures")



import cv2
import mediapipe as mp
import numpy as np
import screen_brightness_control as sbc
import tkinter as tk
from PIL import Image, ImageTk

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

def adjust_brightness(distance):
    # Map the distance to a brightness level (0 to 100)
    brightness = max(0, min(100, distance * 100))  # Scale the distance to 0-100
    sbc.set_brightness(brightness)
    print(f"Brightness set to: {brightness}%")

class BrightnessControlApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0  # Webcam source
        self.vid = cv2.VideoCapture(self.video_source)

        # Set up the canvas to display the video feed
        self.canvas = tk.Canvas(window, width=640, height=480)
        self.canvas.pack()

        # Initialize the button to close the window
        self.btn_quit = tk.Button(window, text="Quit", width=10, command=self.quit)
        self.btn_quit.pack()

        # Start the video update loop
        self.update_video()

        self.window.mainloop()

    def update_video(self):
        ret, frame = self.vid.read()
        if ret:
            # Convert the frame to RGB for MediaPipe processing
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Get positions of the thumb and index finger
                    thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    # Calculate the distance between thumb and index finger
                    thumb_pos = np.array([thumb.x, thumb.y])
                    index_pos = np.array([index_finger.x, index_finger.y])
                    distance = np.linalg.norm(thumb_pos - index_pos)

                    # Adjust brightness based on finger distance
                    adjust_brightness(distance)

            # Convert the frame to a format that Tkinter can use
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(image=image)

            # Update the canvas with the new image
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.image = photo  # Keep a reference to the image to avoid garbage collection

            # Schedule the next video update
            self.window.after(10, self.update_video)  # Schedule the next video update

    def quit(self):
        self.vid.release()
        self.window.quit()

# Create a Tkinter window and pass it to the BrightnessControlApp class
root = tk.Tk()
app = BrightnessControlApp(root, "Brightness Control with Hand Gestures")
