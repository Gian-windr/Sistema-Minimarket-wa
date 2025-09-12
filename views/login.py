import tkinter as tk
from tkinter import messagebox
import pandas as pd
from config.settings import *
from PIL import Image, ImageTk

class LoginVentana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} - Login")
        self.geometry("1024x768")
        self.resizable(False, False)
        self.config(bg="white")
        self.center_window()
        
        self.usuario_logueado = None
        self._crear_interfaz()
    
    def center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
    
    def _crear_interfaz(self):
        # Contenedor principal con dos columnas
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill="both", expand=True)
        
        # LADO IZQUIERDO - Imagen del minimarket
        left_frame = tk.Frame(main_frame, bg="#f8f9fa")
        left_frame.pack(side="left", fill="both", expand=True)
        
        try:
            imagen_original = Image.open("C:/Users/LENOVO LOQ/Sistema-Minimarket-wa/db/imagenes/minimercado.jpg")
            imagen_redimensionada = imagen_original.crop((0, 0, 720, 720))  # Recortar la imagen
            
            # Convertir para tkinter
            self.fondo_img = ImageTk.PhotoImage(imagen_redimensionada)
            fondo_label = tk.Label(left_frame, image=self.fondo_img)
            fondo_label.pack(fill="both", expand=True)
        except:
            # Si no hay imagen, mostrar placeholder elegante
            placeholder_frame = tk.Frame(left_frame, bg="#e9ecef")
            placeholder_frame.pack(fill="both", expand=True)
            
            tk.Label(placeholder_frame, text="🏪", font=("Arial", 120), 
                    bg="#e9ecef", fg="#6c757d").place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(placeholder_frame, text="MINIMARKET", font=("Arial", 24, "bold"), 
                    bg="#e9ecef", fg="#495057").place(relx=0.5, rely=0.6, anchor="center")
        
        # LADO DERECHO - Formulario de login
        right_frame = tk.Frame(main_frame, bg="white", width=400)
        right_frame.pack(side="right", fill="y", padx=0, pady=0)
        right_frame.pack_propagate(False)
        
        # Contenedor del formulario centrado
        form_container = tk.Frame(right_frame, bg="white")
        form_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo y título del formulario
        logo_frame = tk.Frame(form_container, bg="white")
        logo_frame.pack(pady=(0, 20))
        
        # Cargar imagen del logo con título
        try:
            logo_original = Image.open("C:/Users/LENOVO LOQ/Sistema-Minimarket-wa/db/imagenes/LOGOT.png")
            logo_redimensionado = logo_original.resize((240, 55), Image.Resampling.LANCZOS)
            # Convertir para tkinter
            self.logo_img = ImageTk.PhotoImage(logo_redimensionado)
            logo_label = tk.Label(logo_frame, image=self.logo_img, bg="white")
            logo_label.pack()
        except Exception as e:
            print(f"Error logo: {e}")  # Ver el error en consola
            tk.Label(logo_frame, text="🏪 DON MANUELITO", 
                    font=("Arial", 18, "bold"), bg="white", fg="#4285F4").pack()
        
        # Subtítulo
        tk.Label(form_container, text="Iniciar sesión", 
                font=("Times New Roman", 24, "bold"), bg="white", fg="#1a1a1a").pack(pady=(0, 5))
        
        # Subtítulo secundario
        tk.Label(form_container, text="Acceder", 
                font=("Times New Roman", 14), bg="white", fg="#6c757d").pack(pady=(0, 30))
        
        # Campos del formulario
        ## Usuario
        tk.Label(form_container, text="Nombre de usuario", 
                font=("Times New Roman", 12), bg="white", fg="#495057").pack(anchor="w", pady=(0, 5))
        
        user_frame = tk.Frame(form_container, bg="white")
        user_frame.pack(fill="x", pady=(0, 20))
        
        self.usuario_entry = tk.Entry(user_frame, font=("Times New Roman", 12), width=25, 
                                      bg="#f8f9fa", fg="#495057", bd=1, relief="solid",
                                     highlightthickness=1, highlightcolor="#4285F4")
        self.usuario_entry.pack(fill="x", ipady=8, padx=2)
        
        # Contraseña
        tk.Label(form_container, text="Contraseña", 
                font=("Times New Roman", 12), bg="white", fg="#495057").pack(anchor="w", pady=(0, 5))
        
        pass_frame = tk.Frame(form_container, bg="white")
        pass_frame.pack(fill="x", pady=(0, 30))
        
        self.password_entry = tk.Entry(pass_frame, font=("Arial", 12), width=25, show="*",
                                      bg="#f8f9fa", fg="#495057", bd=1, relief="solid",
                                      highlightthickness=1, highlightcolor="#4285F4")
        self.password_entry.pack(fill="x", ipady=8, padx=2)
        
        # Botón de iniciar sesión
        login_btn = tk.Button(form_container, text="Iniciar sesión", 
                             command=self._login, bg="#4285F4", fg="white",
                             font=("Arial", 12, "bold"), relief="flat", bd=0,
                             cursor="hand2", pady=12)
        login_btn.pack(fill="x", pady=(0, 20))
        
        # Efectos hover para el botón
        def on_enter(e):
            login_btn.config(bg="#3367D6")
        def on_leave(e):
            login_btn.config(bg="#4285F4")
        
        login_btn.bind("<Enter>", on_enter)
        login_btn.bind("<Leave>", on_leave)
        
        # Link de olvidé contraseña
        forgot_link = tk.Label(form_container, text="¿Olvidó su contraseña?", 
                              font=("Arial", 10, "underline"), bg="white", 
                              fg="#4285F4", cursor="hand2")
        forgot_link.pack()
        
        # Bindings para navegación
        self.usuario_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self._login())
        self.usuario_entry.focus()
    
    def _login(self):
        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Por favor ingrese usuario y contraseña.")
            return
        
        # Validar credenciales
        if self._validar_credenciales(usuario, password):
            self.usuario_logueado = usuario
            self._abrir_dashboard()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def _validar_credenciales(self, usuario, password):
        try:
            df = pd.read_excel(EMPLEADOS_FILE)
            empleado = df[(df["Usuario"] == usuario) & (df["Contraseña"] == password)]
            return not empleado.empty
        except:
            # Credenciales por defecto si no existe el archivo
            return usuario == "admin" and password == "admin"
    
    def _abrir_dashboard(self):
        self.withdraw()  # Ocultar ventana de login
        
        # Importar aquí para evitar importación circular
        from views.dashboard import Dashboard
        
        dashboard = Dashboard(self.usuario_logueado)
        dashboard.protocol("WM_DELETE_WINDOW", self._volver_al_login)
        dashboard.mainloop()
        
        # Cuando el dashboard se cierre, mostrar login de nuevo
        self.deiconify() 
        self.usuario_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.usuario_entry.focus()
    
    def _volver_al_login(self):
        # Este método se llama cuando se cierra el dashboard con la X
        # Terminar el mainloop y cerrar aplicación completamente
        self.quit()
        self.destroy()
    
    def _cerrar_aplicacion(self):
        self.quit()
        self.destroy()