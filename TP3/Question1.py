import math
import subprocess
import re
import tkinter as tk
from tkinter import messagebox

def Get_RSSI():
    try:
        process = subprocess.Popen("netsh wlan show interfaces", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        stdout = stdout.decode("utf-8")

        rssi_match = re.search(r"Signal\s*:\s*(\d+)%", stdout)
        if rssi_match:
            signal_percent = int(rssi_match.group(1))
            rssi_dbm = (signal_percent / 2) - 100
            return rssi_dbm
        else:
            messagebox.showerror("Erreur", "RSSI non trouvé. Vérifiez la connexion réseau.")
            return None
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'exécution : {e}")
        return None

def calculer_distance(rssi, rssi_reference, n=3):
    distance = 10 ** ((rssi_reference - rssi) / (10 * n))
    return distance

def afficher_resultats():
    rssi = Get_RSSI()
    rssi_label_var.set(f"{rssi:.2f} dBm")
    # Valeur de référence de RSSI à 1 mètre
    rssi_reference = -40  
    distance = calculer_distance(rssi, rssi_reference)
    distance_label_var.set(f"{distance:.2f} mètres")


root = tk.Tk()
root.title("Estimation de la Distance WiFi")
root.geometry("300x200")

# Variables pour afficher les résultats
rssi_label_var = tk.StringVar()
distance_label_var = tk.StringVar()

# Interface
tk.Label(root, text="RSSI (dBm):").pack(pady=5)
tk.Label(root, textvariable=rssi_label_var).pack()

tk.Label(root, text="Distance estimée (mètres):").pack(pady=5)
tk.Label(root, textvariable=distance_label_var).pack()

# Bouton pour calculer
tk.Button(root, text="Obtenir RSSI et Distance", command=afficher_resultats).pack(pady=20)

# Exécution de la fenêtre principale
root.mainloop()
