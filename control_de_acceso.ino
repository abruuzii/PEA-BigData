#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define RST_PIN   9
#define SS_PIN   10
#define SERVO_PIN 5

// Ajusta estos si hace falta calibrar el alto
const int STOP_PWM = 90;   // neutro (parado) ~ 88–92 según el servo
const int RUN_PWM  = 0;    // gira (usa 180 si quieres el otro sentido)
const unsigned long RUN_MS = 3000; // tiempo de giro

MFRC522 mfrc522(SS_PIN, RST_PIN);
Servo servo;

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();

  servo.attach(SERVO_PIN);
  servo.write(STOP_PWM);   //⛔️ parado al inicio

  // Si tu programa en PC solo espera el UID, mejor no imprimir textos extra:
  // Serial.println("Esperando tarjetas...");
}

void loop() {
  // Esperar tarjeta nueva
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) return;

  // Construir UID en minúsculas
  String uid = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    uid += String(mfrc522.uid.uidByte[i], HEX);
  }
  uid.toLowerCase();

  // Enviar SOLO el UID a la PC
  Serial.println(uid);

  // Esperar respuesta "OK" / "NO" desde la PC (máx 3 s)
  unsigned long t0 = millis();
  while (!Serial.available()) {
    if (millis() - t0 > 3000) return;
  }

  String respuesta = Serial.readStringUntil('\n');
  respuesta.trim();

  if (respuesta == "OK") {
    // ✅ AHORA sí: primero girar, luego parar
    servo.write(RUN_PWM);      // girar (0 = un sentido; 180 = el otro)
    delay(RUN_MS);             // tiempo de giro
    servo.write(STOP_PWM);     // parar
  } else {
    // Denegado → asegurarse de que quede parado
    servo.write(STOP_PWM);
  }

  // Finalizar comunicación con la tarjeta y evitar lecturas dobles
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();

  // Esperar a que se retire la tarjeta
  while (mfrc522.PICC_IsNewCardPresent() || mfrc522.PICC_ReadCardSerial()) {
    delay(100);
  }

  delay(300); // pequeña pausa
}
