import mysql.connector
from mysql.connector import Error
import datetime

def connect():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port='3306',
            database='projet_dbpy',
            user='cpnv',
            password='Pa$$w0rd',
            buffered=True,
            autocommit=True
        )
        if connection.is_connected():
            print(f"Connecté à la base de données MySQL (version {connection.get_server_info()})")
            return connection
    except Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

def save_result(exercise_code, user_nickname, start_date, duration, nb_trials, nb_ok):
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()

            # Récupérer l'ID de l'utilisateur ou l'ajouter s'il n'existe pas
            cursor.execute(f"SELECT id FROM Users WHERE nickname = '{user_nickname}'")
            user_row = cursor.fetchone()

            if user_row:
                user_id = user_row[0]
            else:
                # Ajouter l'utilisateur et récupérer l'ID
                cursor.execute(f"INSERT INTO Users (nickname) VALUES ('{user_nickname}')")
                connection.commit()
                user_id = cursor.lastrowid  # Récupérer l'ID après l'ajout

            # Récupérer l'ID de l'exercice
            cursor.execute(f"SELECT id FROM exercices WHERE exercice_code = '{exercise_code}'")
            exercise_row = cursor.fetchone()

            if exercise_row:
                exercise_id = exercise_row[0]
            else:
                print(f"L'exercice avec le code '{exercise_code}' n'a pas été trouvé dans la base de données.")
                return

            # Insérer le résultat dans la table results (en excluant la colonne 'id')
            cursor.execute(
                f"INSERT INTO results (hours, date_time, number_try, number_ok, Users_id, exercices_id) "
                f"VALUES ('{duration}', '{start_date}', {nb_trials}, {nb_ok}, {user_id}, {exercise_id})"
            )

            connection.commit()
            print("Résultat enregistré avec succès")

    except Error as e:
        print(f"Erreur lors de l'enregistrement du résultat dans la base de données: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")
