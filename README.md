# 🏪 Sistema Minimarket Don Manuelito

Sistema POS (Point of Sale) modular para minimarket desarrollado en Python con tkinter.

## 📋 Descripción

Sistema de gestión completo para minimarket que incluye manejo de inventario, ventas, empleados y reportes. Desarrollado siguiendo metodología SCRUM con arquitectura modular escalable.

## 🚀 Estado del Proyecto

**Sprint 1 ✅ COMPLETADO** - Módulo de Inventario
- CRUD completo de productos
- Manejo de imágenes
- Sistema de categorías
- Interfaz moderna y profesional

## 🛠️ Tecnologías

- **Python 3.x**
- **tkinter** - Interfaz gráfica
- **pandas** - Manejo de datos Excel
- **Pillow (PIL)** - Procesamiento de imágenes
- **Excel** - Base de datos temporal

## 📦 Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/TU_USUARIO/Sistema-Minimarket-wa.git
cd Sistema-Minimarket-wa
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar aplicación**
```bash
python main.py
```

## 🔑 Credenciales por Defecto

- **Usuario**: `admin`
- **Contraseña**: `admin`

## 📁 Estructura del Proyecto

```
Sistema-Minimarket-wa/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── config/
│   └── settings.py        # Configuraciones
├── models/
│   └── producto.py        # Lógica de datos
├── views/
│   ├── login.py           # Pantalla de login
│   ├── dashboard.py       # Menú principal
│   ├── inventario.py      # Módulo de inventario
│   └── components/
│       └── forms.py       # Formularios reutilizables
├── utils/
│   └── helpers.py         # Funciones auxiliares
├── db/                    # Archivos Excel de datos
└── reportes/              # Reportes generados
```

## ✨ Funcionalidades

### ✅ Sprint 1 - Inventario
- [x] Login con interfaz moderna
- [x] Dashboard principal
- [x] Registrar productos
- [x] Modificar productos
- [x] Eliminar productos
- [x] Visualizar inventario en tiempo real
- [x] Manejo de imágenes de productos
- [x] Sistema de categorías

### 🚧 Próximos Sprints
- [ ] **Sprint 2**: Módulo de Ventas
- [ ] **Sprint 3**: Módulo de Despachos  
- [ ] **Sprint 4**: Gestión de Empleados
- [ ] **Sprint 5**: Reportes y Analytics

## 🎨 Capturas de Pantalla

### Login
![Login](docs/login-screenshot.png)

### Dashboard
![Dashboard](docs/dashboard-screenshot.png)

### Inventario
![Inventario](docs/inventario-screenshot.png)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Tu Nombre** - [@tu_usuario](https://github.com/tu_usuario)

## 🙏 Agradecimientos

- Inspirado en las necesidades reales de pequeños negocios
- Desarrollado como proyecto educativo
- Gracias a la comunidad Python por las librerías utilizadas

---
⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub!