const int humiditySensorPin = A0; // Pin analogique pour le capteur d'humidité
int humidityValue = 0;

void setup() {
    Serial.begin(9600); // Initialiser la communication série
    pinMode(humiditySensorPin, INPUT);
}

void loop() {
    humidityValue = analogRead(humiditySensorPin); // Lire la valeur du capteur
    Serial.println(humidityValue); // Envoyer la valeur au Raspberry Pi via Serial

    delay(1000); // Attendre une seconde avant de lire à nouveau
}
