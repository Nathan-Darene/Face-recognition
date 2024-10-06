import face_recognition
import mysql.connector
import json
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

# Connexion à la base de données MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nathan_85/@",
    database="view_face"
)

cursor = connection.cursor()

# Fonction pour insérer un visage dans la base de données
def add_face_to_db(name, encoding):
    encoding_str = json.dumps(encoding.tolist())  # Convertir en chaîne JSON
    query = "INSERT INTO face (name, encoding) VALUES (%s, %s)"
    cursor.execute(query, (name, encoding_str))
    connection.commit()

# Fonction pour charger une image et encoder le visage
def load_and_encode_image(image_path, name):
    try:
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]  # Encoder l'image
        add_face_to_db(name, encoding)  # Ajouter dans la base de données
        messagebox.showinfo("Succès", f"Le visage de {name} a été ajouté à la base de données.")
    except IndexError:
        messagebox.showerror("Erreur", "Aucun visage détecté dans l'image.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

# Fonction pour choisir une image
def choose_image():
    file_path = filedialog.askopenfilename(title="Choisir une image", filetypes=[("Images", "*.jpg *.jpeg *.png")])
    if file_path:
        display_image(file_path)  # Afficher l'image dans l'interface
    return file_path

# Fonction pour afficher l'image dans l'interface
def display_image(image_path):
    global img_label, image_tk  # Pour maintenir une référence à l'image
    image = Image.open(image_path)
    image = image.resize((200, 200))  # Redimensionner l'image pour qu'elle tienne dans l'interface
    image_tk = ctk.CTkImage(light_image=image, size=(200, 200))
    img_label.configure(image=image_tk)  # Afficher l'image dans le label
    img_label.pack(pady=10)
    button_confirm.pack(pady=20)  # Afficher le bouton "Confirmer" après l'affichage de l'image

# Fonction pour gérer l'ajout du visage après confirmation
def confirm_add_face():
    name = entry_name.get()  # Récupérer le nom
    if not name:
        messagebox.showerror("Erreur", "Veuillez entrer un nom.")
        return

    if not image_path_global:
        messagebox.showerror("Erreur", "Veuillez sélectionner une image.")
        return

    load_and_encode_image(image_path_global, name)  # Charger et encoder l'image

# Afficher la fenêtre d'ajout de visage
def show_add_face_form():
    global image_path_global
    image_path_global = None
    hide_main_menu()  # Masquer le menu principal
    label_add.pack(pady=10)
    entry_name.pack(pady=10)
    button_select_image.pack(pady=10)
    img_label.pack_forget()  # Cacher le cadre d'image au début
    button_confirm.pack_forget()  # Cacher le bouton "Confirmer" au début
    button_back.pack(pady=20)  # Ajouter le bouton retour

# Masquer les formulaires et revenir au menu principal
def go_back_to_main_menu():
    label_add.pack_forget()
    entry_name.pack_forget()
    button_select_image.pack_forget()
    img_label.pack_forget()
    button_confirm.pack_forget()
    label_delete.pack_forget()
    entry_name_delete.pack_forget()
    button_delete.pack_forget()
    button_back.pack_forget()
    show_main_menu()  # Afficher le menu principal

# Masquer le menu principal
def hide_main_menu():
    button_add_face.pack_forget()
    button_delete_face.pack_forget()

# Fonction pour supprimer un visage dans la base de données
def delete_face_from_db(name):
    try:
        query = "DELETE FROM face WHERE name = %s"
        cursor.execute(query, (name,))
        connection.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Succès", f"Le visage de {name} a été supprimé de la base de données avec succés.")
        else:
            messagebox.showwarning("Non trouvé", f"Aucun visage associé à {name} n'a été trouvé.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

# Fonction pour gérer la suppression d'un visage
def delete_face():
    name = entry_name_delete.get()  # Récupérer le nom
    if not name:
        messagebox.showerror("Erreur", "Veuillez entrer un nom à supprimer.")
        return
    
    delete_face_from_db(name)  # Supprimer le visage de la base de données

# Afficher le menu principal
def show_main_menu():
    button_add_face.pack(pady=20)
    button_delete_face.pack(pady=20)

# Fonction pour afficher le formulaire de suppression de visage
def show_delete_face_form():
    hide_main_menu()  # Masquer le menu principal
    label_delete.pack(pady=10)
    entry_name_delete.pack(pady=10)
    button_delete.pack(pady=20)
    button_back.pack(pady=20)

# Fenêtre principale avec CustomTkinter
app = ctk.CTk()
app.title("Gestion des visages")
app.geometry("500x600")
app.configure(fg_color="#2B2B2B")

# Menu principal
button_add_face = ctk.CTkButton(app,fg_color="#2BFF00",text_color="#ffffff", text="Ajouter un visage", command=show_add_face_form)
button_add_face.place(x=0, y=0)

button_delete_face = ctk.CTkButton(app, text="Supprimer un visage", command=show_delete_face_form)

show_main_menu()

# Formulaire pour ajouter un visage
label_add = ctk.CTkLabel(app, text="Ajouter un visage :")
entry_name = ctk.CTkEntry(app, placeholder_text="Nom de l'individu")

# Cadre pour afficher l'image sélectionnée
img_label = ctk.CTkLabel(app, text="")

button_select_image = ctk.CTkButton(app, text="Choisir une image", command=lambda: choose_image())

# Bouton "Confirmer" pour envoyer l'ajout
button_confirm = ctk.CTkButton(app, text="Confirmer", command=confirm_add_face)

# Bouton "Retour" pour revenir au menu principal
button_back = ctk.CTkButton(app, text="Retour", command=go_back_to_main_menu)

# Formulaire pour supprimer un visage
label_delete = ctk.CTkLabel(app, text="Supprimer un visage :")
entry_name_delete = ctk.CTkEntry(app, placeholder_text="Nom du visage à supprimer :")
button_delete = ctk.CTkButton(app, text="Supprimer un visage", command=delete_face)

# Lancer l'application
app.mainloop()

# Fermer la connexion à la base de données
cursor.close()
connection.close()
