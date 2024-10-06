import cv2
import dlib
import face_recognition
import numpy as np


# Charger et encoder les images des personnes connues
image_person1 = face_recognition.load_image_file("/home/nathan/Documents/PROJECT/Reconnaissace_Facial/face/Elon musk.jpeg")
encoding_person1 = face_recognition.face_encodings(image_person1)[0]

# Stocker les encodages et les noms
known_face_encodings = [encoding_person1]
known_face_names = ["Elon musk"]
