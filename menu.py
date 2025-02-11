"""Ethan Martin
Projet_DBPY
Le 15.12.23"""

# menu.py
import tkinter as tk
from tkinter import ttk, StringVar
from tkinter.ttk import Combobox, Entry
from tkinter import messagebox
import bcrypt
import hashlib
import datetime
import database
import geo01
import info02
import info05

# Definition of available exercises
a_exercise = ["geo01", "info02", "info05"]
albl_image = [None, None, None]
a_image = [None, None, None]
a_title = [None, None, None]

# Dictionary of games with their associated function
dict_games = {"geo01": geo01.open_window_geo_01, "info02": info02.open_window_info_02,
              "info05": info05.open_window_info_05}


# Function to start an exercise based on the event
def exercise(event, exer):
    dict_games[exer](window)


# Function to display filtered results
def display_result(event=None):
    result_window = tk.Toplevel(window)
    result_window.title("Résultats")
    result_window.geometry("1500x500")

    filter_frame = tk.Frame(result_window)
    filter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    lbl_filter_exercise = tk.Label(filter_frame, text="Exercice:", font=("Arial", 12))
    lbl_filter_exercise.grid(row=0, column=0, padx=5, pady=5)
    filter_exercise = tk.Entry(filter_frame, font=("Arial", 12))
    filter_exercise.grid(row=0, column=1, padx=5, pady=5)

    lbl_filter_nickname = tk.Label(filter_frame, text="Pseudo:", font=("Arial", 12))
    lbl_filter_nickname.grid(row=0, column=2, padx=5, pady=5)
    filter_nickname = tk.Entry(filter_frame, font=("Arial", 12))
    filter_nickname.grid(row=0, column=3, padx=5, pady=5)

    lbl_filter_start_date = tk.Label(filter_frame, text="Date :", font=("Arial", 12))
    lbl_filter_start_date.grid(row=0, column=4, padx=5, pady=5)
    filter_start_date = tk.Entry(filter_frame, font=("Arial", 12))
    filter_start_date.grid(row=0, column=5, padx=5, pady=5)

    def apply_filters():
        exercise_filter = filter_exercise.get()
        nickname_filter = filter_nickname.get()
        start_date_filter = filter_start_date.get()
        filtered_results = database.get_filtered_results(exercise_filter, nickname_filter, start_date_filter)

        for widget in result_window.winfo_children():
            if widget not in [filter_frame]:
                widget.destroy()

        labels_frame = tk.Frame(result_window)
        labels_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        lbl_game = tk.Label(labels_frame, text="Jeu", font=("Arial", 12, "bold"))
        lbl_nickname = tk.Label(labels_frame, text="Pseudo", font=("Arial", 12, "bold"))
        lbl_hours = tk.Label(labels_frame, text="Temps", font=("Arial", 12, "bold"))
        lbl_date_time = tk.Label(labels_frame, text="Date et Heure", font=("Arial", 12, "bold"))
        lbl_number_try = tk.Label(labels_frame, text="Nombre d'essai", font=("Arial", 12, "bold"))
        lbl_number_ok = tk.Label(labels_frame, text="Nombre d'essai réussi", font=("Arial", 12, "bold"))

        lbl_game.grid(row=0, column=0, padx=10, pady=5)
        lbl_nickname.grid(row=0, column=1, padx=10, pady=5)
        lbl_hours.grid(row=0, column=2, padx=10, pady=5)
        lbl_date_time.grid(row=0, column=3, padx=10, pady=5)
        lbl_number_try.grid(row=0, column=4, padx=10, pady=5)
        lbl_number_ok.grid(row=0, column=5, padx=10, pady=5)

        for idx, result in enumerate(filtered_results, start=1):
            tk.Label(labels_frame, text=result['exercise_code']).grid(row=idx, column=0, padx=10, pady=5)
            tk.Label(labels_frame, text=result['nickname']).grid(row=idx, column=1, padx=10, pady=5)
            tk.Label(labels_frame, text=result['hours']).grid(row=idx, column=2, padx=10, pady=5)
            tk.Label(labels_frame, text=result['date_time']).grid(row=idx, column=3, padx=10, pady=5)
            tk.Label(labels_frame, text=result['number_try']).grid(row=idx, column=4, padx=10, pady=5)
            tk.Label(labels_frame, text=result['number_ok']).grid(row=idx, column=5, padx=10, pady=5)

            # Boutons de modification et suppression
            btn_modify = tk.Button(labels_frame, text="Modifier", font=("Arial", 12),
                                   command=lambda result=result: modify_result(result['id'],
                                                                               result['hours'],
                                                                               result['number_try'],
                                                                               result['number_ok'],
                                                                               result['nickname']))
            btn_modify.grid(row=idx, column=6, padx=5, pady=5)

            btn_delete = tk.Button(labels_frame, text="Supprimer", font=("Arial", 12),
                                   command=lambda result=result: delete_result(result['id']))
            btn_delete.grid(row=idx, column=7, padx=5, pady=5)

    btn_apply_filters = tk.Button(filter_frame, text="Appliquer les filtres", font=("Arial", 12), command=apply_filters)
    btn_apply_filters.grid(row=0, column=6, padx=10, pady=5)

    apply_filters()

    btn_add_result = tk.Button(result_window, text="Ajouter un résultat", font=("Arial", 12), command=add_result)
    btn_add_result.grid(row=0, column=7, padx=10, pady=5)


# Function to delete a result
def delete_result(result_id):
    database.delete_result(result_id)
    display_result()


# Function to modify a result
def modify_result(result_id, current_hours, current_number_try, current_number_ok, current_pseudo):
    result_info = database.get_result_info(result_id)
    if not result_info:
        print(f"Aucune information trouvée pour le résultat avec l'ID {result_id}")
        return

    current_game = result_info['current_game']

    modify_window = tk.Toplevel(window)
    modify_window.title("Modifier le résultat")
    modify_window.geometry("500x220")

    lbl_modify_hours = tk.Label(modify_window, text="Nouveau temps:", font=("Arial", 12))
    lbl_modify_hours.grid(row=0, column=0, padx=5, pady=5)
    entry_modify_hours = tk.Entry(modify_window, font=("Arial", 12))
    entry_modify_hours.grid(row=0, column=1, padx=5, pady=5)
    entry_modify_hours.insert(0, current_hours)

    # Champ d'entrée pour choisir le pseudo
    lbl_choose_pseudo = tk.Label(modify_window, text="Choisir le pseudo:", font=("Arial", 12))
    lbl_choose_pseudo.grid(row=3, column=0, padx=5, pady=5)
    entry_choose_pseudo = tk.Entry(modify_window, font=("Arial", 12))
    entry_choose_pseudo.grid(row=3, column=1, padx=5, pady=5)
    entry_choose_pseudo.insert(0, current_pseudo)

    # Combobox pour choisir le jeu
    lbl_choose_game = tk.Label(modify_window, text="Choisir le jeu:", font=("Arial", 12))
    lbl_choose_game.grid(row=4, column=0, padx=5, pady=5)
    combo_choose_game = ttk.Combobox(modify_window, values=database.get_all_games(), font=("Arial", 12))
    combo_choose_game.grid(row=4, column=1, padx=5, pady=5)
    combo_choose_game.set(current_game)

    lbl_modify_number_try = tk.Label(modify_window, text="Nouveau nombre d'essais:", font=("Arial", 12))
    lbl_modify_number_try.grid(row=1, column=0, padx=5, pady=5)
    entry_modify_number_try = tk.Entry(modify_window, font=("Arial", 12))
    entry_modify_number_try.grid(row=1, column=1, padx=5, pady=5)
    entry_modify_number_try.insert(0, current_number_try)

    lbl_modify_number_ok = tk.Label(modify_window, text="Nouveau nombre d'essais réussis:", font=("Arial", 12))
    lbl_modify_number_ok.grid(row=2, column=0, padx=5, pady=5)
    entry_modify_number_ok = tk.Entry(modify_window, font=("Arial", 12))
    entry_modify_number_ok.grid(row=2, column=1, padx=5, pady=5)
    entry_modify_number_ok.insert(0, current_number_ok)

    btn_modify_result = tk.Button(modify_window, text="Modifier le résultat", font=("Arial", 12),
                                  command=lambda: update_result(result_id,
                                                                entry_modify_hours.get(),
                                                                entry_modify_number_try.get(),
                                                                entry_modify_number_ok.get(),
                                                                entry_choose_pseudo.get(),
                                                                combo_choose_game.get()))
    btn_modify_result.grid(row=5, column=0, columnspan=2, pady=10)


# Function to update a modified result
def update_result(result_id, new_hours, new_number_try, new_number_ok, new_pseudo, new_game):
    database.update_result(result_id, new_hours, new_number_try, new_number_ok, new_pseudo, new_game)


# Function to manually add a result
def add_result():
    result_window = tk.Toplevel(window)
    result_window.title("Ajouter un résultat")
    result_window.geometry("400x220")

    lbl_add_pseudo = tk.Label(result_window, text="Pseudo:", font=("Arial", 12))
    lbl_add_pseudo.grid(row=0, column=0, padx=5, pady=5)

    # Utilisation d'un champ d'entrée pour le pseudo
    entry_pseudo = tk.Entry(result_window, font=("Arial", 12))
    entry_pseudo.grid(row=0, column=1, padx=5, pady=5)

    lbl_add_hours = tk.Label(result_window, text="Temps:", font=("Arial", 12))
    lbl_add_hours.grid(row=1, column=0, padx=5, pady=5)
    entry_add_hours = tk.Entry(result_window, font=("Arial", 12))
    entry_add_hours.grid(row=1, column=1, padx=5, pady=5)

    lbl_add_number_try = tk.Label(result_window, text="Nombre d'essais:", font=("Arial", 12))
    lbl_add_number_try.grid(row=2, column=0, padx=5, pady=5)
    entry_add_number_try = tk.Entry(result_window, font=("Arial", 12))
    entry_add_number_try.grid(row=2, column=1, padx=5, pady=5)

    lbl_add_number_ok = tk.Label(result_window, text="Nombre d'essais réussis:", font=("Arial", 12))
    lbl_add_number_ok.grid(row=3, column=0, padx=5, pady=5)
    entry_add_number_ok = tk.Entry(result_window, font=("Arial", 12))
    entry_add_number_ok.grid(row=3, column=1, padx=5, pady=5)

    # Ajout de la combobox pour le jeu
    lbl_add_game = tk.Label(result_window, text="Jeu:", font=("Arial", 12))
    lbl_add_game.grid(row=4, column=0, padx=5, pady=5)
    game_options = ["GEO01", "INFO02", "INFO05"]  # Remplacez par vos données réelles
    selected_game = StringVar()
    combo_game = Combobox(result_window, textvariable=selected_game, values=game_options)
    combo_game.grid(row=4, column=1, padx=5, pady=5)

    btn_add_result = tk.Button(result_window, text="Ajouter le résultat", font=("Arial", 12),
                               command=lambda: save_new_result(selected_game.get(),
                                                               entry_pseudo.get(),
                                                               entry_add_hours.get(),
                                                               entry_add_number_try.get(),
                                                               entry_add_number_ok.get()))
    btn_add_result.grid(row=5, column=0, columnspan=2, pady=10)


# Function to save a new result
def save_new_result(exercise_code, user_pseudo, hours, number_try, number_ok):
    # Obtenez l'ID de l'utilisateur
    user_id = database.get_user_id(user_pseudo)

    # Obtenez l'ID de l'exercice
    exercise_id = database.get_exercise_id(exercise_code)

    # Obtenez la date actuelle
    start_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Enregistrez le résultat avec les informations obtenues
    database.save_result(exercise_code, user_pseudo, start_date, hours, number_try, number_ok)

    # Affichez le résultat mis à jour
    display_result()


# Function to quit the application
def quit(event):
    window.destroy()


# Variables to track authentication state
user_authenticated = False


# Function to show the registration window
def show_register_window():
    register_window = tk.Toplevel()
    register_window.title("Inscription")
    register_window.geometry("400x200")

    lbl_username = tk.Label(register_window, text="Nom d'utilisateur:", font=("Arial", 12))
    lbl_username.grid(row=0, column=0, padx=5, pady=5)
    entry_username = Entry(register_window, font=("Arial", 12))
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    lbl_password = tk.Label(register_window, text="Mot de passe:", font=("Arial", 12))
    lbl_password.grid(row=1, column=0, padx=5, pady=5)
    entry_password = Entry(register_window, show="*", font=("Arial", 12))
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    lbl_confirm_password = tk.Label(register_window, text="Confirmer le mot de passe:", font=("Arial", 12))
    lbl_confirm_password.grid(row=2, column=0, padx=5, pady=5)
    entry_confirm_password = Entry(register_window, show="*", font=("Arial", 12))
    entry_confirm_password.grid(row=2, column=1, padx=5, pady=5)

    # Function to register a new user
    def register_user():
        username = entry_username.get()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()

        if password == confirm_password:
            # Utilisation de bcrypt pour hacher le mot de passe avant l'enregistrement dans la base de données
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Enregistrement de l'utilisateur dans la base de données avec le mot de passe haché
            database.register_user(username, hashed_password)

            # Après l'enregistrement, fermez la fenêtre d'enregistrement
            register_window.destroy()
            # Montrez la fenêtre de connexion
            show_login_window()
        else:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")

    # Function to show the login window from the registration window
    def show_login_window_from_register():
        # Fermez la fenêtre d'enregistrement et affichez la fenêtre de connexion
        register_window.destroy()
        show_login_window()

    # Button to login
    btn_login_direct = tk.Button(register_window, text="Déjà un compte? Se connecter", font=("Arial", 12),
                                 command=show_login_window_from_register)
    btn_login_direct.grid(row=3, column=0, columnspan=2, pady=10)

    btn_register = tk.Button(register_window, text="S'inscrire", font=("Arial", 12), command=register_user)
    btn_register.grid(row=4, column=0, columnspan=2, pady=10)


# Function to show the login window
def show_login_window():
    login_window = tk.Toplevel()
    login_window.title("Connexion")
    login_window.geometry("400x150")

    lbl_username = tk.Label(login_window, text="Nom d'utilisateur:", font=("Arial", 12))
    lbl_username.grid(row=0, column=0, padx=5, pady=5)
    entry_username = Entry(login_window, font=("Arial", 12))
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    lbl_password = tk.Label(login_window, text="Mot de passe:", font=("Arial", 12))
    lbl_password.grid(row=1, column=0, padx=5, pady=5)
    entry_password = Entry(login_window, show="*", font=("Arial", 12))
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    # Function to authenticate the user
    def authenticate_user_interface():
        global user_authenticated
        username = entry_username.get()
        password = entry_password.get()

        # Vérifiez l'authentification de l'utilisateur avec la base de données
        if database.authenticate_user(username, password):
            login_window.destroy()
            user_authenticated = True
            # Montrez la fenêtre principale du jeu
            window.deiconify()
        else:
            messagebox.showerror("Erreur", "Authentification échouée. Veuillez vérifier vos informations.")

    btn_login = tk.Button(login_window, text="Se connecter", font=("Arial", 12), command=authenticate_user_interface)
    btn_login.grid(row=2, column=0, columnspan=2, pady=10)


# Main function of the application
window = tk.Tk()
window.title("Entraînement cérébral")
window.geometry("1100x900")

rgb_color = (139, 201, 194)
hex_color = '#%02x%02x%02x' % rgb_color
window.configure(bg=hex_color)
window.grid_columnconfigure((0, 1, 2), minsize=300, weight=1)

lbl_title = tk.Label(window, text="MENU D'ENTRAÎNEMENT", font=("Arial", 15))
lbl_title.grid(row=0, column=1, ipady=5, padx=40, pady=40)

for ex in range(len(a_exercise)):
    a_title[ex] = tk.Label(window, text=a_exercise[ex], font=("Arial", 15))
    a_title[ex].grid(row=1 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)

    a_image[ex] = tk.PhotoImage(file="img/" + a_exercise[ex] + ".gif")
    albl_image[ex] = tk.Label(window, image=a_image[ex])
    albl_image[ex].grid(row=2 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)
    albl_image[ex].bind("<Button-1>", lambda event, ex=ex: exercise(event=None, exer=a_exercise[ex]))

btn_display = tk.Button(window, text="Afficher les résultats", font=("Arial", 15), command=display_result)
btn_display.grid(row=1 + 2 * len(a_exercise) // 3, column=1)

btn_finish = tk.Button(window, text="Quitter", font=("Arial", 15), command=lambda: quit(None))
btn_finish.grid(row=2 + 2 * len(a_exercise) // 3, column=1)

# Cacher la fenêtre principale jusqu'à ce que l'utilisateur soit connecté
window.withdraw()

# Afficher d'abord la fenêtre d'enregistrement
show_register_window()

window.mainloop()