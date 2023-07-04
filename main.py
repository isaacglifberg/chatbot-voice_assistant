import speech_recognition as sr
import pyaudio
import pyttsx3
import datetime
import webbrowser
import requests
import json
import smtplib
import ssl
import pyautogui
import pyjokes
import wikipedia
from wikipedia.exceptions import DisambiguationError


class Assistant:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.p = pyaudio.PyAudio()
        self.api_key = "9c6930ba3c8af466984fff562c3d786c"
        self.weather_api = "https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}"
        # self.weather_api = f"http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={self.api_key}"

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def time(self):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        self.speak(f"Current time is {time}")

    def date(self):
        year = datetime.date.today().year
        day = datetime.date.today().day
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        self.speak(f"Current date is {year}, {day}, {hour}, {minute}")

    def greeting(self):
        hour = datetime.datetime.now().hour
        if 5 <= hour <= 12:
            self.speak('Good morning to you')
        elif 12 < hour <= 18:
            self.speak('Good afternoon to you')
        else:
            self.speak('Good night to you')

    def make_commands(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio, language='en-US')
            print(f"This is what you said: {query}")
        except Exception:
            self.speak('Say that again')
            # self.make_commands()
        return query

    def get_weather(self, city):
        api_key = "88bd90d3c467f767008cf5516997fb7e"
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)
        data = json.loads(response.text)
        return data

    def send_email(self, content, to):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('isaac.glifberg99@gmail.com', 'Bajskorv99')
        server.sendmail('isaac.glifberg99@gmail.com', to, content)
        server.close()

    def joke(self):
        some_joke = pyjokes.get_joke(language="en", category='neutral')
        self.speak(some_joke)

    def screenshot(self):
        img = pyautogui.screenshot()
        img.save('C:/Users/Tech/Desktop/Assets/screenshot.png')


class Main:
    def __init__(self):
        self.assistant = Assistant()
        self.main_menu()

    def main_menu(self):
        # self.assistant.greeting()
        while True:
            command = self.assistant.make_commands().lower()
            if 'time' in command:
                self.assistant.time()

            elif 'date' in command:
                self.assistant.date()

            elif 'joke' in command:
                self.assistant.joke()

            elif 'google' in command:
                print('what should i search on?')
                google_search = self.assistant.make_commands().lower()
                webbrowser.open(
                    f'https://www.google.com/search?q={google_search}')

            elif 'wikipedia' in command:
                print('what to open?')
                wikipedia_search = self.assistant.make_commands().lower()
                try:
                    text = wikipedia.summary(wikipedia_search, sentences=3)
                    self.assistant.speak(text)
                except Exception as error:
                    print(error)
                    self.assistant.speak('Please say that again')
            
            elif 'weather' in command:
                # self.assistant.speak('Which City Sir!')
                print('City?')
                city = self.assistant.make_commands().lower()
                data = self.assistant.get_weather(city)
                weather_type = data['weather'][0]['main']
                description = data['weather'][0]['description']
                temp = data['main']['temp']
                self.assistant.speak(f'Main weather is {weather_type}')
                self.assistant.speak(f'Cloud status is {description}')
                self.assistant.speak(f'Temperature is {temp}')
            
            elif 'email' in command:
                self.assistant.send_email('hello', 'isaac.glifberg99@icloud.com')


if __name__ == "__main__":
    menu = Main()
