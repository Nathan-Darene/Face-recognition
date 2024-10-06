import mysql.connector


# Connexion à la base de données MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nathan_85/@",
    database="view_face"
)

cursor = connection.cursor()