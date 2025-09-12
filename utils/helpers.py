## Funciones auxiliares y utilidades del sistema

import tkinter as tk
from datetime import datetime
import pandas as pd
from config.settings import *

def generar_id(prefijo):
    return f"{prefijo}{datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}"

def boton_grande(parent, texto, color, comando, icono=""):
    btn_text = f"{icono} {texto}" if icono else texto
    btn = tk.Button(parent, text=btn_text, command=comando, bg=color, fg="white",
                   font=("Arial", 12, "bold"), relief="flat", bd=0, 
                   padx=20, pady=10, cursor="hand2")
    
    # Efectos hover
    darker = f"#{max(0, int(color[1:3], 16) - 20):02x}{max(0, int(color[3:5], 16) - 20):02x}{max(0, int(color[5:7], 16) - 20):02x}"
    btn.bind("<Enter>", lambda e: btn.config(bg=darker))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    
    return btn

def cargar_categorias():
    try:
        return pd.read_excel(CATEGORIAS_FILE)["Nombre"].tolist()
    except:
        return ["Carnes", "Lacteos", "Bebidas", "Snacks", "Limpieza"]

def formatear_precio(precio):
    try:
        return f"S/ {float(precio):.2f}"
    except:
        return "S/ 0.00"

def validar_numero(valor, tipo="float"):
    try:
        return (int(valor), True) if tipo == "int" else (float(valor), True)
    except:
        return 0, False
