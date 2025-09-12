## Dashboard principal del sistema

import tkinter as tk
from tkinter import messagebox
from config.settings import *
from utils.helpers import boton_grande

class Dashboard(tk.Tk):
    
    def __init__(self, usuario):
        super().__init__()
        self.usuario = usuario
        self.title(f"{APP_NAME} - Usuario: {usuario}")
        self.geometry("1200x700")
        self.config(bg="white")
        self.center_window()
        
        self.main_frame = None
        self._crear_interfaz()
        self.mostrar_inventario()  # Mostrar inventario por defecto
    
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    def _crear_interfaz(self):
        # Barra superior
        header_frame = tk.Frame(self, bg=THEME_COLOR, height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Título y usuario
        title_frame = tk.Frame(header_frame, bg=THEME_COLOR)
        title_frame.pack(expand=True, fill="both")
        
        tk.Label(title_frame, text=f"🏪 {APP_NAME}", 
                font=("Arial", 20, "bold"), bg=THEME_COLOR, fg="white").pack(side="left", padx=20, pady=20)
        
        tk.Label(title_frame, text=f"👤 {self.usuario}", 
                font=("Arial", 12), bg=THEME_COLOR, fg="white").pack(side="right", padx=20, pady=20)
        
        # Menú lateral
        menu_frame = tk.Frame(self, bg="#5ccfeb", width=200)
        menu_frame.pack(side="left", fill="y")
        menu_frame.pack_propagate(False)
        
        # Título del menú
        tk.Label(menu_frame, text="MENÚ PRINCIPAL", font=("Arial", 12, "bold"), 
                bg="#e79052", fg="#2c3e50").pack(pady=20)
        
        # Botones del menú
        self._crear_menu_botones(menu_frame)
        
        # Área de contenido principal
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(side="right", fill="both", expand=True)
    
    def _crear_menu_botones(self, parent):
        botones = [
            ("📦 Inventario", SUCCESS_COLOR, self.mostrar_inventario),
            ("💰 Ventas", INFO_COLOR, self.mostrar_ventas),
            ("📋 Despachos", WARNING_COLOR, self.mostrar_despachos),
            ("👥 Empleados", "#9678e3", self.mostrar_empleados),
            ("📊 Reportes", "#e67e22", self.mostrar_reportes),
            ("🛒 Compras", "#1abc9c", self.mostrar_compras),
            ("📁 Categorías", "#34495e", self.mostrar_categorias),
        ]
        
        for texto, color, comando in botones:
            btn = tk.Button(parent, text=texto, command=comando,
                           bg=color, fg="white", font=("Arial", 11, "bold"),
                           relief="flat", bd=0, pady=12, cursor="hand2")
            btn.pack(fill="x", padx=10, pady=2)
            
            # Efectos hover
            def on_enter(e, btn=btn, color=color):
                btn.config(bg=self._darken_color(color))
            
            def on_leave(e, btn=btn, color=color):
                btn.config(bg=color)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)
        
        # Separador
        tk.Frame(parent, height=2, bg="#5ccfeb").pack(fill="x", pady=20, padx=10)
        
        # Botón de cerrar sesión
        btn_logout = tk.Button(parent, text="🚪 Cerrar Sesión", command=self._cerrar_sesion,
                              bg=ERROR_COLOR, fg="white", font=("Arial", 11, "bold"),
                              relief="flat", bd=0, pady=12, cursor="hand2")
        btn_logout.pack(fill="x", padx=10, pady=5)
    
    def _darken_color(self, color):
        # Implementación simple para oscurecer colores
        color_map = {
            SUCCESS_COLOR: "#27ae60",
            INFO_COLOR: "#2980b9", 
            WARNING_COLOR: "#e67e22",
            ERROR_COLOR: "#c0392b",
            "#9b59b6": "#8e44ad",
            "#1abc9c": "#16a085",
            "#34495e": "#2c3e50"
        }
        return color_map.get(color, color)
    
    def limpiar_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def mostrar_inventario(self):
        self.limpiar_main()
        from views.inventario import InventarioFrame
        InventarioFrame(self.main_frame)
    
    def mostrar_ventas(self):
        self.limpiar_main()
        tk.Label(self.main_frame, text="🚧 Módulo de Ventas", 
                font=("Arial", 24), bg="white", fg="#95a5a6").pack(expand=True)
        tk.Label(self.main_frame, text="Próximamente en Sprint 2", 
                font=("Arial", 14), bg="white", fg="#7f8c8d").pack()
    
    def mostrar_despachos(self):
        self.limpiar_main()
        tk.Label(self.main_frame, text="🚧 Módulo de Despachos", 
                font=("Arial", 24), bg="white", fg="#95a5a6").pack(expand=True)
        tk.Label(self.main_frame, text="Próximamente en Sprint 3", 
                font=("Arial", 14), bg="white", fg="#7f8c8d").pack()
    
    def mostrar_empleados(self):
        self.limpiar_main()
        tk.Label(self.main_frame, text="🚧 Módulo de Empleados", 
                font=("Arial", 24), bg="white", fg="#95a5a6").pack(expand=True)
        tk.Label(self.main_frame, text="Próximamente en Sprint 4", 
                font=("Arial", 14), bg="white", fg="#7f8c8d").pack()
    
    def mostrar_reportes(self):
        self.limpiar_main()
        tk.Label(self.main_frame, text="🚧 Módulo de Reportes", 
                font=("Arial", 24), bg="white", fg="#95a5a6").pack(expand=True)
        tk.Label(self.main_frame, text="Próximamente en Sprint 5", 
                font=("Arial", 14), bg="white", fg="#7f8c8d").pack()
    
    def mostrar_compras(self):
        self.limpiar_main()
        tk.Label(self.main_frame, text="🚧 Módulo de Compras", 
                font=("Arial", 24), bg="white", fg="#95a5a6").pack(expand=True)
        tk.Label(self.main_frame, text="Próximamente en Sprint 6", 
                font=("Arial", 14), bg="white", fg="#7f8c8d").pack()
    
    def mostrar_categorias(self):
        self.limpiar_main()
        tk.Label(self.main_frame, text="🚧 Módulo de Categorías", 
                font=("Arial", 24), bg="white", fg="#95a5a6").pack(expand=True)
        tk.Label(self.main_frame, text="Próximamente en Sprint 2", 
                font=("Arial", 14), bg="white", fg="#7f8c8d").pack()
    
    def _cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro que deseas cerrar la sesión?"):
            self.destroy()  
            self.quit()    