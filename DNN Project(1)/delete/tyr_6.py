import tkinter as tk
from tkinter import ttk
import cv2
import mediapipe as mp
import numpy as np
from AppOpener import open
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import threading
import PIL.Image, PIL.ImageTk
import screen_brightness_control as sbc
import pyautogui


class HandGestureControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Hand Gesture App Controller")
        self.root.geometry("700x800")
        
        # Mediapipe setup
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Apps dictionary
        self.apps = {
            'A': 'whatsapp',
            'B': 'telegram',
            'C': 'chrome'
        }
        
        # Volume control setup
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.minVol, self.maxVol, _ = self.volume.GetVolumeRange()
        
        # App state variables
        self.last_opened_app = None
        self.last_gesture = None
        self.consecutive_gesture_frames = 0
        
        # Camera and recognition state
        self.camera_active = False
        self.cap = None
        
        # Create GUI components
        self.create_widgets()
        
    def create_widgets(self):
        # Frame for app status
        app_frame = ttk.LabelFrame(self.root, text="App Status")
        app_frame.pack(padx=10, pady=10, fill='x')
        
        self.app_status = {}
        for app in ['WhatsApp', 'Telegram', 'Chrome']:
            app_label = ttk.Label(app_frame, text=f"{app}: Closed", 
                                  foreground='red')
            app_label.pack(anchor='w', padx=10, pady=5)
            self.app_status[app.lower()] = app_label
        
        # Volume control frame
        volume_frame = ttk.LabelFrame(self.root, text="Volume Control")
        volume_frame.pack(padx=10, pady=10, fill='x')
        
        self.volume_scale = ttk.Scale(volume_frame, from_=0, to=100, 
                                      orient='horizontal', 
                                      command=self.manual_volume_adjust)
        self.volume_scale.set(50)
        self.volume_scale.pack(padx=10, pady=10, fill='x')
        
        self.volume_label = ttk.Label(volume_frame, text="Volume: 50%")
        self.volume_label.pack()
        
        # Brightness control frame
        brightness_frame = ttk.LabelFrame(self.root, text="Brightness Control")
        brightness_frame.pack(padx=10, pady=10, fill='x')
        
        self.brightness_scale = ttk.Scale(brightness_frame, from_=0, to=100, 
                                          orient='horizontal', 
                                          command=self.manual_brightness_adjust)
        self.brightness_scale.set(sbc.get_brightness()[0])
        self.brightness_scale.pack(padx=10, pady=10, fill='x')
        
        self.brightness_label = ttk.Label(brightness_frame, text=f"Brightness: {sbc.get_brightness()[0]}%")
        self.brightness_label.pack()
        
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
        
        screenshot_button = ttk.Button(button_frame, text="Take Screenshot", 
                                       command=self.take_screenshot)
        screenshot_button.pack(side='left', expand=True, padx=5)
        
        quit_button = ttk.Button(button_frame, text="Quit", 
                                 command=self.on_closing)
        quit_button.pack(side='right', expand=True, padx=5)
        
        # Gesture info
        info_label = ttk.Label(self.root, 
            text="Gestures: A (Close) - WhatsApp, B (Far) - Telegram, C (Spread) - Chrome, V - Screenshot",
            font=('Arial', 10, 'italic')
        )
        info_label.pack(padx=10, pady=5)
        
        # Protocol for closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def manual_volume_adjust(self, val):
        volume_val = float(val)
        self.volume_label.config(text=f"Volume: {int(volume_val)}%")
        vol = np.interp(volume_val, [0, 100], [self.minVol, self.maxVol])
        self.volume.SetMasterVolumeLevel(vol, None)
    
    def manual_brightness_adjust(self, val):
        brightness_val = int(float(val))
        self.brightness_label.config(text=f"Brightness: {brightness_val}%")
        sbc.set_brightness(brightness_val)
    
    def take_screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        print("Screenshot saved as 'screenshot.png'.")
    
    def process_camera_frame(self):
        if not self.camera_active:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            return
        
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        with self.mp_hands.Hands(
            model_complexity=0, 
            min_detection_confidence=0.5, 
            min_tracking_confidence=0.5, 
            max_num_hands=2
        ) as hands:
            results = hands.process(frame_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame_rgb, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS
                    )
        
        # Convert frame for Tkinter
        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame_rgb))
        self.camera_label.config(image=photo)
        self.camera_label.image = photo
        
        # Schedule next frame
        self.root.after(10, self.process_camera_frame)
    
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
