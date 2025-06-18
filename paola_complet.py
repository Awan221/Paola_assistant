import requests
import os
import vlc
import time
from gtts import gTTS
import speech_recognition as sr
import subprocess
import pygame
from pytube import YouTube
from datetime import datetime
import serial
import threading


# Fonction pour rechercher une piste sur Deezer
# def search_track(query):
#     url = f"https://api.deezer.com/search?q={query}"
#     response = requests.get(url)
#     data = response.json()
#     return data['data'][0]  # retourne la première piste trouvée

# # Fonction pour lire la musique avec VLC
# def play_track(url):
#     player = vlc.MediaPlayer(url)
#     player.play()

#     # attendre que la lecture commence
#     time.sleep(1.5)

#     # attendre que la piste soit terminée
#     while player.is_playing():
#         time.sleep(1)

# Initialisation de pygame mixer
pygame.mixer.init()
#ser = serial.Serial('/dev/ttyUSB0', 9600)  # Mettez à jour le port série selon votre configuration

def control_led(command):
    if command == "allumer LED rouge":
        ser.write(b'R')  # Envoyer 'R' à l'Arduino pour allumer la LED rouge
        print("LED rouge allumée")
    elif command == "éteindre LED rouge":
        ser.write(b'r')  # Envoyer 'r' à l'Arduino pour éteindre la LED rouge
        print("LED rouge éteinte")
    elif command == "allumer LED verte":
        ser.write(b'G')  # Envoyer 'G' à l'Arduino pour allumer la LED verte
        print("LED verte allumée")
    elif command == "éteindre LED verte":
        ser.write(b'g')  # Envoyer 'g' à l'Arduino pour éteindre la LED verte
        print("LED verte éteinte")
    elif command == "allumer LED bleue":
        ser.write(b'B')  # Envoyer 'B' à l'Arduino pour allumer la LED bleue
        print("LED bleue allumée")
    elif command == "éteindre LED bleue":
        ser.write(b'b')  # Envoyer 'b' à l'Arduino pour éteindre la LED bleue
        print("LED bleue éteinte")
    else:
        print("Commande de LED inconnue")

def read_humidity():
    if ser.in_waiting > 0:
        humidity_value = ser.readline().decode('utf-8').rstrip()
        print(f"Niveau d'humidité: {humidity_value}")
        text_to_vocal(f"Le niveau d'humidité est de {humidity_value} pourcent")

def search_music(query):
    api_key = 'AIzaSyAXTArSfaA2-mXK89mqmBWgxjce-l1kJfc'  # Remplacez par votre clé API YouTube
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&videoCategoryId=10&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if data.get('items') and len(data['items']) > 0:
        return data['items'][0]  # retourne la première vidéo trouvée
    else:
        return None

def get_direct_video_url(video_id):
    yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
    stream = yt.streams.filter(only_audio=True).first()
    return stream.url

def play_track(url,stop_event):
    player = vlc.MediaPlayer(url)
    player.play()

    # attendre que la lecture commence
    time.sleep(1.5)

    # attendre que la vidéo soit terminée ou que l'arrêt soit demandé
    while player.is_playing() and not stop_event.is_set():
        time.sleep(1)
    
    player.stop()

# Fonction pour écouter et reconnaître la commande vocale
def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language="fr-FR")
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand the gaudio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

def get_weather(city, api_key):
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no'
    response = requests.get(url)
    data = response.json()

    if 'error' in data:
        print(f"Error: {data['error']['message']}")
    else:
        location = data['location']['name']
        temp_c = data['current']['temp_c']
        condition = data['current']['condition']['text']
        humidity = data['current']['humidity']
        wind_kph = data['current']['wind_kph']

        return f"La météo à {location}: {condition}, Température : {temp_c} degrés Celsius, Humidité : {humidity} pourcent, Vitesse du vent : {wind_kph} kilomètres heure"


def text_to_vocal(text):
    if text:
        # Générer un nom de fichier unique basé sur la date et l'heure
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"command_{current_time}.mp3"
        
        tts = gTTS(text=text, lang='fr')
        save_path = os.path.join("c:\\Users\\Dell\\Downloads", file_name)
        tts.save(save_path)
        play_audio(save_path)

def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        
        while True:
            try:
                print("En attente du mot-clé...")
                audio = recognizer.listen(source, timeout=3)
                keyword = recognizer.recognize_google(audio, language="fr-FR").lower()
                print(f"Vous avez dit : {keyword}")
                if "paula" in keyword or "paola" in keyword:
                    print("Mot-clé détecté, veuillez dire votre commande:")
                    text_to_vocal("Bonjour, que puis-je faire pour vous ?")
                    recognizer = sr.Recognizer()
                    mic = sr.Microphone()
                    with mic as source:
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio, language="fr-FR")
                        print("Votre commande est : " + command)
                        return command
            except sr.UnknownValueError:
                print("Je n'ai pas compris, veuillez répéter.")
            except sr.RequestError as e:
                print(f"Erreur du service de reconnaissance vocale: {e}")
            except KeyboardInterrupt:
                print("Interruption de l'utilisateur.")
                return None  # Sortir de la fonction si l'interruption est détectée

if __name__ == "__main__":
    intro = "Bienvenue, je suis Paola votre assistant domestique. Veuillez dire une commande en commençant par Paola"
    print("Dites 'Paola' pour commencer à enregistrer votre commande:")
    text_to_vocal(intro)

    while True:
        command = recognize_speech()
        if command:
            if "mets-moi" in command:
                query = command.replace("mets-moi","").split()
                print(f"Recherche de musique: {query}")
                track = search_music(query)
                if track:
                    video_id = track['id']['videoId']
                    print(f"Lecture de la vidéo: {track['snippet']['title']}")
                    direct_url = get_direct_video_url(video_id)

                    stop_event = threading.Event()
                    music_thread = threading.Thread(target=play_track, args=(direct_url, stop_event))
                    music_thread.start()

                    # Attendre que l'utilisateur demande d'arrêter la musique
                    input("Appuyez sur Entrée pour arrêter la musique....\n")

                    stop_event.set()
                    music_thread.join()
                    print("La musique a été arrêtée.")
            elif "météo de" in command:
                city = command.replace("météo de","")
                api_key = "Votre_clé_API_WeatherAPI"
                text = get_weather(city, api_key)
                text_to_vocal(text)
            elif "niveau d'humidité" in command:
                read_humidity()
            elif "allumer LED" in command or "éteindre LED" in command:
                control_led(command)
            else:
                print("Commande non reconnue")
                text_to_vocal("Commande non reconnue")