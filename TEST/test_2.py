import cv2
import dlib

# Charger les modèles de détection de visage et de landmarks
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
predictor_path = "68_points-master/shape_predictor_68_face_landmarks.dat"  # Chemin vers le fichier .dat du prédicteur de landmarks
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

# Ouvrir la webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Lire une image depuis la webcam
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir l'image en niveaux de gris
    
    # Détecter les visages
    faces = detector(gray)
    
    for face in faces:
        # Dessiner un rectangle autour du visage détecté
        x, y, w, h = (face.left(), face.top(), face.width(), face.height())
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Prédire les landmarks du visage
        shape = predictor(gray, face)
        
        # Dessiner les points des landmarks
        for i in range(68):  # Il y a 68 points dans le modèle
            part = shape.part(i)
            cv2.circle(frame, (part.x, part.y), 2, (0, 255, 0), -1)  # Dessiner un petit cercle à chaque landmark

    # Afficher la vidéo avec les landmarks et le visage détecté
    cv2.imshow('Landmarks Facials', frame)

    # Appuyer sur 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Libérer la caméra
cv2.destroyAllWindows()  # Fermer toutes les fenêtres ouvertes
