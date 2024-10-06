import face_recognition
import numpy as np
import mysql.connector
import json

try:
    # Connexion à la base de données MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # Change en fonction de ton utilisateur MySQL
        password="nathan_85/@",  # Change en fonction de ton mot de passe
        database="view_face"
    )

    cursor = connection.cursor()

    def get_all_faces_from_db():
        cursor.execute("SELECT name, encoding FROM face")
        results = cursor.fetchall()
        known_face_encodings = []
        known_face_names = []

        for row in results:
            name = row[0]
            encoding = np.array(json.loads(row[1]))  # Convertir le JSON en tableau NumPy
            known_face_encodings.append(encoding)
            known_face_names.append(name)

        return known_face_names, known_face_encodings

    # Récupérer les visages connus
    known_face_names, known_face_encodings = get_all_faces_from_db()

finally:
    # Assure que le curseur et la connexion sont fermés correctement
    if cursor:
        cursor.close()
    if connection:
        connection.close()
