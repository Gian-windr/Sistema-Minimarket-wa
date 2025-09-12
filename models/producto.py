# Modelo para manejar los datos de productos

import pandas as pd
import os
import shutil
from config.settings import *
from utils.helpers import generar_id

class ProductoModel:
    def __init__(self):
        self.columnas = ["ID", "Nombre", "Categoría", "Tipo de Corte", "Precio", "Stock", "Stock Mínimo", "Imagen"]
        self._inicializar_archivo()

    def _inicializar_archivo(self):
        if not os.path.exists(PRODUCTOS_FILE):
            pd.DataFrame(columns=self.columnas).to_excel(PRODUCTOS_FILE, index=False)
    
    def obtener_todos(self):
        try:
            return pd.read_excel(PRODUCTOS_FILE).reindex(columns=self.columnas)
        except:
            return pd.DataFrame(columns=self.columnas)
    
    def obtener_por_id(self, producto_id):
        df = self.obtener_todos()
        productos = df[df["ID"] == producto_id]
        return productos.iloc[0] if not productos.empty else None
    
    def crear(self, datos): 
        df = self.obtener_todos()   
        # Generar ID único
        nuevo_id = generar_id("P")
        datos["ID"] = nuevo_id
        # Manejar imagen si existe
        if datos.get("imagen_origen"):
            imagen_destino = self._copiar_imagen(datos["imagen_origen"], nuevo_id)
            datos["Imagen"] = imagen_destino
        else:
            datos["Imagen"] = ""
        
        # Crear DataFrame con el nuevo producto
        nuevo_producto = pd.DataFrame([datos], columns=self.columnas)
        df = pd.concat([df, nuevo_producto], ignore_index=True)
        
        # Guardar
        df.to_excel(PRODUCTOS_FILE, index=False)
        return nuevo_id
    
    # Actualiza un producto existente
    def actualizar(self, producto_id, datos):
        df = self.obtener_todos()
        indice = df[df["ID"] == producto_id].index
        if indice.empty:
            raise ValueError(f"Producto con ID {producto_id} no encontrado")
        
        idx = indice[0]
        
        # Actualizar campos
        for campo, valor in datos.items():
            if campo in self.columnas and campo != "ID":
                df.at[idx, campo] = valor
        
        # Manejar imagen si se proporciona una nueva
        if datos.get("imagen_origen"):
            imagen_destino = self._copiar_imagen(datos["imagen_origen"], producto_id)
            df.at[idx, "Imagen"] = imagen_destino
        
        # Guardar
        df.to_excel(PRODUCTOS_FILE, index=False)
        return True
    
    # Elimina un producto
    def eliminar(self, producto_id):
        df = self.obtener_todos()
        df_nuevo = df[df["ID"] != producto_id]
        if len(df_nuevo) == len(df):
            return False  # No se encontró el producto
        
        df_nuevo.to_excel(PRODUCTOS_FILE, index=False)
        return True
    
    # Copia una imagen al directorio de productos
    def _copiar_imagen(self, origen, producto_id):
        try:
            if not os.path.exists(origen):
                return ""
            extension = os.path.splitext(origen)[1]
            destino = os.path.join(IMG_DIR, f"{producto_id}{extension}")
            shutil.copy(origen, destino)
            return destino
        except Exception as e:
            print(f"Error al copiar imagen: {e}")
            return ""
    
    # Busca productos por nombre, ID o categoría
    def buscar(self, termino):
        df = self.obtener_todos()
        if termino.strip():
            termino = termino.lower()
            mask = (
                df["Nombre"].str.lower().str.contains(termino, na=False) |
                df["ID"].str.lower().str.contains(termino, na=False) |
                df["Categoría"].str.lower().str.contains(termino, na=False)
            )
            return df[mask]
        return df
    
    # Obtiene productos con stock bajo o crítico
    def obtener_stock_bajo(self):
        df = self.obtener_todos()
        productos_problematicos = []
        
        for _, row in df.iterrows():
            stock_actual = int(row["Stock"]) if pd.notna(row["Stock"]) else 0
            stock_minimo = int(row["Stock Mínimo"]) if pd.notna(row["Stock Mínimo"]) else 0
            if stock_minimo > 0:
                if stock_actual <= stock_minimo:
                    productos_problematicos.append({
                        'tipo': 'critico',
                        'producto': row
                    })
                elif stock_actual <= stock_minimo * 1.5:
                    productos_problematicos.append({
                        'tipo': 'bajo',
                        'producto': row
                    })
        return productos_problematicos