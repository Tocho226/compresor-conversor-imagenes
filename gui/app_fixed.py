#!/usr/bin/env python3
"""
ImageCompressorApp - Interfaz gráfica principal
Aplicación GUI moderna con todas las funcionalidades integradas
VERSIÓN CORREGIDA: Cambio de tema automático sin reinicio
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading
from typing import List, Optional, Tuple

# Imports de módulos locales
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.compression_engine import CompressionEngine
from core.format_handler import FormatHandler
from utils.theme_manager import ThemeManager
from utils.config_manager import ConfigManager
from utils.history_manager import HistoryManager
from utils.icon_manager import IconManager

class ImageCompressorApp:
    """Aplicación principal del compresor de imágenes."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.selected_images = []
        self.compression_thread = None
        self.is_compressing = False
        
        # Inicializar managers
        self.theme = ThemeManager()
        self.config = ConfigManager()
        self.history = HistoryManager()
        self.icons = IconManager()
        self.compression_engine = CompressionEngine()
        
        # Lista para mantener referencias a todos los widgets que necesitan actualización
        self.widgets_to_update = []
        
        # Configurar aplicación
        self.setup_window()
        self.setup_variables()
        self.create_gui()
        self.setup_drag_drop()
        self.setup_shortcuts()
        self.load_user_settings()
        
        print("✅ Aplicación iniciada correctamente")
    
    def setup_window(self):
        """Configura la ventana principal."""
        self.root.title("Compresor Avanzado de Imágenes v9.1")
        self.root.geometry(self.config.get("window_geometry", "1200x800"))
        self.root.minsize(800, 600)
        
        # Configurar icono
        self.icons.set_window_icon(self.root)
        
        # Configurar tema
        theme_name = self.config.get("theme", "modern_light")
        self.theme.set_theme(theme_name)
        
        # Configurar grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Aplicar colores de tema
        self.root.configure(bg=self.theme.get_color("bg_primary"))
    
    def setup_variables(self):
        """Configura variables de tkinter."""
        self.quality_var = tk.IntVar(value=self.config.get("quality", 85))
        self.output_format_var = tk.StringVar(value=self.config.get("output_format", ".jpg"))
        self.maintain_aspect_var = tk.BooleanVar(value=self.config.get("maintain_aspect", True))
        self.width_var = tk.StringVar(value="")
        self.height_var = tk.StringVar(value="")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Listo para comprimir imágenes")
    
    def create_gui(self):
        """Crea la interfaz gráfica completa."""
        # Frame principal
        self.main_frame = tk.Frame(self.root, **self.theme.get_frame_style("primary"))
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.widgets_to_update.append(("frame", self.main_frame, "primary"))
        
        # Header con banner
        self.create_header(self.main_frame)
        
        # Contenido principal
        self.content_frame = tk.Frame(self.main_frame, **self.theme.get_frame_style("primary"))
        self.content_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.widgets_to_update.append(("frame", self.content_frame, "primary"))
        
        # Panel izquierdo - Controles
        self.create_controls_panel(self.content_frame)
        
        # Panel derecho - Vista previa + historial
        self.create_preview_panel(self.content_frame)
        
        # Footer con progreso
        self.create_footer(self.main_frame)
    
    def create_header(self, parent):
        """Crea el header con banner y controles principales."""
        header_frame = tk.Frame(parent, **self.theme.get_frame_style("secondary"))
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        self.widgets_to_update.append(("frame", header_frame, "secondary"))
        
        # Banner con degradado y título superpuesto
        banner_container = tk.Frame(header_frame, **self.theme.get_frame_style("primary"))
        banner_container.grid(row=0, column=0, sticky="ew")
        banner_container.grid_rowconfigure(0, weight=1)
        banner_container.grid_columnconfigure(0, weight=1)
        self.widgets_to_update.append(("frame", banner_container, "primary"))
        
        # Banner con degradado (si está disponible)
        banner_gradient = self.icons.get_gradient("banner")
        if banner_gradient:
            self.banner_label = tk.Label(banner_container, image=banner_gradient, 
                                  **self.theme.get_label_style("primary"))
            self.banner_label.grid(row=0, column=0, sticky="ew")
            self.widgets_to_update.append(("label", self.banner_label, "primary"))
        
        # Título superpuesto sobre el banner
        style_title1 = self.theme.get_label_style("title").copy()
        style_title1["font"] = ("Arial", 20, "bold")
        # Para que el fondo sea transparente y se vea el banner
        style_title1["bg"] = ""
        self.title_label = tk.Label(banner_container, text="🎨 Compresor Avanzado de Imágenes v9.1", **style_title1)
        self.title_label.grid(row=0, column=0, pady=15)
        self.widgets_to_update.append(("label", self.title_label, "title"))
        
        # Frame para botones
        button_frame = tk.Frame(header_frame, **self.theme.get_frame_style("primary"))
        button_frame.grid(row=1, column=0, sticky="ew", pady=10)
        self.widgets_to_update.append(("frame", button_frame, "primary"))
        
        # Botón de tema
        self.theme_button = self.icons.create_button_with_icon(
            button_frame, "Cambiar Tema", "theme",
            command=self.toggle_theme,
            **self.theme.get_button_style("secondary")
        )
        self.theme_button.pack(side=tk.RIGHT, padx=20)
        self.widgets_to_update.append(("button", self.theme_button, "secondary"))
        
        # Botón de ayuda
        self.help_button = self.icons.create_button_with_icon(
            button_frame, "Ayuda (F1)", "help",
            command=self.show_help,
            **self.theme.get_button_style("secondary")
        )
        self.help_button.pack(side=tk.RIGHT, padx=(0, 10))
        self.widgets_to_update.append(("button", self.help_button, "secondary"))
    
    def create_controls_panel(self, parent):
        """Crea el panel de controles."""
        self.controls_frame = tk.Frame(parent, **self.theme.get_frame_style("card"))
        self.controls_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.widgets_to_update.append(("frame", self.controls_frame, "card"))
        
        # Título del panel
        style_title2 = self.theme.get_label_style("subtitle").copy()
        style_title2["font"] = ("Arial", 16, "bold")
        self.controls_title_label = tk.Label(self.controls_frame, text="⚙️ Configuración", **style_title2)
        self.controls_title_label.pack(pady=10)
        self.widgets_to_update.append(("label", self.controls_title_label, "subtitle"))
        
        # Selección de archivos
        self.create_file_selection(self.controls_frame)
        
        # Configuración de compresión
        self.create_compression_settings(self.controls_frame)
        
        # Botones de acción
        self.create_action_buttons(self.controls_frame)
    
    def create_file_selection(self, parent):
        """Crea la sección de selección de archivos."""
        style_title3 = self.theme.get_frame_style("secondary").copy()
        style_title3["font"] = ("Arial", 12, "bold")
        # Usar el color de texto correcto para el LabelFrame
        style_title3["fg"] = self.theme.get_color("text_primary")

        self.file_frame = tk.LabelFrame(
            parent,
            text="📁 Selección de Archivos", **style_title3
        )
        self.file_frame.pack(fill="x", padx=10, pady=5)
        self.widgets_to_update.append(("labelframe", self.file_frame, "secondary"))
        
        # Área de drag & drop
        self.drop_area = tk.Frame(self.file_frame, 
                                 bg=self.theme.get_color("canvas_bg"),
                                 relief="solid", borderwidth=2,
                                 highlightbackground=self.theme.get_color("border_accent"))
        self.drop_area.pack(fill="x", padx=10, pady=10, ipady=20)
        self.widgets_to_update.append(("canvas", self.drop_area, None))

        # Tomamos el estilo del tema
        style = self.theme.get_label_style("secondary").copy()
        style["font"] = ("Arial", 16)

        self.drop_label = tk.Label(
            self.drop_area,
            text="🖼️ Arrastra imágenes aquí o haz clic para seleccionar ",
            **style
        )
        self.drop_label.pack(pady=20, expand=True)
        self.widgets_to_update.append(("label", self.drop_label, "secondary"))
        
        # Bind click event
        self.drop_area.bind("<Button-1>", lambda e: self.select_images())
        self.drop_label.bind("<Button-1>", lambda e: self.select_images())
        
        # Lista de archivos seleccionados
        self.file_listbox = tk.Listbox(self.file_frame, height=6,
                                      bg=self.theme.get_color("bg_primary"),
                                      fg=self.theme.get_color("text_primary"),
                                      selectbackground=self.theme.get_color("accent_primary"))
        self.file_listbox.pack(fill="x", padx=10, pady=(0, 10))
        self.widgets_to_update.append(("listbox", self.file_listbox, None))
        
        # Botones de gestión de archivos
        file_buttons_frame = tk.Frame(self.file_frame, **self.theme.get_frame_style("primary"))
        file_buttons_frame.pack(fill="x", padx=10, pady=(0, 5))
        self.widgets_to_update.append(("frame", file_buttons_frame, "primary"))

        self.select_btn = self.icons.create_button_with_icon(
            file_buttons_frame, "Seleccionar", "folder",
            command=self.select_images,
            **self.theme.get_button_style("primary")
        )
        self.select_btn.pack(side=tk.LEFT, padx=(0, 5))
        self.widgets_to_update.append(("button", self.select_btn, "primary"))

        self.clear_btn = self.icons.create_button_with_icon(
            file_buttons_frame, "Limpiar", "clear",
            command=self.clear_selection,
            **self.theme.get_button_style("secondary")
        )
        self.clear_btn.pack(side=tk.LEFT)
        self.widgets_to_update.append(("button", self.clear_btn, "secondary"))

        self.file_info_label = tk.Label(
            file_buttons_frame,
            text="0 archivos | 0 MB",
            **self.theme.get_label_style("secondary")
        )
        self.file_info_label.pack(side=tk.RIGHT, padx=5)
        self.widgets_to_update.append(("label", self.file_info_label, "secondary"))

    
    def create_compression_settings(self, parent):
        """Crea la sección de configuración de compresión."""
        style_settings = self.theme.get_frame_style("secondary").copy()
        style_settings["font"] = ("Arial", 12, "bold")
        style_settings["fg"] = self.theme.get_color("text_primary")
        
        self.settings_frame = tk.LabelFrame(parent, text="🔧 Configuración de Compresión",
                                      **style_settings)
        self.settings_frame.pack(fill="x", padx=10, pady=5)
        self.widgets_to_update.append(("labelframe", self.settings_frame, "secondary"))
        
        # Calidad
        quality_frame = tk.Frame(self.settings_frame, **self.theme.get_frame_style("primary"))
        quality_frame.pack(fill="x", padx=10, pady=5)
        self.widgets_to_update.append(("frame", quality_frame, "primary"))
        
        self.quality_label = tk.Label(quality_frame, text="Calidad:", **self.theme.get_label_style("primary"))
        self.quality_label.pack(side=tk.LEFT)
        self.widgets_to_update.append(("label", self.quality_label, "primary"))
        
        self.quality_scale = tk.Scale(quality_frame, from_=10, to=100, orient=tk.HORIZONTAL,
                                     variable=self.quality_var, command=self.update_quality_label,
                                     bg=self.theme.get_color("bg_primary"),
                                     fg=self.theme.get_color("text_primary"),
                                     highlightbackground=self.theme.get_color("accent_primary"))
        self.quality_scale.pack(side=tk.LEFT, fill="x", expand=True, padx=10)
        self.widgets_to_update.append(("scale", self.quality_scale, None))
        
        self.quality_value_label = tk.Label(quality_frame, text="85%", 
                                           **self.theme.get_label_style("primary"))
        self.quality_value_label.pack(side=tk.RIGHT)
        self.widgets_to_update.append(("label", self.quality_value_label, "primary"))
        
        # Formato de salida
        format_frame = tk.Frame(self.settings_frame, **self.theme.get_frame_style("primary"))
        format_frame.pack(fill="x", padx=10, pady=5)
        self.widgets_to_update.append(("frame", format_frame, "primary"))
        
        self.format_label = tk.Label(format_frame, text="Formato:", **self.theme.get_label_style("primary"))
        self.format_label.pack(side=tk.LEFT)
        self.widgets_to_update.append(("label", self.format_label, "primary"))
        
        format_combo = ttk.Combobox(format_frame, textvariable=self.output_format_var,
                                   values=FormatHandler.SUPPORTED_FORMATS, state="readonly")
        format_combo.pack(side=tk.LEFT, fill="x", expand=True, padx=10)
        
        # Redimensionado
        style_resize = self.theme.get_frame_style("primary").copy()
        style_resize["font"] = ("Arial", 11, "bold")
        style_resize["fg"] = self.theme.get_color("text_primary")
        
        self.resize_frame = tk.LabelFrame(self.settings_frame, text="📏 Redimensionar",
                                    **style_resize)
        self.resize_frame.pack(fill="x", padx=10, pady=5)
        self.widgets_to_update.append(("labelframe", self.resize_frame, "primary"))
        
        size_frame = tk.Frame(self.resize_frame, **self.theme.get_frame_style("primary"))
        size_frame.pack(fill="x", padx=5, pady=5)
        self.widgets_to_update.append(("frame", size_frame, "primary"))
        
        self.width_label = tk.Label(size_frame, text="Ancho:", **self.theme.get_label_style("primary"))
        self.width_label.pack(side=tk.LEFT)
        self.widgets_to_update.append(("label", self.width_label, "primary"))
        
        width_entry = tk.Entry(size_frame, textvariable=self.width_var, width=8)
        width_entry.pack(side=tk.LEFT, padx=5)
        
        self.height_label = tk.Label(size_frame, text="Alto:", **self.theme.get_label_style("primary"))
        self.height_label.pack(side=tk.LEFT, padx=(10, 0))
        self.widgets_to_update.append(("label", self.height_label, "primary"))
        
        height_entry = tk.Entry(size_frame, textvariable=self.height_var, width=8)
        height_entry.pack(side=tk.LEFT, padx=5)
        
        self.aspect_check = tk.Checkbutton(self.resize_frame, text="Mantener aspecto",
                                     variable=self.maintain_aspect_var,
                                     **self.theme.get_label_style("primary"))
        self.aspect_check.pack(anchor="w", padx=5, pady=5)
        self.widgets_to_update.append(("checkbutton", self.aspect_check, "primary"))
    
    def create_action_buttons(self, parent):
        """Crea los botones de acción principales."""
        action_frame = tk.Frame(parent, **self.theme.get_frame_style("primary"))
        action_frame.pack(fill="x", padx=10, pady=10)
        self.widgets_to_update.append(("frame", action_frame, "primary"))
        
        # Botón principal de compresión
        self.compress_button = self.icons.create_button_with_icon(
            action_frame, "Comprimir Imágenes (Ctrl+S)", "compression",
            command=self.start_compression,
            **self.theme.get_button_style("success")
        )
        self.compress_button.pack(fill="x", pady=5)
        self.widgets_to_update.append(("button", self.compress_button, "success"))
        
        # Botones secundarios
        secondary_frame = tk.Frame(action_frame, **self.theme.get_frame_style("primary"))
        secondary_frame.pack(fill="x", pady=5)
        self.widgets_to_update.append(("frame", secondary_frame, "primary"))
        
        self.export_btn = self.icons.create_button_with_icon(
            secondary_frame, "Exportar Historial", "export",
            command=self.export_history,
            **self.theme.get_button_style("secondary")
        )
        self.export_btn.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 2))
        self.widgets_to_update.append(("button", self.export_btn, "secondary"))
        
        # Nuevo botón: Limpiar Historial
        self.clear_history_btn = self.icons.create_button_with_icon(
            action_frame, "Limpiar Historial", "clear",
            command=self.clear_history,
            **self.theme.get_button_style("danger")
        )
        self.clear_history_btn.pack(fill="x", pady=(5, 0))
        self.widgets_to_update.append(("button", self.clear_history_btn, "danger"))
        
        self.settings_btn = self.icons.create_button_with_icon(
            secondary_frame, "Configuración", "settings",
            command=self.show_settings,
            **self.theme.get_button_style("secondary")
        )
        self.settings_btn.pack(side=tk.RIGHT, fill="x", expand=True, padx=(2, 0))
        self.widgets_to_update.append(("button", self.settings_btn, "secondary"))

    
    def create_history_section(self, parent):
        """Crea la sección de historial."""
        style_history = self.theme.get_frame_style("secondary").copy()
        style_history["font"] = ("Arial", 12, "bold")
        style_history["fg"] = self.theme.get_color("text_primary")
        
        self.history_frame = tk.LabelFrame(parent, text="📋 Historial Reciente",
                                     **style_history)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.widgets_to_update.append(("labelframe", self.history_frame, "secondary"))
        
        # Lista de historial
        self.history_listbox = tk.Listbox(self.history_frame, height=8,
                                         bg=self.theme.get_color("bg_primary"),
                                         fg=self.theme.get_color("text_primary"),
                                         selectbackground=self.theme.get_color("accent_primary"))
        self.history_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.history_listbox.bind("<Double-Button-1>", self.load_from_history)
        self.widgets_to_update.append(("listbox", self.history_listbox, None))
        
        # Actualizar historial
        self.update_history_display()
    
    def create_preview_panel(self, parent):
        """Crea el panel de vista previa."""
        self.preview_frame = tk.Frame(parent, **self.theme.get_frame_style("card"))
        self.preview_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        self.widgets_to_update.append(("frame", self.preview_frame, "card"))
        
        # Título del panel
        self.preview_title_label = tk.Label(self.preview_frame, text="🖼️ Vista Previa",
                              **self.theme.get_label_style("subtitle"))
        self.preview_title_label.pack(pady=10)
        self.widgets_to_update.append(("label", self.preview_title_label, "subtitle"))
        
        # Canvas para vista previa
        canvas_frame = tk.Frame(self.preview_frame, **self.theme.get_frame_style("primary"))
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.widgets_to_update.append(("frame", canvas_frame, "primary"))
        
        # Vista previa antes/después
        preview_container = tk.Frame(canvas_frame, **self.theme.get_frame_style("primary"))
        preview_container.pack(fill="both", expand=True)
        self.widgets_to_update.append(("frame", preview_container, "primary"))
        
        # Antes
        before_frame = tk.Frame(preview_container, **self.theme.get_frame_style("secondary"))
        before_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 5))
        self.widgets_to_update.append(("frame", before_frame, "secondary"))
        
        self.before_label = tk.Label(before_frame, text="Antes", **self.theme.get_label_style("primary"))
        self.before_label.pack(pady=5)
        self.widgets_to_update.append(("label", self.before_label, "primary"))
        
        self.before_canvas = tk.Canvas(before_frame, width=280, height=280,
                                      bg=self.theme.get_color("canvas_bg"),
                                      highlightthickness=1,
                                      highlightbackground=self.theme.get_color("border_primary"))
        self.before_canvas.pack(padx=5, pady=5)
        self.widgets_to_update.append(("canvas", self.before_canvas, None))
        
        # Después
        after_frame = tk.Frame(preview_container, **self.theme.get_frame_style("secondary"))
        after_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=(5, 0))
        self.widgets_to_update.append(("frame", after_frame, "secondary"))
        
        self.after_label = tk.Label(after_frame, text="Después", **self.theme.get_label_style("primary"))
        self.after_label.pack(pady=5)
        self.widgets_to_update.append(("label", self.after_label, "primary"))
        
        self.after_canvas = tk.Canvas(after_frame, width=280, height=280,
                                     bg=self.theme.get_color("canvas_bg"),
                                     highlightthickness=1,
                                     highlightbackground=self.theme.get_color("border_primary"))
        self.after_canvas.pack(padx=5, pady=5)
        self.widgets_to_update.append(("canvas", self.after_canvas, None))
        
        # Información de la imagen
        self.info_label = tk.Label(self.preview_frame, text="Selecciona imágenes para ver información",
                                  **self.theme.get_label_style("secondary"))
        self.info_label.pack(pady=10)
        self.widgets_to_update.append(("label", self.info_label, "secondary"))

        # Historial debajo de Vista Previa
        self.create_history_section(self.preview_frame)
        # Bind de un clic para previsualizar antes/después desde historial
        self.history_listbox.bind("<<ListboxSelect>>", self.preview_from_history_single_click)
        # Doble clic para detalles completos de la conversión
        self.history_listbox.bind("<Double-Button-1>", self.load_from_history)

    
    def create_footer(self, parent):
        """Crea el footer con barra de progreso."""
        self.footer_frame = tk.Frame(parent, **self.theme.get_frame_style("secondary"))
        self.footer_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        self.footer_frame.grid_columnconfigure(0, weight=1)
        self.widgets_to_update.append(("frame", self.footer_frame, "secondary"))
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(self.footer_frame, variable=self.progress_var,
                                           maximum=100, mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        # Estado
        self.status_label = tk.Label(self.footer_frame, textvariable=self.status_var,
                                    **self.theme.get_label_style("secondary"))
        self.status_label.grid(row=1, column=0, pady=(0, 5))
        self.widgets_to_update.append(("label", self.status_label, "secondary"))
    
    def apply_theme_to_all_widgets(self):
        """Aplica el tema actual a todos los widgets registrados."""
        # Actualizar ventana principal
        self.root.configure(bg=self.theme.get_color("bg_primary"))
        
        # Actualizar todos los widgets registrados
        for widget_info in self.widgets_to_update:
            widget_type, widget, style_type = widget_info
            
            try:
                if widget_type == "frame":
                    style = self.theme.get_frame_style(style_type)
                    widget.configure(**style)
                    
                elif widget_type == "label":
                    style = self.theme.get_label_style(style_type)
                    widget.configure(**style)
                    
                elif widget_type == "button":
                    style = self.theme.get_button_style(style_type)
                    widget.configure(**style)
                    
                elif widget_type == "labelframe":
                    style = self.theme.get_frame_style(style_type).copy()
                    style["fg"] = self.theme.get_color("text_primary")
                    widget.configure(**style)
                    
                elif widget_type == "listbox":
                    widget.configure(
                        bg=self.theme.get_color("bg_primary"),
                        fg=self.theme.get_color("text_primary"),
                        selectbackground=self.theme.get_color("accent_primary")
                    )
                    
                elif widget_type == "canvas":
                    if widget == self.drop_area:
                        widget.configure(
                            bg=self.theme.get_color("canvas_bg"),
                            highlightbackground=self.theme.get_color("border_accent")
                        )
                    else:
                        widget.configure(
                            bg=self.theme.get_color("canvas_bg"),
                            highlightbackground=self.theme.get_color("border_primary")
                        )
                        
                elif widget_type == "scale":
                    widget.configure(
                        bg=self.theme.get_color("bg_primary"),
                        fg=self.theme.get_color("text_primary"),
                        highlightbackground=self.theme.get_color("accent_primary")
                    )
                    
                elif widget_type == "checkbutton":
                    style = self.theme.get_label_style("primary")
                    widget.configure(**style)
                    
            except Exception as e:
                print(f"⚠️ Error aplicando tema a widget {widget_type}: {e}")
        
        # Actualizar el título superpuesto
        if hasattr(self, 'title_label'):
            # El título debe tener un fondo que coincida con el banner o transparente
            style_title = self.theme.get_label_style("title").copy()
            style_title["font"] = ("Arial", 20, "bold")
            # Intentar hacer el fondo transparente o del color del banner
            try:
                self.title_label.configure(fg=style_title["fg"])
            except:
                pass
    
    def setup_drag_drop(self):
        """Configura drag & drop con implementación mejorada."""
        try:
            from .drag_drop_fix import setup_drag_drop_for_widget
            
            # Configurar drag & drop mejorado
            self.drag_drop_handler = setup_drag_drop_for_widget(
                self.drop_area, 
                self.handle_dropped_files
            )
            
            print("✅ Drag & drop mejorado configurado")
        except ImportError:
            print("⚠️ Módulo drag_drop_fix no disponible, usando método básico")
            # Configurar método básico
            self.drop_area.bind("<Button-1>", lambda e: self.select_images())
    
    def setup_shortcuts(self):
        """Configura atajos de teclado."""
        self.root.bind("<Control-o>", lambda e: self.select_images())
        self.root.bind("<Control-s>", lambda e: self.start_compression())
        self.root.bind("<F1>", lambda e: self.show_help())
        self.root.bind("<Control-q>", lambda e: self.on_closing())
        
        # Configurar protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_user_settings(self):
        """Carga configuraciones guardadas del usuario."""
        # Cargar valores de configuración
        self.quality_var.set(self.config.get("quality", 85))
        self.output_format_var.set(self.config.get("output_format", ".jpg"))
        self.maintain_aspect_var.set(self.config.get("maintain_aspect", True))
    
    def select_images(self):
        """Abre diálogo para seleccionar imágenes."""
        file_paths = filedialog.askopenfilenames(
            title="Seleccionar imágenes",
            filetypes=[
                ("Imágenes", " ".join(f"*{fmt}" for fmt in FormatHandler.SUPPORTED_FORMATS)),
                ("Todos los archivos", "*.*")
            ],
            initialdir=self.config.get("last_input_dir", "")
        )
        
        if file_paths:
            self.selected_images = list(file_paths)
            self.config.set("last_input_dir", os.path.dirname(file_paths[0]))
            self.update_file_list()
            self.update_preview()
            self.status_var.set(f"Cargadas {len(file_paths)} imágenes")
    
    def handle_dropped_files(self, files):
        """Maneja archivos arrastrados y soltados."""
        image_files = []
        
        for file_path in files:
            # Limpiar path
            file_path = file_path.strip('{}')
            
            # Verificar si es imagen
            ext = os.path.splitext(file_path)[1].lower()
            if ext in FormatHandler.SUPPORTED_FORMATS:
                image_files.append(file_path)
        
        if image_files:
            self.selected_images = image_files
            self.update_file_list()
            self.update_preview()
            self.status_var.set(f"Cargadas {len(image_files)} imágenes")
        else:
            messagebox.showwarning("Sin imágenes", "No se encontraron imágenes válidas.")
    
    def clear_selection(self):
        """Limpia la selección de imágenes."""
        self.selected_images = []
        self.file_listbox.delete(0, tk.END)
        self.before_canvas.delete("all")
        self.after_canvas.delete("all")
        self.info_label.config(text="Selecciona imágenes para ver información")
        self.file_info_label.config(text="0 archivos | 0 MB")
        self.status_var.set("Listo para comprimir imágenes")
    
    def update_file_list(self):
        """Actualiza la lista de archivos seleccionados."""
        self.file_listbox.delete(0, tk.END)
        total_size = 0
        
        for file_path in self.selected_images:
            filename = os.path.basename(file_path)
            try:
                size = os.path.getsize(file_path)
                total_size += size
                size_mb = round(size / (1024 * 1024), 2)
                self.file_listbox.insert(tk.END, f"{filename} ({size_mb} MB)")
            except:
                self.file_listbox.insert(tk.END, filename)
        
        # Actualizar info label
        total_mb = round(total_size / (1024 * 1024), 2)
        self.file_info_label.config(text=f"{len(self.selected_images)} archivos | {total_mb} MB")
    
    def update_preview(self):
        """Actualiza la vista previa de la primera imagen seleccionada."""
        if not self.selected_images:
            return
        
        try:
            first_image = self.selected_images[0]
            with Image.open(first_image) as img:
                # Crear thumbnail
                img.thumbnail((280, 280), Image.Resampling.LANCZOS)
                
                # Guardar referencia para evitar garbage collection
                self.before_image = ImageTk.PhotoImage(img)
                
                # Limpiar canvas
                self.before_canvas.delete("all")
                
                # Centrar imagen
                canvas_width = self.before_canvas.winfo_width() or 280
                canvas_height = self.before_canvas.winfo_height() or 280
                x = (canvas_width - img.width) // 2
                y = (canvas_height - img.height) // 2
                
                # Mostrar imagen
                self.before_canvas.create_image(x, y, anchor=tk.NW, image=self.before_image)
                
                # Actualizar info
                size = os.path.getsize(first_image)
                size_mb = round(size / (1024 * 1024), 2)
                self.info_label.config(
                    text=f"📊 {img.width}x{img.height} px | {size_mb} MB | {img.format}"
                )
        except Exception as e:
            print(f"❌ Error actualizando preview: {e}")
            self.info_label.config(text="Error cargando vista previa")
    
    def update_quality_label(self, value):
        """Actualiza el label de calidad."""
        if hasattr(self, 'quality_value_label'):
            self.quality_value_label.config(text=f"{int(float(value))}%")
    
    def toggle_theme(self):
        """Alterna entre tema claro y oscuro CON ACTUALIZACIÓN AUTOMÁTICA."""
        new_theme = self.theme.toggle_theme()
        self.config.set("theme", new_theme)
        
        # Aplicar el nuevo tema a todos los widgets inmediatamente
        self.apply_theme_to_all_widgets()
        
        # Mostrar mensaje de confirmación
        theme_name = 'oscuro' if 'dark' in new_theme else 'claro'
        self.status_var.set(f"Tema cambiado a {theme_name}")
    
    def start_compression(self):
        """Inicia el proceso de compresión."""
        if not self.selected_images:
            messagebox.showwarning("Sin imágenes", "Selecciona al menos una imagen para comprimir.")
            return
        
        if self.is_compressing:
            messagebox.showinfo("En progreso", "Ya hay una compresión en progreso.")
            return
        
        # Seleccionar directorio de salida
        output_dir = filedialog.askdirectory(
            title="Seleccionar carpeta de destino",
            initialdir=self.config.get("last_output_dir", "")
        )
        
        if not output_dir:
            return
        
        # Guardar directorio
        self.config.set("last_output_dir", output_dir)
        
        # Guardar configuración
        self.config.set("quality", self.quality_var.get())
        self.config.set("output_format", self.output_format_var.get())
        self.config.set("maintain_aspect", self.maintain_aspect_var.get())
        
        # Preparar parámetros
        params = {
            "quality": self.quality_var.get(),
            "output_format": self.output_format_var.get(),
            "maintain_aspect": self.maintain_aspect_var.get()
        }
        
        # Añadir dimensiones si están especificadas
        if self.width_var.get():
            try:
                params["target_width"] = int(self.width_var.get())
            except ValueError:
                pass
        
        if self.height_var.get():
            try:
                params["target_height"] = int(self.height_var.get())
            except ValueError:
                pass
        
        # Iniciar compresión en thread separado
        self.is_compressing = True
        self.compress_button.config(state="disabled", text="Comprimiendo...")
        self.status_var.set("Iniciando compresión...")
        
        self.compression_thread = threading.Thread(
            target=self._compress_images_thread,
            args=(self.selected_images, output_dir, params),
            daemon=True
        )
        self.compression_thread.start()
    
    def _compress_images_thread(self, images: List[str], output_dir: str, params: dict):
        """Thread de compresión de imágenes."""
        try:
            results = []
            total = len(images)
            
            for i, image_path in enumerate(images):
                # Actualizar progreso
                progress = ((i + 1) / total) * 100
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                self.root.after(0, lambda i=i, t=total: 
                              self.status_var.set(f"Comprimiendo imagen {i+1} de {t}..."))
                
                # Actualizar preview "Antes" en tiempo real
                self.root.after(0, lambda path=image_path: self.update_before_preview(path))
                
                # Comprimir imagen
                result = self.compression_engine.compress_image(
                    image_path, output_dir, **params
                )
                results.append(result)
                
                # Actualizar preview "Después" en tiempo real
                if result["success"] and result.get("output_path"):
                    self.root.after(0, lambda path=result["output_path"]: 
                                  self.update_preview_after_compression(path))
            
            # Procesar resultados
            successful = sum(1 for r in results if r["success"])
            failed = len(results) - successful
            
            # Añadir al historial
            for i, result in enumerate(results):
                if i < len(self.selected_images):
                    self.history.add_entry(result, self.selected_images[i])
            
            # Mostrar resultado final
            self.root.after(0, lambda: self._show_compression_results(successful, failed, results))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error durante la compresión: {e}"))
        
        finally:
            # Restaurar interfaz
            self.root.after(0, self._compression_finished)
    
    def update_preview_after_compression(self, output_path: str):
        """Actualiza la vista previa después de comprimir una imagen."""
        try:
            if os.path.exists(output_path):
                with Image.open(output_path) as img:
                    img.thumbnail((280, 280), Image.Resampling.LANCZOS)
                    
                    self.after_image = ImageTk.PhotoImage(img)
                    self.after_canvas.delete("all")
                    
                    # Centrar imagen
                    canvas_width = self.after_canvas.winfo_width() or 280
                    canvas_height = self.after_canvas.winfo_height() or 280
                    x = (canvas_width - img.width) // 2
                    y = (canvas_height - img.height) // 2
                    
                    self.after_canvas.create_image(x, y, anchor=tk.NW, image=self.after_image)
        except Exception as e:
            print(f"❌ Error actualizando preview: {e}")

    def update_before_preview(self, input_path: str):
        """Pinta la imagen original (antes) mientras se procesa."""
        try:
            if os.path.exists(input_path):
                with Image.open(input_path) as img:
                    img.thumbnail((280, 280), Image.Resampling.LANCZOS)
                    self.before_image = ImageTk.PhotoImage(img)
                    self.before_canvas.delete("all")
                    cw = self.before_canvas.winfo_width() or 280
                    ch = self.before_canvas.winfo_height() or 280
                    x = (cw - img.width) // 2
                    y = (ch - img.height) // 2
                    self.before_canvas.create_image(x, y, anchor=tk.NW, image=self.before_image)
        except Exception as e:
            print(f"❌ Error actualizando preview 'Antes': {e}")

    
    def _show_compression_results(self, successful: int, failed: int, results: list):
        """Muestra los resultados de la compresión."""
        if successful > 0:
            total_saved = sum(r.get("original_size", 0) - r.get("compressed_size", 0) 
                            for r in results if r["success"])
            saved_mb = round(total_saved / (1024 * 1024), 2)
            
            message = f"✅ Compresión completada!\n\n"
            message += f"📊 Imágenes procesadas: {successful}\n"
            if failed > 0:
                message += f"❌ Errores: {failed}\n"
            message += f"💾 Espacio ahorrado: {saved_mb} MB"
            
            messagebox.showinfo("Compresión Completada", message)
        else:
            messagebox.showerror("Error", "No se pudo comprimir ninguna imagen.")
        
        # Actualizar historial
        self.update_history_display()
    
    def _compression_finished(self):
        """Restaura la interfaz después de la compresión."""
        self.is_compressing = False
        self.compress_button.config(state="normal", text="Comprimir Imágenes (Ctrl+S)")
        self.progress_var.set(0)
        self.status_var.set("Compresión completada")
    
    def update_history_display(self):
        """Actualiza la visualización del historial (sin límite)."""
        if not hasattr(self, "history_listbox"):
            return
        self.history_listbox.delete(0, tk.END)

        # Obtener TODO el historial (sin recorte a 10)
        try:
            all_entries = self.history.get_history()
        except Exception:
            # Fallback por si la clase no expone get_history()
            all_entries = self.history.get_recent_entries(10**9)

        # Mostrar más recientes primero
        for entry in reversed(all_entries):
            filename = entry.get("input_filename", "Desconocido")
            format_name = entry.get("format", "")
            ratio = entry.get("compression_ratio", 0)
            status = "✅" if entry.get("success") else "❌"
            display_text = f"{status} {filename} → {format_name} ({ratio:.1f}%)"
            self.history_listbox.insert(tk.END, display_text)

    def clear_history(self):
        """Limpia el historial completo (memoria + interfaz)."""
        if messagebox.askyesno("Confirmar", "¿Seguro que quieres borrar TODO el historial?"):
            try:
                self.history.clear_history()  # Debe existir en tu HistoryManager
            except Exception as e:
                print(f"⚠️ No se pudo limpiar historial: {e}")
            self.update_history_display()
            messagebox.showinfo("Historial", "✅ Historial borrado correctamente.")
        
    def load_from_history(self, event):
        """Doble clic: muestra ventana con todos los detalles de la conversión."""
        selection = self.history_listbox.curselection()
        if not selection:
            return

        try:
            all_entries = self.history.get_history()
        except Exception:
            all_entries = self.history.get_recent_entries(10**9)

        index = selection[0]
        entry = list(reversed(all_entries))[index]

        # Construir info extendida (con fallbacks)
        orig_w, orig_h = (entry.get('original_dimensions') or [0, 0])[:2]
        comp_w, comp_h = (entry.get('compressed_dimensions') or entry.get('new_dimensions') or [0, 0])[:2]
        info = []
        info.append(f"📁 Archivo: {entry.get('input_filename', 'N/A')}")
        info.append(f"🗂️ Ruta origen: {entry.get('input_path', entry.get('source_path', 'N/A'))}")
        info.append(f"📦 Ruta salida: {entry.get('output_path', entry.get('dest_path', 'N/A'))}")
        info.append(f"📏 Dimensiones (origen): {orig_w}x{orig_h}")
        if comp_w and comp_h:
            info.append(f"📐 Dimensiones (resultado): {comp_w}x{comp_h}")
        info.append(f"💾 Tamaño original: {round(entry.get('original_size', 0)/(1024*1024), 2)} MB")
        info.append(f"🗜️ Tamaño comprimido: {round(entry.get('compressed_size', 0)/(1024*1024), 2)} MB")
        info.append(f"📉 Reducción: {entry.get('compression_ratio', 0):.1f}%")
        info.append(f"🎨 Formato destino: {entry.get('format', 'N/A')}")
        info.append(f"🧪 Calidad: {entry.get('quality', 'N/A')}")
        info.append(f"🔁 Mantener aspecto: {entry.get('maintain_aspect', 'N/A')}")
        info.append(f"📅 Fecha: {str(entry.get('timestamp', 'N/A'))[:19]}")
        info.append(f"✅ Éxito: {entry.get('success', False)}")
        if entry.get('error'):
            info.append(f"❗ Error: {entry.get('error')}")

        messagebox.showinfo("Detalles del Historial", "\n".join(info))

    def preview_from_history_single_click(self, event):
        """Un clic en historial: pinta en preview la imagen antes/después de esa conversión."""
        selection = self.history_listbox.curselection()
        if not selection:
            return

        # Obtener la misma lista que usa update_history_display (todo el historial)
        try:
            all_entries = self.history.get_history()
        except Exception:
            all_entries = self.history.get_recent_entries(10**9)

        # Recordatorio: en pantalla están en orden invertido (más recientes arriba)
        index = selection[0]
        entries_reversed = list(reversed(all_entries))
        if index >= len(entries_reversed):
            return

        entry = entries_reversed[index]
        input_path = entry.get("input_path") or entry.get("source_path") or entry.get("input_filename")
        output_path = entry.get("output_path") or entry.get("dest_path")

        # Pintar "Antes"
        if input_path and os.path.exists(input_path):
            try:
                with Image.open(input_path) as img:
                    img.thumbnail((280, 280), Image.Resampling.LANCZOS)
                    self.before_image = ImageTk.PhotoImage(img)
                    self.before_canvas.delete("all")
                    cw = self.before_canvas.winfo_width() or 280
                    ch = self.before_canvas.winfo_height() or 280
                    x = (cw - img.width) // 2
                    y = (ch - img.height) // 2
                    self.before_canvas.create_image(x, y, anchor=tk.NW, image=self.before_image)
            except Exception as e:
                print(f"⚠️ No se pudo cargar 'Antes' desde historial: {e}")

        # Pintar "Después"
        if output_path and os.path.exists(output_path):
            try:
                with Image.open(output_path) as img:
                    img.thumbnail((280, 280), Image.Resampling.LANCZOS)
                    self.after_image = ImageTk.PhotoImage(img)
                    self.after_canvas.delete("all")
                    cw = self.after_canvas.winfo_width() or 280
                    ch = self.after_canvas.winfo_height() or 280
                    x = (cw - img.width) // 2
                    y = (ch - img.height) // 2
                    self.after_canvas.create_image(x, y, anchor=tk.NW, image=self.after_image)
            except Exception as e:
                print(f"⚠️ No se pudo cargar 'Después' desde historial: {e}")
        
    
    def export_history(self):
        """Exporta el historial a CSV."""
        if not self.history.get_history():
            messagebox.showinfo("Historial vacío", "No hay entradas en el historial para exportar.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Exportar historial",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json")]
        )
        
        if file_path:
            if file_path.endswith('.csv'):
                success = self.history.export_to_csv(file_path)
            else:
                success = self.history.export_to_json(file_path)
            
            if success:
                messagebox.showinfo("Exportación exitosa", f"Historial exportado a:\n{file_path}")
            else:
                messagebox.showerror("Error", "No se pudo exportar el historial.")
    
    def show_settings(self):
        """Muestra ventana de configuración."""
        messagebox.showinfo("Configuración", "Ventana de configuración avanzada\n(Próximamente)")
    
    def show_help(self):
        """Muestra ayuda de la aplicación."""
        help_text = """🎨 Compresor Avanzado de Imágenes v9.1

📖 CÓMO USAR:
1. Arrastra imágenes al área designada o usa 'Seleccionar'
2. Configura calidad, formato y opciones
3. Haz clic en 'Comprimir Imágenes'
4. Selecciona carpeta de destino

⌨️ ATAJOS DE TECLADO:
• Ctrl+O: Seleccionar imágenes
• Ctrl+S: Comprimir imágenes
• F1: Mostrar esta ayuda
• Ctrl+Q: Salir

🎨 FORMATOS SOPORTADOS:
• Entrada: 30+ formatos (JPG, PNG, GIF, BMP, TIFF, WebP, AVIF, HEIC, SVG, PDF, PSD, etc.)
• Salida: Todos los formatos de entrada

✨ CARACTERÍSTICAS:
• Vista previa en tiempo real
• Historial persistente
• Temas claro/oscuro (cambio automático)
• Drag & drop funcional
• Control de archivos duplicados
• Soporte real para formatos especiales"""
        
        messagebox.showinfo("Ayuda - Compresor de Imágenes", help_text)
    
    # Eventos de drag & drop
    def on_drop(self, event):
        """Maneja el evento de soltar archivos."""
        try:
            files = event.data.split()
            image_files = []
            
            for file_path in files:
                # Limpiar path (remover {} si existen)
                file_path = file_path.strip('{}')
                
                # Verificar si es imagen
                ext = os.path.splitext(file_path)[1].lower()
                if ext in FormatHandler.SUPPORTED_FORMATS:
                    image_files.append(file_path)
            
            if image_files:
                self.selected_images = image_files
                self.update_file_list()
                self.update_preview()
                self.status_var.set(f"Cargadas {len(image_files)} imágenes")
            else:
                messagebox.showwarning("Sin imágenes", "No se encontraron imágenes válidas en los archivos soltados.")
                
        except Exception as e:
            print(f"❌ Error en drag & drop: {e}")
    
    def on_drag_enter(self, event):
        """Efecto visual al entrar en área de drop."""
        self.drop_area.configure(relief="raised", 
                                highlightbackground=self.theme.get_color("accent_secondary"))
    
    def on_drag_leave(self, event):
        """Efecto visual al salir del área de drop."""
        self.drop_area.configure(relief="solid",
                                highlightbackground=self.theme.get_color("border_accent"))
    
    def on_closing(self):
        """Maneja el cierre de la aplicación."""
        # Guardar geometría de ventana
        self.config.set("window_geometry", self.root.geometry())
        
        # Cerrar aplicación
        self.root.destroy()

# Configurar protocolo de cierre
def setup_app_closing(app):
    """Configura el manejo del cierre de la aplicación."""
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
