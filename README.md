
# Paola - Assistant Vocal Domestique avec Raspberry Pi et Arduino

Paola est un assistant vocal développé en Python, conçu pour s'exécuter sur un Raspberry Pi et interagir avec des composants Arduino via des commandes vocales. Il permet à l'utilisateur de piloter des LED, de lire de la musique, de connaître la météo ou l'humidité, et d'interagir vocalement grâce à la synthèse et la reconnaissance vocale.

## Fonctionnalités

- Reconnaissance vocale en français (via `speech_recognition`)
- Synthèse vocale avec `gTTS` et lecture audio avec `pygame`
- Lecture de musique via recherche YouTube (API + VLC)
- Contrôle vocal des LEDs (rouge, verte, bleue) via Arduino
- Lecture du niveau d’humidité ambiante
- Annonce vocale de la météo d'une ville
- Interaction naturelle via mot-clé ("Paola")

## Technologies et Matériel

### Logiciel
- Python 3
- gTTS
- SpeechRecognition
- VLC (libvlc)
- Pygame
- Pytube
- API WeatherAPI
- API YouTube Data v3
- Arduino IDE

### Matériel
- Raspberry Pi (3 ou 4 recommandé)
- Arduino Uno (connecté en USB)
- LED RGB (rouge, verte, bleue)
- Capteur d’humidité (DHT11 ou équivalent)
- Écran LCD (optionnel)
- Microphone USB
- Haut-parleur ou jack audio

## Arborescence du dépôt

```
paola-assistant/
├── paola_complet.py              # Script principal en Python
├── requirements.txt              # Dépendances Python
├── README.md                     # Présentation du projet
├── docs/
│   └── architecture.md           # Documentation technique
├── arduino/                      # Dossiers des modules Arduino
│   ├── bluetooh/
│   │   └── bluetooh.ino
│   ├── humidite/
│   │   └── humidite.ino
│   └── leds/
│       └── leds.ino
```

## Installation

### 1. Préparer le Raspberry Pi

- Assurez-vous que `python3`, `pip`, `vlc`, `pygame`, et les bibliothèques sont installés.
- Connectez l'Arduino au port USB.

### 2. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### 3. Lancer le script principal

```bash
python paola_complet.py
```

## Dépendances Python

- gTTS
- SpeechRecognition
- pygame
- pytube
- requests
- python-vlc

## Auteure

**Awa Ndiaye**  

Étudiante ingénieure en informatique à l’ESP Dakar  
