import serial
from datetime import datetime
import uuid
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firestore
cred = credentials.Certificate("clave-firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

tarjetas_permitidas = {
    "326eb73": {"nombre": "Juan Pérez", "cedula": "1712345678"},
    "4682c295f2b80": {"nombre": "Joselyn Carrión", "cedula": "1723456789"},
    "4694d52987680": {"nombre": "Brayan Chango", "cedula": "1751148618"},
    "445f42c91a90": {"nombre": "David Minango", "cedula": "1716042435"}
}

arduino = serial.Serial('COM5', 9600)

print("Esperando tarjetas...")

while True:
    if arduino.in_waiting:
        uid = arduino.readline().decode().strip().lower()

        # 🔹 Filtrar mensajes que no sean UIDs (evita "servo en reposo")
        if not all(c in "0123456789abcdef" for c in uid):
            continue

        print(f"UID recibido: {uid}")

        ahora = datetime.now()
        fecha = ahora.strftime("%Y-%m-%d")
        hora_actual = ahora.strftime("%Y-%m-%d %H:%M:%S")

        datos_usuario = tarjetas_permitidas.get(uid)

        if datos_usuario:
            nombre = datos_usuario["nombre"]
            cedula = datos_usuario["cedula"]
            print(f"✔️ Acceso permitido a {nombre}")

            registros_ref = db.collection("registros")

            query = registros_ref.where("uid", "==", uid)\
                                 .where("fecha", "==", fecha)\
                                 .order_by("hora_entrada", direction=firestore.Query.DESCENDING)\
                                 .limit(1)
            resultados = query.stream()

            documento_encontrado = None
            for doc in resultados:
                documento_encontrado = doc
                break

            if documento_encontrado:
                datos_registro = documento_encontrado.to_dict()
                if "hora_salida" not in datos_registro or datos_registro["hora_salida"] == "":
                    registros_ref.document(documento_encontrado.id).update({
                        "hora_salida": hora_actual
                    })
                    print(f"⏺️ Se registró la **salida** de {nombre}")
                else:
                    nuevo_id = str(uuid.uuid4())
                    registros_ref.document(nuevo_id).set({
                        "nombre": nombre,
                        "cedula": cedula,
                        "uid": uid,
                        "fecha": fecha,
                        "hora_entrada": hora_actual,
                        "hora_salida": ""
                    })
                    print(f"⏺️ Se registró la **entrada** de {nombre}")
            else:
                nuevo_id = str(uuid.uuid4())
                registros_ref.document(nuevo_id).set({
                    "nombre": nombre,
                    "cedula": cedula,
                    "uid": uid,
                    "fecha": fecha,
                    "hora_entrada": hora_actual,
                    "hora_salida": ""
                })
                print(f"⏺️ Se registró la **entrada** de {nombre}")

            # Solo se envía si es válido
            arduino.write(b'OK\n')

        else:
            print("❌ Acceso denegado")

