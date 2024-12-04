# import tkinter as tk
# from tkinter import ttk
# import cv2
# import mediapipe as mp
# import numpy as np
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# import threading
# import PIL.Image, PIL.ImageTk
# import pyautogui
# import os

# class HandGestureControllerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Gesture Controller with New Features")
#         self.root.geometry("800x800")
        
#         # Mediapipe setup
#         self.mp_hands = mp.solutions.hands
#         self.mp_drawing = mp.solutions.drawing_utils
        
#         # Volume control setup
#         devices = AudioUtilities.GetSpeakers()
#         interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
#         self.volume = cast(interface, POINTER(IAudioEndpointVolume))
#         self.minVol, self.maxVol, _ = self.volume.GetVolumeRange()
        
#         # App state variables
#         self.last_gesture = None
#         self.consecutive_gesture_frames = 0
        
#         # Camera and recognition state
#         self.camera_active = False
#         self.cap = None
        
#         # Create GUI components
#         self.create_widgets()
        
#     def create_widgets(self):
#         # Frame for media control
#         media_frame = ttk.LabelFrame(self.root, text="Media Control")
#         media_frame.pack(padx=10, pady=10, fill='x')
        
#         self.media_status = ttk.Label(media_frame, text="Media: Paused", font=('Arial', 12))
#         self.media_status.pack(padx=10, pady=5)
        
#         # Document scrolling frame
#         scroll_frame = ttk.LabelFrame(self.root, text="Document Scrolling")
#         scroll_frame.pack(padx=10, pady=10, fill='x')
        
#         self.scroll_status = ttk.Label(scroll_frame, text="Scroll: Stopped", font=('Arial', 12))
#         self.scroll_status.pack(padx=10, pady=5)
        
#         # Screen lock/unlock frame
#         lock_frame = ttk.LabelFrame(self.root, text="Screen Lock/Unlock")
#         lock_frame.pack(padx=10, pady=10, fill='x')
        
#         self.lock_status = ttk.Label(lock_frame, text="Screen: Unlocked", font=('Arial', 12))
#         self.lock_status.pack(padx=10, pady=5)
        
#         # Camera feed frame
#         self.camera_frame = ttk.LabelFrame(self.root, text="Camera Feed")
#         self.camera_frame.pack(padx=10, pady=10, expand=True, fill='both')
        
#         self.camera_label = ttk.Label(self.camera_frame)
#         self.camera_label.pack(padx=10, pady=10)
        
#         # Control buttons
#         button_frame = ttk.Frame(self.root)
#         button_frame.pack(padx=10, pady=10, fill='x')
        
#         self.camera_button = ttk.Button(button_frame, text="Start Camera", 
#                                         command=self.toggle_camera)
#         self.camera_button.pack(side='left', expand=True, padx=5)
        
#         quit_button = ttk.Button(button_frame, text="Quit", 
#                                  command=self.on_closing)
#         quit_button.pack(side='right', expand=True, padx=5)
        
#         # Gesture info
#         info_label = ttk.Label(self.root, 
#             text="Gestures: Play/Pause (Pinch), Next (Swipe Right), Previous (Swipe Left), Scroll (Up/Down), Lock (Fist)",
#             font=('Arial', 10, 'italic')
#         )
#         info_label.pack(padx=10, pady=5)
        
#         # Protocol for closing
#         self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
#     def process_camera_frame(self):
#         if not self.camera_active:
#             return
        
#         ret, frame = self.cap.read()
#         if not ret:
#             return
        
#         frame = cv2.flip(frame, 1)
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
#         with self.mp_hands.Hands(
#             model_complexity=0, 
#             min_detection_confidence=0.5, 
#             min_tracking_confidence=0.5, 
#             max_num_hands=1
#         ) as hands:
#             results = hands.process(frame_rgb)
            
#             if results.multi_hand_landmarks:
#                 hand_landmarks = results.multi_hand_landmarks[0]
#                 self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
#                 gesture = self.recognize_gesture(hand_landmarks)
                
#                 if gesture:
#                     self.execute_gesture_action(gesture)
        
#         # Convert frame for Tkinter
#         photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_rgb))
#         self.camera_label.config(image=photo)
#         self.camera_label.image = photo
        
#         # Schedule next frame
#         self.root.after(10, self.process_camera_frame)
    
#     def recognize_gesture(self, landmarks):
#         """
#         Recognize gestures based on landmark positions.
#         """
#         thumb_tip = landmarks.landmark[4]
#         index_tip = landmarks.landmark[8]
#         middle_tip = landmarks.landmark[12]
        
#         # Example gesture conditions
#         if self.calculate_distance(thumb_tip, index_tip) < 0.1:
#             return "play_pause"
#         elif self.calculate_distance(thumb_tip, middle_tip) < 0.1:
#             return "lock"
#         elif thumb_tip.x < 0.2:  # Swipe left
#             return "previous"
#         elif thumb_tip.x > 0.8:  # Swipe right
#             return "next"
#         elif thumb_tip.y < 0.2:  # Scroll up
#             return "scroll_up"
#         elif thumb_tip.y > 0.8:  # Scroll down
#             return "scroll_down"
#         return None
    
#     def execute_gesture_action(self, gesture):
#         if gesture == "play_pause":
#             self.toggle_media_playback()
#         elif gesture == "next":
#             self.next_track()
#         elif gesture == "previous":
#             self.previous_track()
#         elif gesture == "scroll_up":
#             self.scroll_document("up")
#         elif gesture == "scroll_down":
#             self.scroll_document("down")
#         elif gesture == "lock":
#             self.toggle_screen_lock()
    
#     def toggle_media_playback(self):
#         current_text = self.media_status["text"]
#         if "Paused" in current_text:
#             self.media_status.config(text="Media: Playing")
#         else:
#             self.media_status.config(text="Media: Paused")
    
#     def next_track(self):
#         print("Next track")
    
#     def previous_track(self):
#         print("Previous track")
    
#     def scroll_document(self, direction):
#         if direction == "up":
#             pyautogui.scroll(200)
#             self.scroll_status.config(text="Scroll: Up")
#         elif direction == "down":
#             pyautogui.scroll(-200)
#             self.scroll_status.config(text="Scroll: Down")
    
#     def toggle_screen_lock(self):
#         current_text = self.lock_status["text"]
#         if "Unlocked" in current_text:
#             self.lock_status.config(text="Screen: Locked")
#             os.system("rundll32.exe user32.dll,LockWorkStation")
#         else:
#             self.lock_status.config(text="Screen: Unlocked")
    
#     def calculate_distance(self, point1, point2):
#         return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
#     def toggle_camera(self):
#         if not self.camera_active:
#             self.cap = cv2.VideoCapture(0)
#             self.cap.set(3, 640)
#             self.cap.set(4, 480)
#             self.camera_active = True
#             self.camera_button.config(text="Stop Camera")
#             self.process_camera_frame()
#         else:
#             self.camera_active = False
#             if self.cap:
#                 self.cap.release()
#             self.camera_button.config(text="Start Camera")
#             self.camera_label.config(image='')
    
#     def on_closing(self):
#         if self.cap:
#             self.cap.release()
#         self.root.destroy()


# def main():
#     root = tk.Tk()
#     app = HandGestureControllerApp(root)
#     root.mainloop()


# if __name__ == "__main__":
#     main()



import tkinter as tk
from tkinter import ttk
import cv2
import mediapipe as mp
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import PIL.Image, PIL.ImageTk
import pyautogui
import os

class HandGestureControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Controller with Hand Tracking")
        self.root.geometry("800x800")
        
        # Mediapipe setup
        self.mp_hands = mp.solutions.hands.Hands(
            model_complexity=1, 
            min_detection_confidence=0.7, 
            min_tracking_confidence=0.7, 
            max_num_hands=1
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Volume control setup
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.minVol, self.maxVol, _ = self.volume.GetVolumeRange()
        
        # App state variables
        self.last_gesture = None
        self.consecutive_gesture_frames = 0
        
        # Camera and recognition state
        self.camera_active = False
        self.cap = None
        
        # Create GUI components
        self.create_widgets()
        
    def create_widgets(self):
        # Frame for media control
        media_frame = ttk.LabelFrame(self.root, text="Media Control")
        media_frame.pack(padx=10, pady=10, fill='x')
        
        self.media_status = ttk.Label(media_frame, text="Media: Paused", font=('Arial', 12))
        self.media_status.pack(padx=10, pady=5)
        
        # Document scrolling frame
        scroll_frame = ttk.LabelFrame(self.root, text="Document Scrolling")
        scroll_frame.pack(padx=10, pady=10, fill='x')
        
        self.scroll_status = ttk.Label(scroll_frame, text="Scroll: Stopped", font=('Arial', 12))
        self.scroll_status.pack(padx=10, pady=5)
        
        # Screen lock/unlock frame
        lock_frame = ttk.LabelFrame(self.root, text="Screen Lock/Unlock")
        lock_frame.pack(padx=10, pady=10, fill='x')
        
        self.lock_status = ttk.Label(lock_frame, text="Screen: Unlocked", font=('Arial', 12))
        self.lock_status.pack(padx=10, pady=5)
        
        # Camera feed frame
        self.camera_frame = ttk.LabelFrame(self.root, text="Camera Feed")
        self.camera_frame.pack(padx=10, pady=10, expand=True, fill='both')
        
        self.camera_label = ttk.Label(self.camera_frame)
        self.camera_label.pack(padx=10, pady=10)
        
        # Control buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(padx=10, pady=10, fill='x')
        
        self.camera_button = ttk.Button(button_frame, text="Start Camera", 
                                        command=self.toggle_camera)
        self.camera_button.pack(side='left', expand=True, padx=5)
        
        quit_button = ttk.Button(button_frame, text="Quit", 
                                 command=self.on_closing)
        quit_button.pack(side='right', expand=True, padx=5)
        
        # Gesture info
        info_label = ttk.Label(self.root, 
            text="Gestures: Play/Pause (Pinch), Next (Swipe Right), Previous (Swipe Left), Scroll (Up/Down), Lock (Fist)",
            font=('Arial', 10, 'italic')
        )
        info_label.pack(padx=10, pady=5)
        
        # Protocol for closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def process_camera_frame(self):
        if not self.camera_active:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            return
        
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = self.mp_hands.process(frame_rgb)
            
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            self.mp_drawing.draw_landmarks(
                frame, 
                hand_landmarks, 
                mp.solutions.hands.HAND_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
            )
            
            gesture = self.recognize_gesture(hand_landmarks)
            
            if gesture:
                self.execute_gesture_action(gesture)
        
        # Convert frame for Tkinter
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.camera_label.config(image=photo)
        self.camera_label.image = photo
        
        # Schedule next frame
        self.root.after(10, self.process_camera_frame)
    
    def recognize_gesture(self, landmarks):
        """
        Recognize gestures based on landmark positions.
        """
        thumb_tip = landmarks.landmark[4]
        index_tip = landmarks.landmark[8]
        middle_tip = landmarks.landmark[12]
        
        # Example gesture conditions
        if self.calculate_distance(thumb_tip, index_tip) < 0.1:
            return "play_pause"
        elif self.calculate_distance(thumb_tip, middle_tip) < 0.1:
            return "lock"
        elif thumb_tip.x < 0.2:  # Swipe left
            return "previous"
        elif thumb_tip.x > 0.8:  # Swipe right
            return "next"
        elif thumb_tip.y < 0.2:  # Scroll up
            return "scroll_up"
        elif thumb_tip.y > 0.8:  # Scroll down
            return "scroll_down"
        return None
    
    def execute_gesture_action(self, gesture):
        if gesture == "play_pause":
            self.toggle_media_playback()
        elif gesture == "next":
            self.next_track()
        elif gesture == "previous":
            self.previous_track()
        elif gesture == "scroll_up":
            self.scroll_document("up")
        elif gesture == "scroll_down":
            self.scroll_document("down")
        elif gesture == "lock":
            self.toggle_screen_lock()
    
    def toggle_media_playback(self):
        current_text = self.media_status["text"]
        if "Paused" in current_text:
            self.media_status.config(text="Media: Playing")
        else:
            self.media_status.config(text="Media: Paused")
    
    def next_track(self):
        print("Next track")
    
    def previous_track(self):
        print("Previous track")
    
    def scroll_document(self, direction):
        if direction == "up":
            pyautogui.scroll(200)
            self.scroll_status.config(text="Scroll: Up")
        elif direction == "down":
            pyautogui.scroll(-200)
            self.scroll_status.config(text="Scroll: Down")
    
    def toggle_screen_lock(self):
        current_text = self.lock_status["text"]
        if "Unlocked" in current_text:
            self.lock_status.config(text="Screen: Locked")
            os.system("rundll32.exe user32.dll,LockWorkStation")
        else:
            self.lock_status.config(text="Screen: Unlocked")
    
    def calculate_distance(self, point1, point2):
        return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def toggle_camera(self):
        if not self.camera_active:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(3, 640)
            self.cap.set(4, 480)
            self.camera_active = True
            self.camera_button.config(text="Stop Camera")
            self.process_camera_frame()
        else:
            self.camera_active = False
            if self.cap:
                self.cap.release()
            self.camera_button.config(text="Start Camera")
            self.camera_label.config(image='')
    
    def on_closing(self):
        if self.cap:
            self.cap.release()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = HandGestureControllerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
