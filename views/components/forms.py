## Formularios y componentes reutilizables

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
from config.settings import *
from utils.helpers import *

class ProductoForm(tk.Toplevel):    
    def __init__(self, parent, title="Producto", producto_data=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("520x510")
        self.resizable(False, False)
        self.parent = parent
        self.producto_data = producto_data
        self.config(bg="white")
        self.img_var = tk.StringVar()
        self.categoria_var = tk.StringVar()
        self.corte_var = tk.StringVar()
        self.entries = {}
        
        self._crear_interfaz()
        if producto_data is not None and not producto_data.empty:
            self._llenar_campos()
    
    def _crear_interfaz(self):
        # Título
        titulo = "Modificar Producto" if (self.producto_data is not None and not self.producto_data.empty) else "Registrar Producto"
        tk.Label(self, text=titulo, font=("Arial", 18), bg="white", fg=THEME_COLOR).pack(pady=10)
        
        # Campos de entrada
        campos = [("Nombre", ""), ("Precio", "0"), ("Stock inicial", "0"), ("Stock Mínimo", "0")]
        for label, default in campos:
            frame = tk.Frame(self, bg="white")
            frame.pack(pady=5)
            tk.Label(frame, text=label+":", bg="white").pack(side="left")
            entry = tk.Entry(frame)
            if self.producto_data is None or self.producto_data.empty:  # Solo poner default si es nuevo producto
                entry.insert(0, default)
            entry.pack(side="left")
            self.entries[label] = entry
        
        # Categoría
        frame_cat = tk.Frame(self, bg="white")
        frame_cat.pack(pady=5)
        tk.Label(frame_cat, text="Categoría:", bg="white").pack(side="left")
        self.categoria_cb = ttk.Combobox(frame_cat, textvariable=self.categoria_var, values=cargar_categorias(), state="readonly")
        self.categoria_cb.pack(side="left")
        ttk.Button(frame_cat, text="Nueva...", command=self._agregar_categoria_rapido).pack(side="left", padx=5)
        
        # Tipo de corte
        frame_corte = tk.Frame(self, bg="white")
        frame_corte.pack(pady=5)
        tk.Label(frame_corte, text="Tipo de Corte:", bg="white").pack(side="left")
        self.corte_cb = ttk.Combobox(frame_corte, textvariable=self.corte_var,
                                   values=["", "Entero", "Bistec", "Molida", "Churrasco", "Costilla", 
                                          "Filete", "Pechuga", "Pierna", "Alitas", "Trozos", "Otros"],
                                   state="readonly")
        self.corte_cb.pack(side="left")
        
        # Imagen
        frame_img = tk.Frame(self, bg="white")
        frame_img.pack(pady=5)
        tk.Label(frame_img, text="Imagen (opcional):", bg="white").pack(side="left")
        ttk.Button(frame_img, text="Seleccionar", command=self._seleccionar_imagen).pack(side="left", padx=2)
        self.img_label = tk.Label(frame_img, text="", bg="white")
        self.img_label.pack(side="left")
        
        # Botones
        frame_botones = tk.Frame(self, bg="white")
        frame_botones.pack(pady=20)
        
        texto_guardar = "Guardar Cambios" if (self.producto_data is not None and not self.producto_data.empty) else "Guardar"
        boton_grande(frame_botones, texto_guardar, INFO_COLOR, self._guardar, "💾").pack(side="left", padx=5)
        boton_grande(frame_botones, "Cancelar", ERROR_COLOR, self.destroy, "❌").pack(side="left", padx=5)
    
    def _llenar_campos(self):
        if self.producto_data is None or self.producto_data.empty:
            return
        
        # Llenar campos de texto
        self.entries["Nombre"].insert(0, str(self.producto_data.get("Nombre", "")))
        self.entries["Precio"].insert(0, str(self.producto_data.get("Precio", 0)))
        self.entries["Stock inicial"].insert(0, str(self.producto_data.get("Stock", 0)))
        self.entries["Stock Mínimo"].insert(0, str(self.producto_data.get("Stock Mínimo", 0)))
        
        # Establecer categoría y tipo de corte
        self.categoria_var.set(str(self.producto_data.get("Categoría", "")))
        self.corte_var.set(str(self.producto_data.get("Tipo de Corte", "")))
        
        # Establecer imagen
        imagen_actual = self.producto_data.get("Imagen", "")
        if imagen_actual and os.path.exists(imagen_actual):
            self.img_var.set(imagen_actual)
            self.img_label.config(text=os.path.basename(imagen_actual))
    
    def _agregar_categoria_rapido(self):
        from tkinter import simpledialog
        nueva_categoria = simpledialog.askstring("Nueva Categoría", 
                                                "Ingrese el nombre de la nueva categoría:",
                                                parent=self)
        if nueva_categoria and nueva_categoria.strip():
            nueva_categoria = nueva_categoria.strip()
            try:
                # Agregar a la base de datos
                from db.database import db
                db.execute_query("INSERT OR IGNORE INTO categorias (nombre, descripcion) VALUES (?, ?)", 
                               (nueva_categoria, f"Categoría {nueva_categoria}"))
                
                # Recargar las categorías en el dropdown
                categorias_actualizadas = cargar_categorias()
                self.categoria_cb['values'] = categorias_actualizadas
                
                # Seleccionar la nueva categoría
                self.categoria_var.set(nueva_categoria)
                
                messagebox.showinfo("Éxito", f"Categoría '{nueva_categoria}' agregada correctamente.", parent=self)
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar la categoría: {e}", parent=self)
    
    def _seleccionar_imagen(self):
        path = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
        )
        if path:
            self.img_var.set(path)
            self.img_label.config(text=os.path.basename(path))
    
    def _validar_datos(self):
        nombre = self.entries["Nombre"].get().strip()
        
        # Obtener categoría de ambas fuentes (por si hay problemas con readonly)
        categoria_var = self.categoria_var.get().strip()
        categoria_widget = self.categoria_cb.get().strip()
        categoria = categoria_var or categoria_widget
        
        if not nombre:
            messagebox.showerror("Error", "El nombre del producto es obligatorio.", parent=self)
            return None
        
        if not categoria:
            messagebox.showerror("Error", "Debes seleccionar una categoría del dropdown.", parent=self)
            return None
        
        # Validar campos numéricos
        precio, precio_valido = validar_numero(self.entries["Precio"].get())
        stock, stock_valido = validar_numero(self.entries["Stock inicial"].get(), "int")
        stock_min, stock_min_valido = validar_numero(self.entries["Stock Mínimo"].get(), "int")
        
        if not precio_valido:
            messagebox.showerror("Error", "El precio debe ser un número válido.", parent=self)
            return None
        
        if not stock_valido:
            messagebox.showerror("Error", "El stock debe ser un número entero válido.", parent=self)
            return None
        
        if not stock_min_valido:
            messagebox.showerror("Error", "El stock mínimo debe ser un número entero válido.", parent=self)
            return None
        
        return {
            "Nombre": nombre,
            "Categoría": categoria,
            "Tipo de Corte": self.corte_var.get().strip(),
            "Precio": precio,
            "Stock": stock,
            "Stock Mínimo": stock_min,
            "imagen_origen": self.img_var.get() if self.img_var.get() else None
        }

    def _guardar(self):
        raise NotImplementedError("Debe implementarse en la clase hija")

class ImagenViewer(tk.Label):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.imagen_actual = None
    
    def mostrar_imagen(self, ruta_imagen, tamaño=(200, 200)):
        try:
            # Limpiar imagen anterior primero
            self.limpiar()
            
            if ruta_imagen and os.path.exists(ruta_imagen):
                imagen = Image.open(ruta_imagen)
                imagen = imagen.resize(tamaño, Image.Resampling.LANCZOS)
                self.imagen_actual = ImageTk.PhotoImage(imagen)
                self.config(image=self.imagen_actual)
                # Mantener una referencia para evitar garbage collection
                self.image = self.imagen_actual
            else:
                self.limpiar()
        except Exception as e:
            # Solo imprimir si es un error real, no de imagen que no existe
            if "doesn't exist" not in str(e):
                print(f"Error al cargar imagen: {e}")
            self.limpiar()
    
    def limpiar(self):
        if hasattr(self, 'image'):
            delattr(self, 'image')
        self.config(image="")
        self.imagen_actual = None