from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter as tk

def zoom_image(image, zoom_factor):
    # Récupère les dimensions de l'image
    width, height = image.size
    
    # Calculer les dimensions de l'image zoomée
    new_width = int(width * zoom_factor)
    new_height = int(height * zoom_factor)
    
    # Agrandir l'image
    zoomed_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Recadre l'image zoomée pour qu'elle ait les dimensions originales
    left = (new_width - width) / 2
    top = (new_height - height) / 2
    right = (new_width + width) / 2
    bottom = (new_height + height) / 2
    
    zoomed_image = zoomed_image.crop((left, top, right, bottom))
    
    return zoomed_image