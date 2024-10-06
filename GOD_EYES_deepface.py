import cv2
import dlib
import numpy as np
# from deepface import DeepFace
from info_users import *

# Charger le modèle de détection de visage et les prédicteurs de landmarks
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
predictor_path = "/home/nathan/Documents/PROJECT/Reconnaissace_Facial/68_points-master/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

# Ouvrir la webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir l'image en niveaux de gris
    
    # Détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        print("Visages détectés")
    else:
        print("Aucun visage détecté")

    # Identifier les visages
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Détection de visages avec DeepFace
    for (x, y, w, h) in faces:
        # Extraire la région du visage
        face_frame = rgb_frame[y:y+h, x:x+w]

        # Sauvegarder temporairement l'image du visage pour la vérification avec DeepFace
        cv2.imwrite("detected_face.jpg", face_frame)
        
        name = "Inconnu"  # Par défaut, on marque le visage comme inconnu

        try:
            # Comparer avec chaque visage connu dans `known_face_names`
            for i, known_face in enumerate(known_face_names):
                result = DeepFace.verify(img1_path="detected_face.jpg", img2_path=f"{known_face}.jpg", enforce_detection=False)

                # Si le visage est reconnu
                if result["verified"]:
                    name = known_face
                    break
        except Exception as e:
            print("Erreur lors de la reconnaissance faciale:", e)
        
        print(f"Nom détecté : {name}")

        # Dessiner un cadre autour du visage détecté
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Calculer les coordonnées du carré pour le suivi
        square_size = min(w, h)
        top_left = (x + w // 2 - square_size // 2, y + h // 2 - square_size // 2)
        bottom_right = (x + w // 2 + square_size // 2, y + h // 2 + square_size // 2)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 3)

        # Convertir en rectangle dlib et prédire les landmarks
        dlib_rect = dlib.rectangle(x, y, x + w, y + h)
        shape = predictor(gray, dlib_rect)

        # Dessiner les landmarks
        for i in range(68):  # Il y a 68 points dans le modèle
            part = shape.part(i)
            cv2.circle(frame, (part.x, part.y), 2, (0, 255, 0), -1)

        # Ajouter le nom du visage
        text = f"{name}"
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        text_x = x
        text_y = y - 10  # Juste au-dessus du visage
        cv2.rectangle(frame, (text_x - 1, text_y - text_size[1] - 1), (text_x + text_size[0] + 1, text_y + 1), (0, 0, 0), -1)
        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Afficher la vidéo
    cv2.imshow('GOD EYES', frame)

    # Quitter en appuyant sur 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
