 # menu.py

import tkinter as tk
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

dict_games = {"geo01": geo01.open_window_geo_01, "info02": info02.open_window_info_02, "info05": info05.open_window_info_05}

# Call other windows (exercises)
def exercise(event, exer):
    dict_games[exer](window)

# Call display_results
def display_result(event):
    # Récupérer tous les résultats avec les informations de l'exercice
    all_results = database.get_all_results_with_exercise()

    # Créer une nouvelle fenêtre pour afficher les résultats
    result_window = tk.Toplevel(window)
    result_window.title("Results")
    result_window.geometry("800x400")

    # Créer des étiquettes pour les champs
    lbl_game = tk.Label(result_window, text="Game", font=("Arial", 12, "bold"))
    lbl_nickname = tk.Label(result_window, text="Nickname", font=("Arial", 12, "bold"))
    lbl_hours = tk.Label(result_window, text="Hours", font=("Arial", 12, "bold"))
    lbl_date_time = tk.Label(result_window, text="Date & Time", font=("Arial", 12, "bold"))
    lbl_number_try = tk.Label(result_window, text="Number of Tries", font=("Arial", 12, "bold"))
    lbl_number_ok = tk.Label(result_window, text="Number OK", font=("Arial", 12, "bold"))

    # Positionner les étiquettes dans la fenêtre
    lbl_game.grid(row=0, column=0, padx=10, pady=5)
    lbl_nickname.grid(row=0, column=1, padx=10, pady=5)
    lbl_hours.grid(row=0, column=2, padx=10, pady=5)
    lbl_date_time.grid(row=0, column=3, padx=10, pady=5)
    lbl_number_try.grid(row=0, column=4, padx=10, pady=5)
    lbl_number_ok.grid(row=0, column=5, padx=10, pady=5)

    # Afficher les résultats dans la fenêtre
    for idx, result in enumerate(all_results, start=1):
        tk.Label(result_window, text=result['exercise_code']).grid(row=idx, column=0, padx=10, pady=5)
        tk.Label(result_window, text=result['nickname']).grid(row=idx, column=1, padx=10, pady=5)
        tk.Label(result_window, text=result['hours']).grid(row=idx, column=2, padx=10, pady=5)
        tk.Label(result_window, text=result['date_time']).grid(row=idx, column=3, padx=10, pady=5)
        tk.Label(result_window, text=result['number_try']).grid(row=idx, column=4, padx=10, pady=5)
        tk.Label(result_window, text=result['number_ok']).grid(row=idx, column=5, padx=10, pady=5)

# Main window
window = tk.Tk()
window.title("Training, entrainement cérébral")
window.geometry("1100x900")

# Color definition
rgb_color = (139, 201, 194)
hex_color = '#%02x%02x%02x' % rgb_color  # Translation in hexa
window.configure(bg=hex_color)
window.grid_columnconfigure((0, 1, 2), minsize=300, weight=1)

# Title creation
lbl_title = tk.Label(window, text="TRAINING MENU", font=("Arial", 15))
lbl_title.grid(row=0, column=1, ipady=5, padx=40, pady=40)

# Labels creation and positioning
for ex in range(len(a_exercise)):
    a_title[ex] = tk.Label(window, text=a_exercise[ex], font=("Arial", 15))
    a_title[ex].grid(row=1 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)  # 3 labels per row

    a_image[ex] = tk.PhotoImage(file="img/" + a_exercise[ex] + ".gif")  # Image name
    albl_image[ex] = tk.Label(window, image=a_image[ex])  # Put image on label
    albl_image[ex].grid(row=2 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)  # 3 labels per row
    albl_image[ex].bind("<Button-1>", lambda event, ex=ex: exercise(event=None, exer=a_exercise[ex]))  # Link to others .py
    print(a_exercise[ex])

# Buttons, display results & quit
btn_display = tk.Button(window, text="Display results", font=("Arial", 15))
btn_display.grid(row=1 + 2 * len(a_exercise) // 3, column=1)
btn_display.bind("<Button-1>", display_result)

btn_finish = tk.Button(window, text="Quitter", font=("Arial", 15))
btn_finish.grid(row=2 + 2 * len(a_exercise) // 3, column=1)
btn_finish.bind("<Button-1>", quit)

# Main loop
window.mainloop()