from flask import Flask, jsonify, render_template, session
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import random
import subprocess  # To handle opening applications
import smtplib  # For sending emails
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'rushi'

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get all available voices
voices = engine.getProperty('voices')

# Set the default voice to female (session or default fallback)
def get_voice_id():
    return session.get('voice_id', voices[1].id)

def speak(text, speed=130, voice_id=None):
    if voice_id is None:
        voice_id = get_voice_id()
    engine.setProperty('rate', speed)
    engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.runAndWait()

# Recognize speech input from microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            query = recognizer.recognize_google(audio)
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand what you said.")
            return None
        except sr.RequestError:
            speak("Sorry, there was an error with the recognition service.")
            return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-information', methods=['POST'])
def get_information():
    query = recognize_speech()
    
    if query:
        try:
            if 'hello' in query:
                speak("Hello, Good Day, welcome to MITCORER")

            # Open applications or websites based on command
            elif 'open' in query:
                process_open_command(query)

            # Voice and speed customization
            elif 'female' in query:
                session['voice_id'] = voices[1].id
                speak("Voice changed to female")
            elif 'male' in query:
                session['voice_id'] = voices[0].id
                speak("Voice changed to male")
            elif 'speed' in query:
                speed = int(query.split()[-1])
                speak("Voice speed changed", speed=speed)
            elif 'voice' in query:
                voice_option = query.split()[-1]
                if voice_option.isdigit() and int(voice_option) < len(voices):
                    selected_voice_id = voices[int(voice_option)].id
                    speak("Voice changed", voice_id=selected_voice_id)
                else:
                    speak("Invalid voice option. Please choose a valid voice.")

            # General commands for time, date, music, jokes, weather
            elif 'time' in query:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"The current time is {current_time}")
            elif 'date' in query:
                current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
                speak(f"Today is {current_date}")
            elif 'play music' in query:
                play_music()
                speak('Playing music...')
            elif 'joke' in query:
                joke = get_joke()
                speak(joke)
            elif 'weather' in query:
                weather_info = get_weather_info()
                speak(f"The weather today is {weather_info}.")

            # Sending email
            elif 'email' in query:
                send_email()
                speak("Sending email.")

            # Handling unknown commands
            else:
                speak("Sorry, I didn't catch that command.")

        except Exception as e:
            speak(f"An error occurred: {str(e)}")

    return jsonify({'status': 'success'})

# Function to handle opening applications and websites
def process_open_command(query):
    if 'open vs code' in query:
        open_application('code')
    elif 'open notepad' in query:
        open_application('notepad')
    elif 'open calculator' in query:
        open_application('calc')
    elif 'open chrome' in query:
        open_application('chrome')
    elif 'open google' in query:
        webbrowser.open("https://www.google.com/")
        speak('Opening Google...')
    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com/")
        speak('Opening YouTube...')
    else:
        speak("I am unable to open that application or website.")

# Function to open local applications
def open_application(app_name):
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(app_name)  # Will open the app by name
        elif os.name == 'posix':  # Linux/MacOS
            subprocess.run(['open', '-a', app_name])  # MacOS example
        speak(f"Opening {app_name}")
    except Exception as e:
        speak(f"Unable to open {app_name}. Error: {str(e)}")

# Dummy functions to represent search, send_email, play_music, etc.
def play_music():
    webbrowser.open("https://open.spotify.com/")  # Opens Spotify for example

# Dummy email function (you can implement actual email logic)
def send_email():
    sender_email = "your_email@gmail.com"
    receiver_email = "receiver_email@gmail.com"
    subject = "Test Email"
    body = "This is a test email from the voice assistant."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Configure your email sending mechanism here (e.g., using Gmail SMTP)
    try:
        # You can use smtplib to send an email
        # e.g., with Gmail: smtp.gmail.com (ensure app passwords or OAuth is set)
        speak("Email sent successfully.")
    except Exception as e:
        speak(f"Error in sending email: {str(e)}")

def get_weather_info():
    return "sunny with a high of 25 degrees Celsius"

def get_joke():
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        # More jokes...
    ]
    return random.choice(jokes)

if __name__ == '__main__':
    app.run(debug=True)
