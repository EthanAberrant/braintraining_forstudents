""" Ethan Martin
    Projet DBPY
    le 05.12.23"""

# database.py
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


def get_all_results_with_exercise():
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor(dictionary=True)

            # Récupérer tous les résultats avec les informations de l'exercice
            cursor.execute("""
                SELECT Users.nickname, results.hours, results.date_time, results.number_try, results.number_ok,
                       exercices.exercice_code AS exercise_code
                FROM results
                INNER JOIN Users ON results.Users_id = Users.id
                INNER JOIN exercices ON results.exercices_id = exercices.id
                ORDER BY results.date_time DESC
            """)
            all_results = cursor.fetchall()

            if all_results:
                return all_results
            else:
                print("Aucun résultat trouvé dans la base de données.")
                return None

    except Error as e:
        print(f"Erreur lors de la récupération des résultats : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


def get_user_id(user_nickname):
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()

            # Récupérer l'ID de l'utilisateur
            cursor.execute(f"SELECT id FROM Users WHERE nickname = '{user_nickname}'")
            user_row = cursor.fetchone()

            print(f"Résultat de la requête pour l'utilisateur '{user_nickname}': {user_row}")

            if user_row:
                user_id = user_row[0]
                return user_id
            else:
                print(f"L'utilisateur avec le pseudo '{user_nickname}' n'a pas été trouvé dans la base de données.")
                return None

    except Error as e:
        print(f"Erreur lors de la récupération de l'ID de l'utilisateur : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


def get_exercise_id(exercise_code):
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()

            # Récupérer l'ID de l'exercice
            cursor.execute(f"SELECT id FROM exercices WHERE exercice_code = '{exercise_code}'")
            exercise_row = cursor.fetchone()

            if exercise_row:
                exercise_id = exercise_row[0]
                return exercise_id
            else:
                print(f"L'exercice avec le code '{exercise_code}' n'a pas été trouvé dans la base de données.")
                return None

    except Error as e:
        print(f"Erreur lors de la récupération de l'ID de l'exercice : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


def save_result(exercise_code, user_pseudo, start_date, duration, nb_trials, nb_ok):
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()

            # Récupérer l'ID de l'utilisateur ou l'ajouter s'il n'existe pas
            user_id = get_user_id(user_pseudo)

            if user_id is not None:
                print(f"Utilisateur '{user_pseudo}' existe déjà. ID: {user_id}")
            else:
                # Ajouter l'utilisateur et récupérer l'ID
                cursor.execute(f"INSERT INTO Users (nickname) VALUES ('{user_pseudo}')")
                connection.commit()
                user_id = cursor.lastrowid  # Récupérer l'ID après l'ajout
                print(f"Utilisateur '{user_pseudo}' ajouté avec succès. ID: {user_id}")

            # Affichez le pseudo correctement ici
            print("Résultat enregistré avec succès pour l'utilisateur:", user_pseudo)

            # Ajouter l'exercice s'il n'existe pas
            exercise_id = get_exercise_id(exercise_code)
            if exercise_id is None:
                cursor.execute(f"INSERT INTO exercices (exercice_code) VALUES ('{exercise_code}')")
                connection.commit()
                exercise_id = cursor.lastrowid  # Récupérer l'ID après l'ajout
                print(f"Exercice '{exercise_code}' ajouté avec succès. ID: {exercise_id}")

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


def get_filtered_results(exercise_filter, nickname_filter, start_date_filter):
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor(dictionary=True)

            # Construire la requête SQL en fonction des filtres fournis
            query = """
                SELECT results.id, Users.nickname, results.hours, results.date_time, results.number_try, results.number_ok,
                       exercices.exercice_code AS exercise_code
                FROM results
                INNER JOIN Users ON results.Users_id = Users.id
                INNER JOIN exercices ON results.exercices_id = exercices.id
                WHERE 1
            """

            if exercise_filter:
                query += f" AND exercices.exercice_code = '{exercise_filter}'"

            if nickname_filter:
                query += f" AND Users.nickname = '{nickname_filter}'"

            if start_date_filter:
                query += f" AND results.date_time >= '{start_date_filter}'"

            query += " ORDER BY results.date_time DESC"

            # Exécuter la requête
            cursor.execute(query)
            filtered_results = cursor.fetchall()

            if filtered_results:
                return filtered_results
            else:
                print("Aucun résultat trouvé avec les filtres spécifiés.")
                return None

    except Error as e:
        print(f"Erreur lors de la récupération des résultats filtrés : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


def save_info05_results(user_pseudo, start_date, duration, nb_trials, nb_ok):
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()

            # Récupérer l'ID de l'utilisateur ou l'ajouter s'il n'existe pas
            user_pseudo = entry_pseudo.get()
            user_id = get_user_id(user_pseudo)

            if user_id is not None:
                print(f"Utilisateur '{user_pseudo}' existe déjà. ID: {user_id}")
            else:
                # Ajouter l'utilisateur et récupérer l'ID
                cursor.execute(f"INSERT INTO Users (nickname) VALUES ('{user_pseudo}')")
                connection.commit()
                user_id = cursor.lastrowid  # Récupérer l'ID après l'ajout
                print(f"Utilisateur '{user_pseudo}' ajouté avec succès. ID: {user_id}")

            # Affichez le pseudo correctement ici
            print("Résultat enregistré avec succès pour l'utilisateur:", user_pseudo)

            # Ajouter l'exercice INFO05 s'il n'existe pas
            exercise_code = "INFO05"
            exercise_id = get_exercise_id(exercise_code)
            if exercise_id is None:
                cursor.execute(f"INSERT INTO exercices (exercice_code) VALUES ('{exercise_code}')")
                connection.commit()
                exercise_id = cursor.lastrowid  # Récupérer l'ID après l'ajout
                print(f"Exercice '{exercise_code}' ajouté avec succès. ID: {exercise_id}")

            # Insérer le résultat dans la table results (en excluant la colonne 'id')
            cursor.execute(
                f"INSERT INTO results (hours, date_time, number_try, number_ok, Users_id, exercices_id) "
                f"VALUES ('{duration}', '{start_date}', {nb_trials}, {nb_ok}, {user_id}, {exercise_id})"
            )

            connection.commit()
            print("Résultat enregistré avec succès pour l'exercice INFO05")

    except Error as e:
        print(f"Erreur lors de l'enregistrement du résultat dans la base de données: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


def delete_result(result_id):
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()

            # Supprimer le résultat avec l'ID spécifié
            cursor.execute(f"DELETE FROM results WHERE id = {result_id}")

            connection.commit()
            print(f"Résultat avec l'ID {result_id} supprimé avec succès")

    except Error as e:
        print(f"Erreur lors de la suppression du résultat : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


def update_result(result_id, new_hours, new_number_try, new_number_ok):
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()

            # Mettre à jour le résultat avec les nouvelles valeurs
            cursor.execute(f"""
                UPDATE results
                SET hours = '{new_hours}', number_try = {new_number_try}, number_ok = {new_number_ok}
                WHERE id = {result_id}
            """)

            connection.commit()
            print(f"Résultat avec l'ID {result_id} mis à jour avec succès")

    except Error as e:
        print(f"Erreur lors de la mise à jour du résultat : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


def get_result_info(result_id):
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor(dictionary=True)

            # Récupérer les informations du résultat avec l'ID spécifié
            cursor.execute(f"""
                SELECT hours, number_try, number_ok
                FROM results
                WHERE id = {result_id}
            """)
            result_info = cursor.fetchone()

            if result_info:
                return result_info
            else:
                print(f"Aucune information trouvée pour le résultat avec l'ID {result_id}")
                return None

    except Error as e:
        print(f"Erreur lors de la récupération des informations du résultat : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")
