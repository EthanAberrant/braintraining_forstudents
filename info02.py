""" Ethan Martin
    Projet DBPY
    le 15.12.23"""

# Training (INFO02)

import tkinter as tk
import random
import time
import datetime
import database

pseudo = ""  # Pseudo provisoire pour l'utilisateur
exercise = "INFO02"
nbtrials = 0  # Nombre total d'essais
nbsuccess = 0  # Nombre d'essais réussis

# Liaison entre le canevas et le code
unite = ["B", "kB", "MB", "GB", "TB"]
n1 = 0  # Valeur à convertir
u1 = unite[0]
n2 = 0  # Valeur à convertir
u2 = unite[0]
rapport = 0


def next(event):
    global n1, u1, u2, rapport
    window_info02.configure(bg=hex_color)

    n1 = round(random.random(), 3)
    dec = random.randint(0, 3)
    for i in range(dec):
        n1 *= 10
    n1 = round(n1, 3)
    p1 = random.randint(1, 4)
    u1 = unite[p1]
    p2 = p1
    while p1 == p2:
        p2 = random.randint(0, 4)
    u2 = unite[p2]
    rapport = pow(10, 3 * (p2 - p1))
    label_n1.configure(text=f" {n1} {u1} =")
    label_u2.configure(text=f" {u2} ")
    entry_n2.delete(0, 'end')


def save_game():
    global pseudo, nbtrials, nbsuccess
    # Obtenir le pseudo saisi
    pseudo = entry_pseudo.get()

    # Calcul de la durée
    end_date = datetime.datetime.now()
    duration = end_date - start_date
    duration_str = "{:02d}:{:02d}".format(int(duration.total_seconds() / 60), int(duration.total_seconds() % 60))

    # Enregistrer les résultats dans la base de données
    database.save_result("info02", pseudo, start_date, duration_str, nbtrials, nbsuccess)

    # Réinitialiser les variables pour le prochain exercice
    pseudo = ""
    nbtrials = 0
    nbsuccess = 0

    # Mettre à jour le texte de l'étiquette avec le nouveau pseudo
    lbl_result.configure(text=f"{pseudo} Essais réussis : {nbsuccess} / {nbtrials}")


def test():
    global n2, nbsuccess, nbtrials
    # Fonction pour tester si la valeur est correcte
    n2 = float(entry_n2.get().replace(" ", ""))
    nbtrials += 1
    success = (abs(n1 / n2 / rapport - 1) < 0.01)  # Tolérance 1%
    if success:
        nbsuccess += 1
        window_info02.configure(bg="green")
    else:
        window_info02.configure(bg="red")
    lbl_result.configure(text=f"{pseudo} Essais réussis : {nbsuccess} / {nbtrials}")
    window_info02.update()
    time.sleep(1)  # Délai 1s
    next(event=None)


def display_timer():
    duration = datetime.datetime.now() - start_date  # Temps écoulé depuis le début, en temps avec décimales
    duration_s = int(duration.total_seconds())  # Idem mais en secondes (entier)
    # Affichage min:sec (00:13)
    lbl_duration.configure(text="{:02d}".format(int(duration_s / 60)) + ":" + "{:02d}".format(duration_s % 60))
    window_info02.after(1000, display_timer)  # Recommencer après 15 ms


def open_window_info_02(window):
    global window_info02, lbl_duration, lbl_result, entry_pseudo, hex_color, start_date, label_n1, label_u2, entry_n2

    window_info02 = tk.Toplevel(window)
    window_info02.title("Conversion d'unités")
    window_info02.geometry("1100x900")
    window_info02.grid_columnconfigure((0, 1, 2), minsize=150, weight=1)

    # Définition de la couleur
    rgb_color = (139, 201, 194)
    hex_color = '#%02x%02x%02x' % rgb_color  # Traduction en hexa
    window_info02.configure(bg=hex_color)

    lbl_title = tk.Label(window_info02, text=f"{exercise}", font=("Arial", 15))
    lbl_title.grid(row=0, column=0, columnspan=3, ipady=5, padx=20, pady=20)

    lbl_duration = tk.Label(window_info02, text="0:00", font=("Arial", 15))
    lbl_duration.grid(row=0, column=2, ipady=5, padx=10, pady=10)

    tk.Label(window_info02, text='Pseudo:', font=("Arial", 15)).grid(row=1, column=0, padx=5, pady=5)
    entry_pseudo = tk.Entry(window_info02, font=("Arial", 15))
    entry_pseudo.grid(row=1, column=1)

    lbl_result = tk.Label(window_info02, text=f"{pseudo} Essais réussis : 0/0", font=("Arial", 15))
    lbl_result.grid(row=1, column=2, columnspan=3, ipady=5, padx=20, pady=20)

    label_n1 = tk.Label(window_info02, text="n1:", font=("Arial", 15))
    label_n1.grid(row=2, column=0, ipady=5, padx=20, pady=20, sticky='E')

    entry_n2 = tk.Entry(window_info02, font=("Arial", 15))
    entry_n2.grid(row=2, column=1, ipady=5, padx=5, pady=20, sticky='E')

    label_u2 = tk.Label(window_info02, text="u2:", font=("Arial", 15))
    label_u2.grid(row=2, column=2, ipady=5, padx=5, pady=20, sticky='W')

    btn_next = tk.Button(window_info02, text="Suivant", font=("Arial", 15), command=test)
    btn_next.grid(row=3, column=0, columnspan=3, ipady=5, padx=5, pady=5)

    btn_finish = tk.Button(window_info02, text="Terminer", font=("Arial", 15), command=save_game)
    btn_finish.grid(row=6, column=0, columnspan=6)

    start_date = datetime.datetime.now()
    display_timer()
    # Premier appel de next_point
    next(event=None)

    # Liaison des actions (entrée & boutons)
    entry_n2.bind("<Return>", lambda e: test())
    # Boucle principale
    window_info02.mainloop()