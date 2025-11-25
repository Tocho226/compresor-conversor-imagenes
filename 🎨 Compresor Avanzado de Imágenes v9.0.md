# 🎨 Compresor Avanzado de Imágenes v9.0

Una aplicación profesional de compresión de imágenes con soporte para 30+ formatos, interfaz moderna y funcionalidades avanzadas.

## ✨ Características Principales

### 🖼️ Soporte Universal de Formatos
- **Entrada y Salida:** 30+ formatos incluyendo JPG, PNG, GIF, BMP, TIFF, WebP, AVIF, HEIC, SVG, PDF, PSD, ICNS, FITS, y más
- **Conversión Real:** Cada formato usa su librería especializada (no conversiones forzadas)
- **Formatos Especiales:** Soporte real para PDF, SVG, EPS, PSD con librerías dedicadas

### 🎨 Interfaz Moderna
- **Diseño Profesional:** Colores modernos con degradados azul-púrpura
- **Temas Dinámicos:** Alternancia entre claro y oscuro
- **Vista Previa en Tiempo Real:** Se actualiza conforme se comprimen las imágenes
- **Drag & Drop Funcional:** Arrastra archivos directamente a la aplicación

### ⚡ Funcionalidades Avanzadas
- **Compresión Inteligente:** Motor optimizado con PIL y librerías especializadas
- **Control de Duplicados:** Genera nombres únicos automáticamente
- **Historial Persistente:** Guarda y exporta historial de compresiones
- **Configuración Persistente:** Recuerda preferencias del usuario
- **Atajos de Teclado:** Ctrl+O, Ctrl+S, F1 para mayor eficiencia

## 📁 Estructura del Proyecto

```
compresor-imagenes/
├── main.py                    # Archivo principal de ejecución
├── requirements.txt           # Dependencias del proyecto
├── README.md                 # Esta documentación
├── core/                     # Módulos principales
│   ├── __init__.py
│   ├── format_handler.py     # Manejo universal de formatos
│   └── compression_engine.py # Motor de compresión
├── gui/                      # Interfaz gráfica
│   ├── __init__.py
│   └── app.py               # Aplicación GUI principal
└── utils/                    # Utilidades
    ├── __init__.py
    ├── theme_manager.py      # Gestión de temas
    ├── config_manager.py     # Configuración persistente
    ├── history_manager.py    # Gestión de historial
    └── icon_manager.py       # Gestión de iconos
```

## 🚀 Instalación y Uso

### 1. Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 2. Instalación Básica
```bash
# Clonar o descargar el proyecto
cd compresor-imagenes

# Instalar dependencias básicas
pip install Pillow tkinterdnd2

# Ejecutar aplicación
python main.py
```

### 3. Instalación Completa (Todos los Formatos)
```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python main.py
```

### 4. Instalación por Módulos (Opcional)
```bash
# Solo formatos básicos
pip install Pillow

# Añadir drag & drop
pip install tkinterdnd2

# Añadir HEIC/HEIF
pip install pillow-heif

# Añadir AVIF
pip install pillow-avif-plugin

# Añadir SVG/EPS (requiere ImageMagick)
pip install Wand

# Añadir PSD
pip install psd-tools

# Añadir FITS
pip install astropy

# Añadir PDF
pip install reportlab pdf2image
```

## 📖 Cómo Usar

### Interfaz Principal
1. **Seleccionar Imágenes:**
   - Arrastra archivos al área designada, o
   - Haz clic en "Seleccionar Imágenes" (Ctrl+O)

2. **Configurar Compresión:**
   - Ajusta la calidad (10-100%)
   - Selecciona formato de salida
   - Configura redimensionado (opcional)

3. **Comprimir:**
   - Haz clic en "Comprimir Imágenes" (Ctrl+S)
   - Selecciona carpeta de destino
   - Observa el progreso en tiempo real

### Atajos de Teclado
- `Ctrl+O`: Seleccionar imágenes
- `Ctrl+S`: Comprimir imágenes
- `F1`: Mostrar ayuda
- `Ctrl+Q`: Salir de la aplicación

### Funcionalidades Avanzadas
- **Historial:** Haz doble clic en entradas para ver detalles
- **Exportar Historial:** Guarda en CSV o JSON
- **Temas:** Alterna entre claro y oscuro
- **Vista Previa:** Se actualiza automáticamente durante la compresión

## 🎯 Formatos Soportados

### Formatos Básicos
- **JPEG/JPG** - Compresión con pérdida optimizada
- **PNG** - Compresión sin pérdida con transparencia
- **GIF** - Imágenes animadas y paleta limitada
- **BMP** - Formato bitmap sin compresión
- **TIFF/TIF** - Formato profesional de alta calidad
- **WebP** - Formato moderno de Google
- **ICO** - Iconos de Windows

### Formatos Modernos
- **AVIF** - Formato de nueva generación
- **HEIC/HEIF** - Formato de Apple (iOS)

### Formatos Especializados
- **SVG** - Gráficos vectoriales escalables
- **DDS** - Texturas para videojuegos
- **TGA** - Formato Targa para gráficos
- **EPS** - PostScript encapsulado
- **IM** - Formato interno de PIL

### Formatos de Solo Lectura (Convertibles)
- **PDF** - Cada página como imagen
- **PSD** - Archivos de Photoshop
- **ICNS** - Iconos de macOS
- **FITS** - Formato astronómico
- **MSP** - Microsoft Paint antiguo

### Formatos Adicionales
- **PPM, PGM, PBM** - Formatos Netpbm
- **PCX** - Formato PC Paintbrush
- **SGI** - Silicon Graphics
- **SPIDER** - Formato científico
- **XBM, XPM** - Formatos X11

## ⚙️ Configuración

### Configuraciones Disponibles
- **Tema:** Claro/Oscuro
- **Calidad por defecto:** 10-100%
- **Formato preferido:** Cualquier formato soportado
- **Mantener aspecto:** Sí/No
- **Directorios recientes:** Automático
- **Atajos de teclado:** Habilitados/Deshabilitados

### Archivos de Configuración
- `image_compressor_config.json` - Configuración principal
- `compression_history.json` - Historial de compresiones

## 🛠️ Solución de Problemas

### Problemas Comunes

**1. Error "tkinterdnd2 no disponible"**
```bash
pip install tkinterdnd2
```

**2. Formatos especiales no funcionan**
```bash
# Instalar dependencias específicas
pip install pillow-heif pillow-avif-plugin Wand psd-tools
```

**3. Error con ImageMagick (SVG/EPS)**
- Windows: Descargar ImageMagick desde el sitio oficial
- Linux: `sudo apt-get install imagemagick libmagickwand-dev`
- macOS: `brew install imagemagick`

**4. Problemas de permisos**
```bash
# Ejecutar con permisos de administrador si es necesario
sudo python main.py  # Linux/macOS
```

### Logs y Depuración
La aplicación muestra mensajes informativos en la consola:
- `✅` - Operaciones exitosas
- `⚠️` - Advertencias
- `❌` - Errores

## 🔧 Desarrollo

### Estructura Modular
El proyecto está organizado en módulos independientes para facilitar el mantenimiento:

- **core/**: Lógica de compresión y manejo de formatos
- **gui/**: Interfaz gráfica de usuario
- **utils/**: Utilidades (temas, configuración, historial, iconos)

### Añadir Nuevos Formatos
1. Editar `core/format_handler.py`
2. Añadir soporte en `SUPPORTED_FORMATS`
3. Implementar encoder/decoder específico
4. Actualizar documentación

### Personalizar Temas
1. Editar `utils/theme_manager.py`
2. Añadir nuevos temas en el diccionario `themes`
3. Definir colores y estilos

## 📄 Licencia

Este proyecto es de código abierto. Puedes usarlo, modificarlo y distribuirlo libremente.

## 🤝 Contribuciones

Las contribuciones son bienvenidas:
1. Fork del proyecto
2. Crear rama para nueva funcionalidad
3. Commit de cambios
4. Push a la rama
5. Crear Pull Request

## 📞 Soporte

Para reportar problemas o solicitar funcionalidades:
- Crear issue en el repositorio
- Incluir información del sistema
- Describir pasos para reproducir el problema

---

**🎨 Compresor Avanzado de Imágenes v9.0** - Herramienta profesional para todas tus necesidades de compresión de imágenes.

