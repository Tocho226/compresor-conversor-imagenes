#!/usr/bin/env python3
"""
IconManager - Gestión de iconos y recursos visuales
Maneja iconos, degradados y elementos gráficos
"""

import os
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageDraw
from typing import Dict, Optional, Tuple

class IconManager:
    """Gestor de iconos con generación automática y fallback a emojis."""
    
    def __init__(self):
        self.icons = {}
        self.gradients = {}
        self.icon_size = 24
        self.load_icons()
        self.create_gradients()
    
    def load_icons(self) -> None:
        """Carga iconos desde archivos o crea fallbacks."""
        icon_files = {
            "app_main": "app_icon_main.png",
            "compression": "compression_icon.png", 
            "folder": "folder_icon.png",
            "settings": "settings_icon.png",
            "preview": "preview_icon.png"
        }
        
        loaded_count = 0
        
        for icon_name, filename in icon_files.items():
            try:
                if os.path.exists(filename):
                    # Cargar desde archivo
                    pil_image = Image.open(filename)
                    pil_image = pil_image.resize((self.icon_size, self.icon_size), Image.Resampling.LANCZOS)
                    self.icons[icon_name] = ImageTk.PhotoImage(pil_image)
                    loaded_count += 1
                else:
                    # Crear icono programático como fallback
                    self.icons[icon_name] = self._create_fallback_icon(icon_name)
            except Exception as e:
                print(f"⚠️ Error cargando {filename}: {e}")
                self.icons[icon_name] = self._create_fallback_icon(icon_name)
        
        print(f"✅ Iconos cargados: {loaded_count}/{len(icon_files)}")
    
    def create_gradients(self) -> None:
        """Crea degradados programáticos."""
        gradient_files = {
            "banner": "banner_moderno_degradado.png",
            "card_bg": "card_background_gradient.png",
            "button_primary": "button_gradient_primary.png",
            "accent": "accent_gradient_coral.png",
            "progress": "progress_bar_gradient.png"
        }
        
        loaded_count = 0
        
        for gradient_name, filename in gradient_files.items():
            try:
                if os.path.exists(filename):
                    # Cargar desde archivo
                    pil_image = Image.open(filename)
                    self.gradients[gradient_name] = ImageTk.PhotoImage(pil_image)
                    loaded_count += 1
                else:
                    # Crear degradado programático
                    self.gradients[gradient_name] = self._create_programmatic_gradient(gradient_name)
            except Exception as e:
                print(f"⚠️ Error cargando {filename}: {e}")
                self.gradients[gradient_name] = self._create_programmatic_gradient(gradient_name)
        
        print(f"✅ Degradados cargados: {loaded_count}/{len(gradient_files)}")
        if loaded_count < len(gradient_files):
            print("⚠️ Creando degradados programáticos...")
            print(f"✅ Degradados programáticos creados: {len(gradient_files) - loaded_count}/{len(gradient_files) - loaded_count}")
    
    def _create_fallback_icon(self, icon_name: str) -> ImageTk.PhotoImage:
        """Crea un icono programático como fallback."""
        try:
            # Crear imagen base
            img = Image.new('RGBA', (self.icon_size, self.icon_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Colores base
            primary_color = (102, 126, 234)  # #667eea
            secondary_color = (118, 75, 162)  # #764ba2
            
            if icon_name == "app_main":
                # Icono principal - círculo con degradado
                draw.ellipse([2, 2, self.icon_size-2, self.icon_size-2], 
                           fill=primary_color, outline=secondary_color, width=2)
                # Añadir símbolo de imagen
                center = self.icon_size // 2
                draw.rectangle([center-4, center-2, center+4, center+2], fill=(255, 255, 255))
                
            elif icon_name == "compression":
                # Icono de compresión - flechas convergentes
                draw.polygon([(4, 8), (8, 4), (8, 7), (16, 7), (16, 4), (20, 8), 
                             (16, 12), (16, 9), (8, 9), (8, 12)], fill=primary_color)
                draw.polygon([(4, 16), (8, 12), (8, 15), (16, 15), (16, 12), (20, 16), 
                             (16, 20), (16, 17), (8, 17), (8, 20)], fill=secondary_color)
                
            elif icon_name == "folder":
                # Icono de carpeta
                draw.rectangle([3, 8, 21, 19], fill=primary_color, outline=secondary_color)
                draw.polygon([(3, 8), (3, 6), (10, 6), (12, 8)], fill=secondary_color)
                
            elif icon_name == "settings":
                # Icono de configuración - engranaje
                center = self.icon_size // 2
                for i in range(8):
                    angle = i * 45
                    x = center + 8 * (1 if i % 2 == 0 else 0.7) * (1 if angle % 90 == 0 else 0.7)
                    y = center + 8 * (1 if i % 2 == 0 else 0.7) * (1 if (angle + 45) % 90 == 0 else 0.7)
                    draw.ellipse([x-1, y-1, x+1, y+1], fill=primary_color)
                draw.ellipse([center-4, center-4, center+4, center+4], 
                           fill=(255, 255, 255), outline=primary_color, width=2)
                
            elif icon_name == "preview":
                # Icono de vista previa - ojo
                draw.ellipse([4, 8, 20, 16], fill=primary_color, outline=secondary_color)
                draw.ellipse([10, 10, 14, 14], fill=(255, 255, 255))
                draw.ellipse([11, 11, 13, 13], fill=(0, 0, 0))
            
            return ImageTk.PhotoImage(img)
            
        except Exception as e:
            print(f"❌ Error creando icono fallback {icon_name}: {e}")
            # Crear icono básico como último recurso
            img = Image.new('RGBA', (self.icon_size, self.icon_size), primary_color)
            return ImageTk.PhotoImage(img)
    
    def _create_programmatic_gradient(self, gradient_name: str) -> ImageTk.PhotoImage:
        """Crea un degradado programático."""
        try:
            if gradient_name == "banner":
                # Banner horizontal azul-púrpura
                width, height = 800, 80
                img = Image.new('RGB', (width, height))
                draw = ImageDraw.Draw(img)
                
                for x in range(width):
                    # Interpolación de color
                    ratio = x / width
                    r = int(102 + (118 - 102) * ratio)  # 667eea -> 764ba2
                    g = int(126 + (75 - 126) * ratio)
                    b = int(234 + (162 - 234) * ratio)
                    draw.line([(x, 0), (x, height)], fill=(r, g, b))
                
            elif gradient_name == "card_bg":
                # Fondo de tarjeta sutil
                width, height = 400, 300
                img = Image.new('RGBA', (width, height), (255, 255, 255, 250))
                
            elif gradient_name == "button_primary":
                # Botón con degradado
                width, height = 120, 40
                img = Image.new('RGB', (width, height))
                draw = ImageDraw.Draw(img)
                
                for y in range(height):
                    ratio = y / height
                    r = int(102 + (90 - 102) * ratio)
                    g = int(126 + (110 - 126) * ratio)
                    b = int(234 + (200 - 234) * ratio)
                    draw.line([(0, y), (width, y)], fill=(r, g, b))
                
            elif gradient_name == "accent":
                # Acento rosa-coral
                width, height = 200, 50
                img = Image.new('RGB', (width, height))
                draw = ImageDraw.Draw(img)
                
                for x in range(width):
                    ratio = x / width
                    r = int(240 + (245 - 240) * ratio)  # f093fb -> f5576c
                    g = int(147 + (87 - 147) * ratio)
                    b = int(251 + (108 - 251) * ratio)
                    draw.line([(x, 0), (x, height)], fill=(r, g, b))
                
            elif gradient_name == "progress":
                # Barra de progreso
                width, height = 300, 20
                img = Image.new('RGB', (width, height))
                draw = ImageDraw.Draw(img)
                
                for x in range(width):
                    ratio = x / width
                    r = int(79 + (0 - 79) * ratio)      # 4facfe -> 00f2fe
                    g = int(172 + (242 - 172) * ratio)
                    b = int(254 + (254 - 254) * ratio)
                    draw.line([(x, 0), (x, height)], fill=(r, g, b))
            
            else:
                # Degradado por defecto
                width, height = 200, 100
                img = Image.new('RGB', (width, height), (102, 126, 234))
            
            return ImageTk.PhotoImage(img)
            
        except Exception as e:
            print(f"❌ Error creando degradado {gradient_name}: {e}")
            # Crear imagen sólida como fallback
            img = Image.new('RGB', (200, 100), (102, 126, 234))
            return ImageTk.PhotoImage(img)
    
    def get_icon(self, icon_name: str) -> Optional[PhotoImage]:
        """Obtiene un icono por nombre."""
        return self.icons.get(icon_name)
    
    def get_gradient(self, gradient_name: str) -> Optional[PhotoImage]:
        """Obtiene un degradado por nombre."""
        return self.gradients.get(gradient_name)
    
    def get_emoji_fallback(self, icon_name: str) -> str:
        """Obtiene emoji como fallback para iconos."""
        emoji_map = {
            "app_main": "🎨",
            "compression": "🧩", 
            "folder": "📁",
            "settings": "⚙️",
            "preview": "🖼️",
            "theme": "🌓",
            "help": "❓",
            "export": "📤",
            "import": "📥",
            "clear": "🗑️",
            "save": "💾",
            "open": "📂"
        }
        return emoji_map.get(icon_name, "📄")
    
    def create_button_with_icon(self, parent, text: str, icon_name: str, **kwargs) -> tk.Button:
        """Crea un botón con icono o emoji fallback."""
        icon = self.get_icon(icon_name)
        
        if icon:
            # Usar icono real
            return tk.Button(parent, text=f" {text}", image=icon, compound=tk.LEFT, **kwargs)
        else:
            # Usar emoji como fallback
            emoji = self.get_emoji_fallback(icon_name)
            return tk.Button(parent, text=f"{emoji} {text}", **kwargs)
    
    def set_window_icon(self, window: tk.Tk) -> None:
        """Establece el icono de la ventana."""
        try:
            icon = self.get_icon("app_main")
            if icon:
                window.iconphoto(True, icon)
                print("✅ Icono de ventana configurado")
            else:
                print("⚠️ Icono de ventana no disponible")
        except Exception as e:
            print(f"⚠️ Error configurando icono de ventana: {e}")
    
    def get_available_icons(self) -> list:
        """Obtiene lista de iconos disponibles."""
        return list(self.icons.keys())
    
    def get_available_gradients(self) -> list:
        """Obtiene lista de degradados disponibles."""
        return list(self.gradients.keys())
    
    def reload_icons(self) -> None:
        """Recarga todos los iconos."""
        self.icons.clear()
        self.gradients.clear()
        self.load_icons()
        self.create_gradients()

