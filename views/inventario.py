## Vista del módulo de inventario

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from PIL import Image, ImageTk
from models.producto import ProductoModel
from views.components.forms import ProductoForm, ImagenViewer
from utils.helpers import boton_grande, formatear_precio
from config.settings import *

class InventarioFrame(tk.Frame):      
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)
        
        self.producto_model = ProductoModel()
        self._crear_interfaz()
        self.mostrar_inventario()
    
    def _crear_interfaz(self):
        # Título
        tk.Label(self, text="Inventario", font=("Arial", 22, "bold"), 
                bg="white", fg=THEME_COLOR).pack(pady=10)
        
        # Configurar estilo del Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 11), rowheight=28)
        style.map("Treeview", background=[("selected", "#d6eaf8")])
        
        # Tabla de productos
        columnas = ("ID", "Nombre", "Categoría", "Tipo de Corte", "Precio", "Stock", "Stock Mínimo", "Imagen")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings", selectmode="browse")
        
        # Configurar columnas
        anchos = {"ID": 80, "Nombre": 180, "Categoría": 120, "Tipo de Corte": 130, 
                 "Precio": 80, "Stock": 80, "Stock Mínimo": 100, "Imagen": 110}
        
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=anchos.get(col, 100), anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Botones de acción
        self.boton_frame = tk.Frame(self, bg="white")
        self.boton_frame.pack(pady=10)
        
        boton_grande(self.boton_frame, "Agregar Producto", SUCCESS_COLOR, 
                    self._agregar_producto, "➕").pack(side="left", padx=10)
        boton_grande(self.boton_frame, "Modificar Producto", INFO_COLOR, 
                    self._modificar_producto, "✏️").pack(side="left", padx=10)
        boton_grande(self.boton_frame, "Eliminar Producto", ERROR_COLOR, 
                    self._eliminar_producto, "🗑️").pack(side="left", padx=10)
        boton_grande(self.boton_frame, "Refrescar", "#2980b9", 
                    self.mostrar_inventario, "🔃").pack(side="left", padx=10)
        
        # Visor de imagen
        self.img_viewer = ImagenViewer(self, bg="white")
        self.img_viewer.pack(pady=8)
        
        # Bind para mostrar imagen al seleccionar
        self.tree.bind("<<TreeviewSelect>>", self._mostrar_imagen_producto)
    
    def mostrar_inventario(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener productos
        df = self.producto_model.obtener_todos()
        
        # Llenar tabla
        for _, row in df.iterrows():
            precio = formatear_precio(row.get("Precio", 0))
            stock_actual = int(row["Stock"]) if pd.notna(row["Stock"]) else 0
            stock_minimo = int(row["Stock Mínimo"]) if pd.notna(row["Stock Mínimo"]) else 0
            
            values = (
                row["ID"], 
                row["Nombre"], 
                row["Categoría"], 
                row.get("Tipo de Corte", ""),
                precio, 
                stock_actual, 
                stock_minimo,
                os.path.basename(row["Imagen"]) if pd.notna(row["Imagen"]) and str(row["Imagen"]).strip() else ""
            )
            
            self.tree.insert("", "end", values=values)
        
        # Limpiar visor de imagen
        self.img_viewer.limpiar()
    
    def _mostrar_imagen_producto(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        values = item["values"]
        if len(values) > 0:
            producto_id = values[0]
            producto = self.producto_model.obtener_por_id(producto_id)
            
            if producto is not None:
                imagen_path = producto.get("Imagen", "")
                self.img_viewer.mostrar_imagen(imagen_path)
    
    def _agregar_producto(self):
        AgregarProductoForm(self)
    
    def _modificar_producto(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Modificar producto", "Selecciona un producto para modificar.")
            return
        
        item = self.tree.item(selection[0])
        producto_id = item["values"][0]
        producto_data = self.producto_model.obtener_por_id(producto_id)
        
        if producto_data is not None:
            ModificarProductoForm(self, producto_data)
    
    def _eliminar_producto(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Eliminar producto", "Selecciona un producto para eliminar.")
            return
        
        item = self.tree.item(selection[0])
        values = item["values"]
        producto_id = values[0]
        nombre_producto = values[1]
        
        if messagebox.askyesno("Confirmar eliminación", 
                              f"¿Seguro que deseas eliminar el producto '{nombre_producto}'?"):
            if self.producto_model.eliminar(producto_id):
                self.mostrar_inventario()
                messagebox.showinfo("Producto eliminado", 
                                   f"Producto '{nombre_producto}' eliminado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto.")

class AgregarProductoForm(ProductoForm):    
    def __init__(self, parent):
        self.parent_frame = parent
        super().__init__(parent, "Registrar Producto")
    
    def _guardar(self):
        """Guarda el nuevo producto"""
        datos = self._validar_datos()
        if datos is None:
            return
        
        try:
            producto_model = ProductoModel()
            nuevo_id = producto_model.crear(datos)
            messagebox.showinfo("Éxito", "Producto registrado correctamente.", parent=self)
            self.parent_frame.mostrar_inventario()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error al guardar", f"Error: {e}", parent=self)

class ModificarProductoForm(ProductoForm):
    def __init__(self, parent, producto_data):
        self.parent_frame = parent
        self.producto_id = producto_data["ID"]
        super().__init__(parent, "Modificar Producto", producto_data)
    
    def _guardar(self):
        """Guarda los cambios del producto"""
        datos = self._validar_datos()
        if datos is None:
            return
        
        try:
            producto_model = ProductoModel()
            producto_model.actualizar(self.producto_id, datos)
            messagebox.showinfo("Éxito", "Producto modificado correctamente.", parent=self)
            self.parent_frame.mostrar_inventario()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error al guardar", f"Error: {e}", parent=self)
