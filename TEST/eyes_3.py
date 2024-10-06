import cv2
import dlib
import face_recognition
import numpy as np

# Charger le modèle de détection de visage et les prédicteurs de landmarks
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
predictor_path = "/home/nathan/Documents/PROJECT/Reconnaissace_Facial/68_points-master/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

# Charger et encoder les images des personnes connues
image_person1 = face_recognition.load_image_file("/home/nathan/Documents/PROJECT/Reconnaissace_Facial/face/Elon musk.jpeg")
encoding_person1 = face_recognition.face_encodings(image_person1)[0]

# Stocker les encodages et les noms
known_face_encodings = [encoding_person1]
known_face_names = ["Elon Musk"]

# Ouvrir la webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir l'image en niveaux de gris
    
    # Détecter les visages dans l'image en niveaux de gris
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        print("Visages détectés")
    else:
        print("Aucun visage détecté")

    # Identifier les visages
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    print("Emplacements des visages détectés :", face_locations)
    print("Encodages des visages détectés :", face_encodings)

    for (x, y, w, h) in faces:
        # Dessiner un rectangle autour du visage détecté
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Calculer les coordonnées du carré pour le suivre
        square_size = min(w, h)
        top_left = (x + w // 2 - square_size // 2, y + h // 2 - square_size // 2)
        bottom_right = (x + w // 2 + square_size // 2, y + h // 2 + square_size // 2)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 3)  # Dessiner le carré en vert

        # Convertir les coordonnées du visage en un objet dlib.rectangle
        dlib_rect = dlib.rectangle(x, y, x+w, y+h)
        
        # Prédire les landmarks du visage
        shape = predictor(gray, dlib_rect)
        
        # Dessiner les points des landmarks
        for i in range(68):
            part = shape.part(i)
            cv2.circle(frame, (part.x, part.y), 2, (0, 255, 0), -1)  # Dessiner un petit cercle à chaque landmark

    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        # Comparer les encodages
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        else:
            name = "Inconnu"
        
        # Dessiner un cadre autour du visage avec le nom
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Afficher le nom juste en dessous du cadre
        text = name
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        text_x = left
        text_y = bottom + text_size[1] + 10  # Position du texte juste en dessous du cadre
        
        # Ajouter un fond pour améliorer la visibilité du texte
        cv2.rectangle(frame, (text_x - 1, text_y - text_size[1] - 1), (text_x + text_size[0] + 1, text_y + 1), (0, 0, 0), -1)
        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Afficher la vidéo dans la fenêtre
    cv2.imshow('Reconnaissance Faciale avec Landmarks', frame)

    # Appuyer sur 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Libérer la caméra
cv2.destroyAllWindows()  # Fermer toutes les fenêtres ouvertes
