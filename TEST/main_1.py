import cv2

# Charger le modèle de détection de visage
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Ouvrir la webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Détecter les visages
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Dessiner un carré au centre de l'image pour test
    height, width = frame.shape[:2]
    square_size = 100
    top_left = (width // 2 - square_size // 2, height // 2 - square_size // 2)
    bottom_right = (width // 2 + square_size // 2, height // 2 + square_size // 2)
    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 3)  # Dessiner le carré en vert
    
    # Dessiner un rectangle autour de chaque visage détecté
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # Afficher la vidéo dans la fenêtre redimensionnable
    cv2.imshow('Video', frame)

    # Appuyer sur 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
