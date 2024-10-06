import cv2
import face_recognition
import numpy as np

# Charger et encoder les images des personnes connues
image_person1 = face_recognition.load_image_file("/path/to/person1.jpg")
encoding_person1 = face_recognition.face_encodings(image_person1)[0]

image_person2 = face_recognition.load_image_file("/path/to/person2.jpg")
encoding_person2 = face_recognition.face_encodings(image_person2)[0]

# Stocker les encodages et les noms
known_face_encodings = [encoding_person1, encoding_person2]
known_face_names = ["Ange Michel", "Person 2"]

# Ouvrir la webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    # Redimensionner l'image pour accélérer la détection
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]  # Convertir BGR à RGB
    
    # Identifier les visages dans l'image
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        else:
            name = "Inconnu"
        
        # Dessiner un cadre autour du visage avec le nom
        for (top, right, bottom, left), name in zip(face_locations, [name]):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    cv2.imshow('Identification de visages', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
