char command = ' '; // Variable pour stocker la commande Bluetooth reçue
int LED_PIN=13;
void setup() {
    Serial.begin(9600); // Initialiser la communication série
    pinMode(LED_PIN, OUTPUT); // Définir le pin de la LED comme sortie
}

void loop() {
    if (Serial.available() > 0) {
        command = Serial.read(); // Lire la commande Bluetooth
        if (command == 'H') {
            digitalWrite(LED_PIN, HIGH); // Allumer la LED
        } else if (command == 'L') {
            digitalWrite(LED_PIN, LOW); // Éteindre la LED
        }
    }
}
