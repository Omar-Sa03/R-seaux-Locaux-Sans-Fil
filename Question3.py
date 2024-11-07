import math
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

def calculer_distance(rssi, rssi_reference, n=3):
    return 10 ** ((rssi_reference - rssi) / (10 * n))
def triangulation(p1, p2, p3, d1, d2, d3):

    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    A = 2*x2 - 2*x1
    B = 2*y2 - 2*y1
    C = d1**2 - d2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2*x3 - 2*x2
    E = 2*y3 - 2*y2
    F = d2**2 - d3**2 - x2**2 + x3**2 - y2**2 + y3**2

    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)
    return (x, y)

def afficher_resultats():
    p1 = (2, 3)
    p2 = (8, 10)
    p3 = (5, 1)

    rssi_reference = -30
    rssi1, rssi2, rssi3 = -50, -50, -52
    d1 = calculer_distance(rssi1, rssi_reference)
    d2 = calculer_distance(rssi2, rssi_reference)
    d3 = calculer_distance(rssi3, rssi_reference)

    position_mobile = triangulation(p1, p2, p3, d1, d2, d3)

    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')

    ax.plot(p1[0], p1[1], 'bo', label="Point d'accès 1")
    ax.plot(p2[0], p2[1], 'go', label="Point d'accès 2")
    ax.plot(p3[0], p3[1], 'ro', label="Point d'accès 3")

    circle1 = plt.Circle(p1, d1, color='b', fill=False, linestyle='--')
    circle2 = plt.Circle(p2, d2, color='g', fill=False, linestyle='--')
    circle3 = plt.Circle(p3, d3, color='r', fill=False, linestyle='--')
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.add_patch(circle3)

    ax.plot(position_mobile[0], position_mobile[1], 'kx', label="Position estimée du mobile")

    plt.legend(loc="upper left")

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Triangulation de la position du mobile")
    plt.grid(True)
    plt.show()

    messagebox.showinfo("Résultat", f"Position estimée du mobile : {position_mobile}")

root = tk.Tk()
root.title("Estimation de Position avec Triangulation")

title_label = tk.Label(root, text="Estimation de la Position d'un Mobile", font=("Arial", 12))
title_label.pack(pady=10)

calcul_button = tk.Button(root, text="Calculer la position", command=afficher_resultats, font=("Arial", 12))
calcul_button.pack(pady=20)

root.mainloop()
