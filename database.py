""" Ethan Martin
    Projet DBPY
    le 15.12.23"""

import mysql.connector
from mysql.connector import Error
import datetime


# Connection a la base de donnée
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


# La fonction récupère les résultats des utilisateurs avec les détails de l'exercice depuis la base de données et les retourne sous forme de liste de dictionnaires triée par date.

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


# La fonction récupère l'ID de l'utilisateur en utilisant le pseudo fourni et renvoie l'ID s'il est trouvé, sinon affiche un message d'absence.

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


# La fonction enregistre les résultats d'un exercice pour un utilisateur donné
# ajoutant l'utilisateur et l'exercice s'ils n'existent pas encore dans la base de données.

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


# La fonction récupère les résultats filtrés en fonction des paramètres fournis,

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


# La fonction enregistre les résultats spécifiques à l'exercice INFO05 pour un utilisateur donné

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


# La fonction supprime le résultat avec l'ID spécifié et
# vérifie si l'utilisateur associé n'a plus aucun résultat, et le supprime également le cas échéant.

def delete_result(result_id):
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()

            # Récupérer l'ID de l'utilisateur associé au résultat
            cursor.execute(f"SELECT Users_id FROM results WHERE id = {result_id}")
            user_id = cursor.fetchone()

            # Supprimer le résultat avec l'ID spécifié
            cursor.execute(f"DELETE FROM results WHERE id = {result_id}")
            connection.commit()

            # Vérifier si la suppression a eu lieu avec succès
            if cursor.rowcount > 0:
                print(f"Résultat avec l'ID {result_id} supprimé avec succès")

                # Vérifier si l'utilisateur associé n'a plus aucun résultat
                cursor.execute(f"SELECT id FROM results WHERE Users_id = {user_id[0]}")
                remaining_results = cursor.fetchall()

                if not remaining_results:
                    # Aucun autre résultat trouvé pour cet utilisateur, supprimer l'utilisateur
                    cursor.execute(f"DELETE FROM Users WHERE id = {user_id[0]}")
                    connection.commit()
                    print(f"Utilisateur avec l'ID {user_id[0]} supprimé car il n'a plus de résultats.")

            else:
                print(f"Aucun résultat trouvé avec l'ID {result_id}. La suppression a peut-être échoué.")

    except Error as e:
        print(f"Erreur lors de la suppression du résultat : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


# La fonction met à jour les informations d'un résultat spécifié avec de nouvelles valeurs
def update_result(result_id, new_hours, new_number_try, new_number_ok, new_pseudo=None, new_game=None):
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()

            # Récupérer les informations actuelles du résultat
            result_info = get_result_info(result_id)
            if not result_info:
                print(f"Aucune information trouvée pour le résultat avec l'ID {result_id}")
                return

            # Utiliser les valeurs actuelles ou les nouvelles si elles sont fournies
            current_pseudo = result_info['current_pseudo'] if new_pseudo is None else new_pseudo
            current_game = result_info['current_game'] if new_game is None else new_game

            # Récupérer l'ID du nouvel utilisateur ou l'ajouter s'il n'existe pas
            user_id = get_user_id(current_pseudo)

            if user_id is None:
                print(f"L'utilisateur '{current_pseudo}' n'existe pas.")
                return

            # Récupérer l'ID du nouvel exercice ou l'ajouter s'il n'existe pas
            exercise_id = get_exercise_id(current_game)

            if exercise_id is None:
                print(f"L'exercice '{current_game}' n'existe pas.")
                return

            # Construire la requête SQL pour la mise à jour
            query = """
                UPDATE results
                SET hours = %s, number_try = %s, number_ok = %s, Users_id = %s, exercices_id = %s
                WHERE id = %s
            """

            # Exécuter la requête avec les nouveaux paramètres
            cursor.execute(query, (new_hours, new_number_try, new_number_ok, user_id, exercise_id, result_id))
            connection.commit()

            print("Résultat mis à jour avec succès.")

    except Error as e:
        print(f"Erreur lors de la mise à jour du résultat : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")


# La fonction récupère les informations détaillées d'un résultat spécifié avec l'ID donné
def get_result_info(result_id):
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor(dictionary=True)

            # Récupérer les informations du résultat avec l'ID spécifié
            cursor.execute(f"""
                SELECT results.id, results.hours, results.number_try, results.number_ok, Users.nickname AS current_pseudo, exercices.exercice_code AS current_game
                FROM results
                INNER JOIN Users ON results.Users_id = Users.id
                INNER JOIN exercices ON results.exercices_id = exercices.id
                WHERE results.id = {result_id}
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


# La fonction récupère tous les codes d'exercice distincts disponibles dans la base de données.
def get_all_games():
    try:
        connection = connect()
        if connection:
            cursor = connection.cursor()

            # Récupérer tous les jeux
            cursor.execute("SELECT DISTINCT exercice_code FROM exercices")
            games = cursor.fetchall()

            if games:
                return [game[0] for game in games]
            else:
                print("Aucun jeu trouvé dans la base de données.")
                return []

    except Error as e:
        print(f"Erreur lors de la récupération des jeux : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion à la base de données fermée")
