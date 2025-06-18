# Architecture du système - Assistant Vocal Paola

Ce document décrit l'architecture technique de l'assistant vocal Paola, basé sur un Raspberry Pi et des modules Arduino.

## Vue d'ensemble

L’assistant vocal « Paola » repose sur une communication bidirectionnelle entre un Raspberry Pi (côté traitement logiciel) et un Arduino Uno (côté composants physiques). Le Raspberry Pi capture, traite et interprète la voix de l’utilisateur, puis interagit avec l’Arduino via un port série pour déclencher des actions physiques (LEDs, capteurs).

```
Utilisateur → Microphone USB → Raspberry Pi
            → Python (speech_recognition)
            → Traitement commande → Action
            → Synthèse vocale (gTTS) → Haut-parleur

                                 ↓
                         Communication série
                                 ↓
                           Arduino Uno
                  (LEDs, capteurs, LCD, etc.)
```

## Composants logiciels

### Côté Raspberry Pi (Python)

- `speech_recognition` : détecte la voix et convertit en texte
- `gTTS` + `pygame` : transforme le texte en audio et le lit
- `requests` : requêtes HTTP pour météo et musique
- `pytube`, `vlc` : récupération et lecture d’audio depuis YouTube
- `serial` : communication avec l’Arduino via USB

### Côté Arduino (firmware `.ino`)

- **leds.ino** : active/éteint les LEDs RGB sur commande reçue
- **humidite.ino** : lit le niveau d’humidité et le transmet par port série
- **bluetooth.ino** : (optionnel) module HC-05 pour pilotage sans fil

## Fonctionnement vocal

1. L’utilisateur dit : “Paola, allume la LED rouge”
2. Le Raspberry Pi détecte le mot-clé (“Paola”), puis écoute la commande
3. Le texte est analysé pour identifier l’action
4. Si c’est une commande physique, un signal est envoyé à l’Arduino via `pyserial`
5. Si c’est une commande logique (météo, musique), une API est appelée et le résultat est lu vocalement

## Communication série (exemples)

| Commande vocale         | Code série envoyé |
|-------------------------|-------------------|
| allumer LED rouge       | R                 |
| éteindre LED rouge      | r                 |
| allumer LED verte       | G                 |
| lire humidité           | Lecture depuis Arduino (valeur en %)

## Évolutions possibles

- Ajout d'une interface web ou mobile pour contrôler l'assistant
- Intégration de MQTT pour les objets connectés
- Ajout de reconnaissance faciale avec OpenCV