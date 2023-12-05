""" Ethan Martin
    Projet DBPY
    le 05.12.23"""


# menu.py

import tkinter as tk
from tkinter import ttk
import geo01
import info02
import info05
import datetime
import database

# Exercises array
a_exercise = ["geo01", "info02", "info05"]
albl_image = [None, None, None]  # Label (with images) array
a_image = [None, None, None]  # Images array
a_title = [None, None, None]  # Array of title (ex: GEO01)

dict_games = {"geo01": geo01.open_window_geo_01, "info02": info02.open_window_info_02,
              "info05": info05.open_window_info_05}


# Call other windows (exercises)
def exercise(event, exer):
    dict_games[exer](window)


# Call display_results
def display_result(event):
    # Créer une nouvelle fenêtre pour afficher les résultats
    result_window = tk.Toplevel(window)
    result_window.title("Résultats")
    result_window.geometry("1500x500")

    # Frame for filters
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

    lbl_filter_start_date = tk.Label(filter_frame, text="Date de début:", font=("Arial", 12))
    lbl_filter_start_date.grid(row=0, column=4, padx=5, pady=5)
    filter_start_date = tk.Entry(filter_frame, font=("Arial", 12))
    filter_start_date.grid(row=0, column=5, padx=5, pady=5)

    lbl_filter_end_date = tk.Label(filter_frame, text="Date de fin:", font=("Arial", 12))
    lbl_filter_end_date.grid(row=0, column=6, padx=5, pady=5)
    filter_end_date = tk.Entry(filter_frame, font=("Arial", 12))
    filter_end_date.grid(row=0, column=7, padx=5, pady=5)

    # Function to apply filters
    def apply_filters():
        # Récupérer les résultats avec les filtres
        exercise_filter = filter_exercise.get()
        nickname_filter = filter_nickname.get()
        start_date_filter = filter_start_date.get()
        end_date_filter = filter_end_date.get()

        # Vous devrez adapter la logique de filtrage selon vos besoins
        filtered_results = database.get_filtered_results(exercise_filter, nickname_filter, start_date_filter, end_date_filter)

        # Effacer les anciens résultats affichés
        for widget in result_window.winfo_children():
            if widget not in [filter_frame]:
                widget.destroy()

        # Créer des étiquettes pour les champs
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

        # Afficher les résultats filtrés
        for idx, result in enumerate(filtered_results, start=1):
            tk.Label(labels_frame, text=result['exercise_code']).grid(row=idx, column=0, padx=10, pady=5)
            tk.Label(labels_frame, text=result['nickname']).grid(row=idx, column=1, padx=10, pady=5)
            tk.Label(labels_frame, text=result['hours']).grid(row=idx, column=2, padx=10, pady=5)
            tk.Label(labels_frame, text=result['date_time']).grid(row=idx, column=3, padx=10, pady=5)
            tk.Label(labels_frame, text=result['number_try']).grid(row=idx, column=4, padx=10, pady=5)
            tk.Label(labels_frame, text=result['number_ok']).grid(row=idx, column=5, padx=10, pady=5)

    # Bouton pour appliquer les filtres
    btn_apply_filters = tk.Button(filter_frame, text="Appliquer les filtres", font=("Arial", 12), command=apply_filters)
    btn_apply_filters.grid(row=0, column=8, padx=10, pady=5)

    # Afficher tous les résultats à l'ouverture de la fenêtre
    apply_filters()



# Main window
window = tk.Tk()
window.title("Entraînement cérébral")
window.geometry("1100x900")

# Color definition
rgb_color = (139, 201, 194)
hex_color = '#%02x%02x%02x' % rgb_color  # Translation in hexa
window.configure(bg=hex_color)
window.grid_columnconfigure((0, 1, 2), minsize=300, weight=1)

# Title creation
lbl_title = tk.Label(window, text="MENU D'ENTRAÎNEMENT", font=("Arial", 15))
lbl_title.grid(row=0, column=1, ipady=5, padx=40, pady=40)

# Labels creation and positioning
for ex in range(len(a_exercise)):
    a_title[ex] = tk.Label(window, text=a_exercise[ex], font=("Arial", 15))
    a_title[ex].grid(row=1 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)  # 3 labels per row

    a_image[ex] = tk.PhotoImage(file="img/" + a_exercise[ex] + ".gif")  # Image name
    albl_image[ex] = tk.Label(window, image=a_image[ex])  # Put image on label
    albl_image[ex].grid(row=2 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)  # 3 labels per row
    albl_image[ex].bind("<Button-1>",
                        lambda event, ex=ex: exercise(event=None, exer=a_exercise[ex]))  # Link to others .py

# Buttons, display results & quit
btn_display = tk.Button(window, text="Afficher les résultats", font=("Arial", 15))
btn_display.grid(row=1 + 2 * len(a_exercise) // 3, column=1)
btn_display.bind("<Button-1>", display_result)

btn_finish = tk.Button(window, text="Quitter", font=("Arial", 15))
btn_finish.grid(row=2 + 2 * len(a_exercise) // 3, column=1)
btn_finish.bind("<Button-1>", quit)

# Main loop
window.mainloop()

