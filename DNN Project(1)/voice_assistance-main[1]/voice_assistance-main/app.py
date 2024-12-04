from flask import Flask, request, jsonify, render_template, session, copy_current_request_context
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import smtplib
import requests
import os
import random
import threading  # For background task handling

app = Flask(__name__)
app.secret_key = 'rushi'

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
default_voice_id = voices[1].id  # Female voice

def speak(text, speed=130):
    """Speak out the provided text, using the voice from the session."""
    voice_id = session.get('voice_id', default_voice_id)
    engine.setProperty('rate', speed)
    engine.setProperty('voice', voice_id)
    engine.say(text)
    engine.runAndWait()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/get-information', methods=['POST'])
def get_information():
    """Process voice commands."""
    if request.method == 'POST':
        data = request.get_json()
        query = data['query'].lower()

        # Copy the request context to allow session handling inside the thread
        @copy_current_request_context
        def handle_command():
            try:
                if 'hello' in query:
                    speak("Hello, welcome, I am Jarvis. How can I assist you?")
                elif 'open google' in query:
                    if 'search' in query:
                        search_query = query.split('open google and search')[-1].strip()
                        search_google(search_query)
                    else:
                        webbrowser.open("https://www.google.com/")
                    speak('Opening Google...')
                elif 'open youtube' in query:
                    if 'search' in query:
                        search_query = query.split('open youtube and search')[-1].strip()
                        search_youtube(search_query)
                    else:
                        webbrowser.open("https://www.youtube.com/")
                    speak('Opening YouTube...')
                elif 'time' in query:
                    current_time = datetime.datetime.now().strftime("%I:%M %p")
                    speak(f"The current time is {current_time}")
                elif 'date' in query:
                    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
                    speak(f"Today is {current_date}")
                elif 'play music' in query:
                    threading.Thread(target=play_music).start()  # Background task
                    speak('Playing music...')
                elif 'change voice' in query:
                    change_voice(query)
                elif 'email' in query:
                    threading.Thread(target=send_email).start()  # Background task for email
                    speak("Sending an email.")
                elif 'weather' in query:
                    city = query.split('weather in')[-1].strip() if 'in' in query else 'Pune'
                    weather_info = get_weather_info(city)
                    speak(f"The weather in {city} is {weather_info}.")
                elif 'joke' in query:
                    joke = get_joke()
                    speak(joke)
                else:
                    speak("Sorry, I couldn't recognize the command.")
            except Exception as e:
                speak("There was an error processing your request.")
                print(f"Error: {e}")

        # Execute commands in a background thread for better responsiveness
        threading.Thread(target=handle_command).start()
        return jsonify({'status': 'success'})

def change_voice(query):
    """Change voice to male or female and save it in the session."""
    if 'female' in query:
        session['voice_id'] = voices[1].id
        speak("Voice changed to female.")
    elif 'male' in query:
        session['voice_id'] = voices[0].id
        speak("Voice changed to male.")
    else:
        speak("Voice command not recognized.")

def send_email():
    """Send an email in the background."""
    smtp_server = 'smtp.example.com'
    port = 587
    sender_email = 'your_email@example.com'
    receiver_email = 'recipient_email@example.com'
    password = 'your_email_password'

    subject = 'Test Email'
    body = 'This is a test email.'

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, f'Subject: {subject}\n\n{body}')
        speak("Email sent successfully.")
    except Exception as e:
        speak("Failed to send email.")
        print(f"Error: {e}")

def get_weather_info(city):
    """Get the weather information using OpenWeather API."""
    api_key = 'your_openweathermap_api_key'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        data = response.json()
        if 'weather' in data and 'main' in data:
            description = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"{description}, with a temperature of {temp}°C"
    except Exception as e:
        speak("Unable to fetch weather information.")
        print(f"Error: {e}")
    return 'Weather information not available.'

def get_joke():
    """Fetch a random joke from an API."""
    joke_api_url = 'https://api.jokes.one/jod'
    headers = {'Accept': 'application/json'}
    try:
        response = requests.get(joke_api_url, headers=headers)
        data = response.json()
        if data and 'contents' in data and 'jokes' in data['contents']:
            return data['contents']['jokes'][0]['joke']['text']
    except Exception as e:
        speak("Couldn't fetch a joke.")
        print(f"Error: {e}")
    return 'No joke available.'

def search_google(query):
    """Search on Google."""
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

def search_youtube(query):
    """Search on YouTube."""
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(search_url)

def play_music():
    """Play a random music file from the specified directory."""
    music_dir = "C:/Users/Rishu/Music"
    try:
        songs = os.listdir(music_dir)
        if songs:
            index = random.randint(0, len(songs) - 1)
            os.startfile(os.path.join(music_dir, songs[index]))
        else:
            speak("No music files found.")
    except Exception as e:
        speak("Couldn't play music.")
        print(f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True,port=8080)
