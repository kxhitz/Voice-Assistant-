from ipaddress import ip_address
import pyttsx3
import requests
import speech_recognition as sr
import threading
import subprocess as sp
import imdb
import wolframalpha
from pynput import keyboard
from datetime import datetime
from decouple import config
from random import choice
from conv import random_text
from online import find_my_ip, search_on_google,  search_on_wikipedia, youtube, get_news, weather_forecast

# Global State
listening = False

def setup_engine():
    engine = pyttsx3.init('nsss')  # Mac-specific driver
    preferred_voice_names = ['daniel']
    voices = engine.getProperty('voices')

    for voice in voices:
        if any(name in voice.id.lower() for name in preferred_voice_names):
            engine.setProperty('voice', voice.id)
            print(f"✅ Voice selected: {voice.name} ({voice.id})")
            break
    else:
        print("⚠️ No preferred voice found. Using default.")

    engine.setProperty('rate', 200)
    engine.setProperty('volume', 1.0)
    return engine

engine = setup_engine()
USER = config('USER')
HOSTNAME = config('BOT')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greed_me():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 16:
        speak("Good Afternoon")
    elif 16 <= hour < 19:
        speak("Good Evening")
    speak(f"I am {HOSTNAME}. How may I help you?")

def take_command():
    r = sr.Recognizer()
    mic_list = sr.Microphone.list_microphone_names()
    print("Available mics:", mic_list)

    with sr.Microphone(device_index=2) as source:  # change index as needed
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.energy_threshold = 300
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-IN')
        print(query)

        if 'stop' not in query and 'exit' not in query:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            speak("Good Night Sir" if hour >= 21 or hour < 6 else "Have a Good Day")
            exit()

    except Exception as e:
        print("Error:", e)
        speak("Oops! I didn't get that. Please say again.")
        query = 'None'

    return query

# Hotkey callback handlers
def on_activate_k():
    global listening
    listening = True
    print("🎙️ Listening started")

def on_activate_p():
    global listening
    listening = False
    print("⏸️ Listening paused")

def hotkey_listener():
    with keyboard.GlobalHotKeys({
        '<cmd>+<ctrl>+k': on_activate_k,
        '<cmd>+<ctrl>+p': on_activate_p
    }) as h:
        h.join()

# Run hotkey listener in a background thread
threading.Thread(target=hotkey_listener, daemon=True).start()

# Main voice assistant loop
if __name__ == '__main__':
    greed_me()
    while True:
        if listening:
            query = take_command().lower()

            if "how are you" in query:
                speak("I am absolutely fine Sir. What about you?")

            elif "open terminal" in query:
                speak("Opening Terminal")
                sp.run(["open", "-a", "Terminal"])

            elif "open photo booth" in query:
                speak("Opening photo booth")
                sp.run(["open", "/System/Applications/Photo Booth.app"])

            elif "open notes" in query:
                speak("Opening Notes")
                sp.run(["open", "/System/Applications/Notes.app"])

            elif "open discord" in query:
                speak("Opening Discord")
                sp.run(["open", "/Applications/Discord.app"])

            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(
                    f"your ip address is {ip_address} "
                )
                print(f"your ip address is {ip_address}")

            elif "youtube" in query:
                speak("What do you want to play on youtube ?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak("What do you want to search on google?")
                query = take_command().lower()
                search_on_google(query)

            elif "wikipedia" in query:
                speak("What do you want to search on wikipedia?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to Wikipedia: {results}")
                speak("I am printing in on terminal")
                print(results)


            elif "give me news" in query:
                news_list = get_news()
                speak("I am reading out the latest headlines of today.")
                for headline in news_list:
                    speak(headline)
                speak("I am printing them on screen.")
                print(*news_list, sep='\n')

            elif "weather" in query:
                ip_address = find_my_ip()
                speak("Tell me the name of your City")
                city = input("Enter name of your City")
                speak(f"Getting Weather Report for your City {city}")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The Current Temperature is {temp},but it feels like {feels_like}")
                speak(f"Also the Weather Report talks about {weather}")
                speak("I am printing Weather information on screen")
                print(f"Description:{weather}\nTemperature: {temp}\nFeels Like: {feels_like}")


            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Tell me the movie name")
                text = take_command()
                movies = movies_db.search_movie(text)
                speak("Searching for " + text)
                speak("I found these")
                for movie in movies:
                    title = movie.get("title", "Unknown Title")
                    year = movie.get("year", "Unknown Year")
                    speak(f"{title} - {year}")
                    try:
                        info = movie.getID()
                        movie_info = movies_db.get_movie(info)
                        rating = movie_info.get("rating", "No rating available")
                        cast = movie_info.get("cast", [])
                        actor = [person.get("name", "Unknown") for person in cast[:5]]
                        plot = movie_info.get("plot outline", "Plot summary not available")
                        speak(
                            f"{title} was released in {year}, has IMDb rating of {rating}. It has a cast of {', '.join(actor)}. The plot summary is: {plot}")
                        print(
                            f"{title} was released in {year}, has IMDb rating of {rating}. It has a cast of {', '.join(actor)}. The plot summary is: {plot}")
                    except Exception as e:
                        speak(f"Sorry, I couldn't fetch details for {title}.")
                        print(f"Error fetching details for {title}: {e}")

            elif "calculate" in query:
                app_id = "E64822-5QQARHLYRJ"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind+1:]
                result = client.query(" ".join(text))
                try:
                    ans = next(result.results).text
                    speak("The answer is: " + ans)
                    print("The answer is: " + ans)
                except StopIteration:
                    speak("Sorry, I couldn't find any answers.")

            elif "what is" in query or 'who is' in query or 'which is' in query:
                app_id = "E64822-5QQARHLYRJ"
                client = wolframalpha.Client(app_id)
                try:
                    ind = query.lower().index('what is') if 'what is' in query.lower() else \
                        query.lower().index('who is') if 'who is' in query.lower() else \
                        query.lower().index('which is') if 'which is' in query.lower() else None

                    if id is not None:
                        text = query.split()[ind+2:]
                        result = client.query(" ".join(text))
                        ans = next(result.results).text
                        speak("The answer is: " + ans)
                        print("The answer is: " + ans)
                    else:
                        speak("Sorry, I couldn't find any answers.")

                except StopIteration:
                    speak("Sorry, I couldn't find any answers.")