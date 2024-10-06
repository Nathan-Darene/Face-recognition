import cv2

# Charger le modèle de détection de visage
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Ouvrir la webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Lire une image depuis la webcam
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir l'image en niveaux de gris
    
    # Détecter les visages
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    print(f"Number of faces detected: {len(faces)}")  # Afficher le nombre de visages détectés
    
    for (x, y, w, h) in faces:
        # Dessiner un rectangle autour de chaque visage détecté
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Calculer le centre du visage pour placer le carré
        center_x = x + w // 2
        center_y = y + h // 2
        square_size = min(w, h) // 2  # Ajuster la taille du carré
        
        # Assurer que le carré est dans les limites de l'image
        top_left_x = max(center_x - square_size, 0)
        top_left_y = max(center_y - square_size, 0)
        bottom_right_x = min(center_x + square_size, frame.shape[1])
        bottom_right_y = min(center_y + square_size, frame.shape[0])
        
        # Afficher les coordonnées pour la vérification
        print(f"Face detected at: x={x}, y={y}, w={w}, h={h}")
        print(f"Center of face: ({center_x}, {center_y})")
        print(f"Top left of square: ({top_left_x}, {top_left_y})")
        print(f"Bottom right of square: ({bottom_right_x}, {bottom_right_y})")
        
        # Dessiner le carré en vert
        cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 3)
    
    # Afficher la vidéo dans la fenêtre
    cv2.imshow('Video', frame)

    # Appuyer sur 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cap.release()  # Libérer la caméra
cv2.destroyAllWindows()  # Fermer toutes les fenêtres ouvertes

