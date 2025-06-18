const int redLEDPin = 3;    // Pin de la LED rouge
const int greenLEDPin = 5;  // Pin de la LED verte
const int blueLEDPin = 6;   // Pin de la LED bleue

void setup() {
    Serial.begin(9600);     // Initialiser la communication série
    pinMode(redLEDPin, OUTPUT);   // Définir les pins comme sortie
    pinMode(greenLEDPin, OUTPUT);
    pinMode(blueLEDPin, OUTPUT);
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read();  // Lire la commande série
        executeCommand(command);       // Exécuter la commande
    }
}

void executeCommand(char command) {
    switch (command) {
        case 'R':  // Allumer la LED rouge
            digitalWrite(redLEDPin, HIGH);
            Serial.println("LED rouge allumée");
            break;
        case 'r':  // Éteindre la LED rouge
            digitalWrite(redLEDPin, LOW);
            Serial.println("LED rouge éteinte");
            break;
        case 'G':  // Allumer la LED verte
            digitalWrite(greenLEDPin, HIGH);
            Serial.println("LED verte allumée");
            break;
        case 'g':  // Éteindre la LED verte
            digitalWrite(greenLEDPin, LOW);
            Serial.println("LED verte éteinte");
            break;
        case 'B':  // Allumer la LED bleue
            digitalWrite(blueLEDPin, HIGH);
            Serial.println("LED bleue allumée");
            break;
        case 'b':  // Éteindre la LED bleue
            digitalWrite(blueLEDPin, LOW);
            Serial.println("LED bleue éteinte");
            break;
        default:
            Serial.println("Commande inconnue");
            break;
    }
}
