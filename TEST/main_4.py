import cv2

# Charger les modèles de détection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
nose_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_mcs_nose.xml')
mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_mcs_mouth.xml')

# Ouvrir la webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Lire une image depuis la webcam
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir l'image en niveaux de gris
    
    # Détecter les visages
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        # Extraire la région du visage
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        # Détecter les yeux
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            eye_center = (x + ex + ew // 2, y + ey + eh // 2)
            cv2.circle(frame, eye_center, 2, (0, 255, 0), -1)
            print(f"Eye center: {eye_center}")  # Afficher les coordonnées des yeux
        
        # Détecter le nez
        noses = nose_cascade.detectMultiScale(roi_gray)
        for (nx, ny, nw, nh) in noses:
            nose_center = (x + nx + nw // 2, y + ny + nh // 2)
            cv2.circle(frame, nose_center, 2, (0, 0, 255), -1)
            print(f"Nose center: {nose_center}")  # Afficher les coordonnées du nez
        
        # Détecter la bouche
        mouths = mouth_cascade.detectMultiScale(roi_gray, 1.5, 11)
        for (mx, my, mw, mh) in mouths:
            mouth_center = (x + mx + mw // 2, y + my + mh // 2)
            cv2.circle(frame, mouth_center, 2, (255, 255, 0), -1)
            print(f"Mouth center: {mouth_center}")  # Afficher les coordonnées de la bouche
        
        # Calculer le centre du visage pour placer le carré
        center_x = x + w // 2
        center_y = y + h // 2
        square_size = min(w, h) // 2  # Ajuster la taille du carré
        
        top_left = (center_x - square_size, center_y - square_size)
        bottom_right = (center_x + square_size, center_y + square_size)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 3)  # Dessiner le carré en vert
    
    # Afficher la vidéo dans la fenêtre
    cv2.imshow('Video', frame)

    # Appuyer sur 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Libérer la caméra
cv2.destroyAllWindows()  # Fermer toutes les fenêtres ouvertes
