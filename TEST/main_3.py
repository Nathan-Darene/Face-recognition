import cv2
import dlib

# Charger le modèle de détection de visage
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
predictor_path = "/home/nathan/Documents/PROJECT/Reconnaissace_Facial/68_points-master/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

# Ouvrir la webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Lire une image depuis la webcam
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir l'image en niveaux de gris
    
    # Détecter les visages dans l'image en niveaux de gris
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Si des visages sont détectés, dessiner un carré autour de chaque visage
    for (x, y, w, h) in faces:
        # Dessiner un rectangle autour du visage détecté
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Calculer les coordonnées du carré pour le suivre
        square_size = min(w, h)  # Utiliser la taille du visage pour le carré
        top_left = (x + w // 2 - square_size // 2, y + h // 2 - square_size // 2)
        bottom_right = (x + w // 2 + square_size // 2, y + h // 2 + square_size // 2)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 3)  # Dessiner le carré en vert

        # Convertir les coordonnées du visage en un objet dlib.rectangle
        dlib_rect = dlib.rectangle(x, y, x+w, y+h)
        
        # Prédire les landmarks du visage
        
        shape = predictor(gray, dlib_rect)
        
        # Dessiner les points des landmarks
        for i in range(68):  # Il y a 68 points dans le modèle
            part = shape.part(i)
            cv2.circle(frame, (part.x, part.y), 2, (0, 255, 0), -1)  # Dessiner un petit cercle à chaque landmark

    # Afficher la vidéo dans la fenêtre
    cv2.imshow('Landmarks Facials', frame)

    # Appuyer sur 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Libérer la caméra
cv2.destroyAllWindows()  # Fermer toutes les fenêtres ouvertes
