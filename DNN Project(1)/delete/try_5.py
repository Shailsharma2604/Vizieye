import cv2
import mediapipe as mp
import numpy as np
import screen_brightness_control as sbc
import threading
import tkinter as tk
from tkinter import messagebox

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

running = False  # To control the video capture thread


def adjust_brightness(distance):
    """Map the distance to a brightness level (0 to 100) and set the brightness."""
    brightness = max(0, min(100, distance * 100))  # Scale the distance to 0-100
    sbc.set_brightness(brightness)
    print(f"Brightness set to: {brightness}%")


def video_capture():
    """Handle the video capture and brightness adjustment."""
    global running
    cap = cv2.VideoCapture(0)

    while running:
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


def start_brightness_control():
    """Start the video capture and brightness adjustment."""
    global running
    if not running:
        running = True
        threading.Thread(target=video_capture, daemon=True).start()
    else:
        messagebox.showinfo("Info", "Brightness control is already running.")


def stop_brightness_control():
    """Stop the video capture."""
    global running
    if running:
        running = False
    else:
        messagebox.showinfo("Info", "Brightness control is not running.")


# Create the GUI window
root = tk.Tk()
root.title("Brightness Control")
root.geometry("300x200")

# Add GUI elements
start_button = tk.Button(root, text="Start Brightness Control", command=start_brightness_control, bg="green", fg="white")
start_button.pack(pady=20)

stop_button = tk.Button(root, text="Stop Brightness Control", command=stop_brightness_control, bg="red", fg="white")
stop_button.pack(pady=20)

exit_button = tk.Button(root, text="Exit", command=root.destroy, bg="gray", fg="white")
exit_button.pack(pady=20)

# Run the GUI loop
root.mainloop()
