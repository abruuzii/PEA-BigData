Proyecto de Control de Acceso con RFID, Arduino y Firestore

Este proyecto consiste en un sistema de control de acceso que utiliza un lector RFID y un Arduino UNO para validar tarjetas. El sistema determina si una tarjeta es válida o no, controla un servomotor para simular la apertura de una puerta y registra las entradas/salidas en una base de datos en la nube (Firebase Firestore).

Concepto del Proyecto

El sistema permite registrar la asistencia o accesos de personas mediante tarjetas RFID.

- La validación de las tarjetas se realiza en un programa en Python, donde se almacenan los UID válidos.

- Cuando se detecta una tarjeta válida:

  - El Arduino activa el servomotor (abre la puerta).

  - Python envía el registro (usuario, UID, hora y acción) a Firestore.

- Desde una página web conectada a Firestore, se pueden visualizar en tiempo real los registros almacenados.

Materiales Utilizados

- Arduino UNO

- Lector RFID RC522

- Tarjetas y llaveros RFID

- Servomotor (SG90 / continuo, según configuración)

- Cables Macho-Hembra y Macho-Macho

- PC con Python instalado

- Cuenta en Firebase con Firestore habilitado

Software y Librerías

- Arduino IDE (para programar el Arduino)

- Librerías Arduino:

  - MFRC522 (lector RFID)

  - Servo.h (servomotor)

- Python 3.x con librerías:

  - pyserial (comunicación con Arduino)

  - firebase-admin (conexión a Firestore)

  - datetime (registro de fechas y horas)

Pasos para Montar el Proyecto

1. Conexión del hardware

- Conectar el módulo RFID RC522 al Arduino UNO (SPI).

- Conectar el servomotor al pin PWM del Arduino.

- Conectar la alimentación y tierra comunes.

2. Programar el Arduino

- Subir el código que permite recibir comandos desde Python y mover el servomotor.

3. Configurar Firebase

- Crear un proyecto en Firebase Console

- Habilitar Firestore en modo prueba.

- Descargar la clave privada de servicio y guardarla en el proyecto Python.

4. Programar en Python

- El archivo .py del repositorio realiza lo siguiente:

  -Lee el UID de la tarjeta desde el Arduino.

  -Verifica si el UID está en la lista de tarjetas válidas.

  -Envía el registro (usuario, UID, acción y fecha/hora) a Firestore.

5. Página Web de Visualización

El archivo .html del repositorio lee los registros en tiempo real desde Firestore y muestra las entradas y salidas de cada usuario con fecha y hora, además de incluir un buscador que se puede filtrar por el número de cédula.
