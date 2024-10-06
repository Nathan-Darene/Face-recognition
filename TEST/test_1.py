import cv2

# Charger les modèles de détection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Ouvrir la webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Lire une image depuis la webcam
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir l'image en niveaux de gris
    
    # Détecter les visages
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        # Dessiner un rectangle autour de chaque visage détecté
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Détecter les yeux dans la région du visage
        roi_gray = gray[y:y+h, x:x+w]  # Région du visage en niveaux de gris
        roi_color = frame[y:y+h, x:x+w]  # Région du visage en couleur
        
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)  # Détection des yeux
        print(f"Number of eyes detected: {len(eyes)}")  # Vérifier le nombre d'yeux détectés
        
        for (ex, ey, ew, eh) in eyes:
            # Dessiner des cercles pour chaque œil détecté
            center_of_eye = (ex + ew // 2, ey + eh // 2)
            radius_of_eye = ew // 2
            cv2.circle(roi_color, center_of_eye, radius_of_eye, (0, 255, 0), 2)
    
    # Afficher la vidéo dans la fenêtre
    cv2.imshow('Video', frame)

    # Appuyer sur 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Libérer la caméra
cv2.destroyAllWindows()  # Fermer toutes les fenêtres ouvertes
