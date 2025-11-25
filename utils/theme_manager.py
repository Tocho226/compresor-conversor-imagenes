#!/usr/bin/env python3
"""
ThemeManager - Gestión de temas y colores modernos
Maneja temas claro/oscuro con colores profesionales
"""

from typing import Dict, Any

class ThemeManager:
    """Gestor de temas con colores modernos y profesionales."""
    
    def __init__(self):
        self.current_theme = "modern_light"
        self.themes = {
            "modern_light": {
                # Colores principales
                "bg_primary": "#ffffff",
                "bg_secondary": "#f8f9fa",
                "bg_tertiary": "#e9ecef",
                "bg_transparent": "#ffffff",
                
                # Colores de texto
                "text_primary": "#212529",
                "text_secondary": "#6c757d",
                "text_accent": "#495057",
                
                # Colores de acento (degradados modernos)
                "accent_primary": "#667eea",      # Azul moderno
                "accent_secondary": "#764ba2",    # Púrpura elegante
                "accent_tertiary": "#f093fb",     # Rosa vibrante
                "accent_quaternary": "#f5576c",   # Coral moderno
                
                # Colores de botones
                "button_primary": "#667eea",
                "button_primary_hover": "#5a6fd8",
                "button_secondary": "#6c757d",
                "button_secondary_hover": "#5a6268",
                "button_success": "#28a745",
                "button_success_hover": "#218838",
                "button_danger": "#dc3545",
                "button_danger_hover": "#c82333",
                
                # Colores de bordes
                "border_primary": "#dee2e6",
                "border_secondary": "#ced4da",
                "border_accent": "#667eea",
                
                # Colores de estado
                "success": "#28a745",
                "warning": "#ffc107",
                "error": "#dc3545",
                "info": "#17a2b8",
                
                # Colores específicos de la aplicación
                "canvas_bg": "#f8f9fa",
                "preview_bg": "#ffffff",
                "progress_bg": "#e9ecef",
                "progress_fill": "#667eea",
                
                # Sombras
                "shadow_light": "#00000010",
                "shadow_medium": "#00000020",
                "shadow_heavy": "#00000030"
            },
            
            "modern_dark": {
                # Colores principales
                "bg_primary": "#1a1a1a",
                "bg_secondary": "#2d2d2d",
                "bg_tertiary": "#404040",
                "bg_transparent": "#1a1a1a",
                
                # Colores de texto
                "text_primary": "#ffffff",
                "text_secondary": "#b0b0b0",
                "text_accent": "#d0d0d0",
                
                # Colores de acento (más vibrantes para tema oscuro)
                "accent_primary": "#7c8aed",      # Azul más brillante
                "accent_secondary": "#8b5fbf",    # Púrpura más brillante
                "accent_tertiary": "#f2a6fc",     # Rosa más brillante
                "accent_quaternary": "#f7677c",   # Coral más brillante
                
                # Colores de botones
                "button_primary": "#7c8aed",
                "button_primary_hover": "#8a96f0",
                "button_secondary": "#6c757d",
                "button_secondary_hover": "#7a8288",
                "button_success": "#32cd32",
                "button_success_hover": "#28a745",
                "button_danger": "#ff4757",
                "button_danger_hover": "#ff3742",
                
                # Colores de bordes
                "border_primary": "#404040",
                "border_secondary": "#555555",
                "border_accent": "#7c8aed",
                
                # Colores de estado
                "success": "#32cd32",
                "warning": "#ffd700",
                "error": "#ff4757",
                "info": "#00d2ff",
                
                # Colores específicos de la aplicación
                "canvas_bg": "#2d2d2d",
                "preview_bg": "#1a1a1a",
                "progress_bg": "#404040",
                "progress_fill": "#7c8aed",
                
                # Sombras
                "shadow_light": "#00000030",
                "shadow_medium": "#00000050",
                "shadow_heavy": "#00000070"
            }
        }
    
    def get_color(self, color_name: str) -> str:
        """Obtiene un color del tema actual."""
        color = self.themes[self.current_theme].get(color_name, "#000000")
        return color if color and color.strip() else "#000000"
    
    def get_theme_colors(self) -> Dict[str, str]:
        """Obtiene todos los colores del tema actual."""
        return self.themes[self.current_theme].copy()
    
    def set_theme(self, theme_name: str) -> bool:
        """Cambia el tema actual."""
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False
    
    def toggle_theme(self) -> str:
        """Alterna entre tema claro y oscuro."""
        if self.current_theme == "modern_light":
            self.current_theme = "modern_dark"
        else:
            self.current_theme = "modern_light"
        return self.current_theme
    
    def get_current_theme(self) -> str:
        """Obtiene el nombre del tema actual."""
        return self.current_theme
    
    def is_dark_theme(self) -> bool:
        """Verifica si el tema actual es oscuro."""
        return "dark" in self.current_theme
    
    def get_gradient_colors(self, gradient_type: str = "primary") -> tuple:
        """Obtiene colores para degradados."""
        if gradient_type == "primary":
            return (self.get_color("accent_primary"), self.get_color("accent_secondary"))
        elif gradient_type == "secondary":
            return (self.get_color("accent_tertiary"), self.get_color("accent_quaternary"))
        elif gradient_type == "success":
            return (self.get_color("button_success"), "#20c997")
        elif gradient_type == "danger":
            return (self.get_color("button_danger"), "#e74c3c")
        else:
            return (self.get_color("accent_primary"), self.get_color("accent_secondary"))
    
    def get_button_style(self, button_type: str = "primary") -> Dict[str, str]:
        """Obtiene estilo completo para botones."""
        base_style = {
            "relief": "flat",
            "borderwidth": 0,
            "cursor": "hand2",
            "font": ("Segoe UI", 10, "normal")
        }
        
        if button_type == "primary":
            base_style.update({
                "bg": self.get_color("button_primary"),
                "fg": "#ffffff",
                "activebackground": self.get_color("button_primary_hover"),
                "activeforeground": "#ffffff"
            })
        elif button_type == "secondary":
            base_style.update({
                "bg": self.get_color("button_secondary"),
                "fg": "#ffffff",
                "activebackground": self.get_color("button_secondary_hover"),
                "activeforeground": "#ffffff"
            })
        elif button_type == "success":
            base_style.update({
                "bg": self.get_color("button_success"),
                "fg": "#ffffff",
                "activebackground": self.get_color("button_success_hover"),
                "activeforeground": "#ffffff"
            })
        elif button_type == "danger":
            base_style.update({
                "bg": self.get_color("button_danger"),
                "fg": "#ffffff",
                "activebackground": self.get_color("button_danger_hover"),
                "activeforeground": "#ffffff"
            })
        
        return base_style
    
    def get_frame_style(self, frame_type: str = "primary") -> Dict[str, str]:
        """Obtiene estilo para frames."""
        if frame_type == "primary":
            return {
                "bg": self.get_color("bg_primary"),
                "relief": "flat",
                "borderwidth": 0
            }
        elif frame_type == "secondary":
            return {
                "bg": self.get_color("bg_secondary"),
                "relief": "flat",
                "borderwidth": 1,
                "highlightbackground": self.get_color("border_primary")
            }
        elif frame_type == "card":
            return {
                "bg": self.get_color("bg_primary"),
                "relief": "solid",
                "borderwidth": 1,
                "highlightbackground": self.get_color("border_primary")
            }
        else:
            return {
                "bg": self.get_color("bg_primary"),
                "relief": "flat",
                "borderwidth": 0
            }
    
    def get_label_style(self, label_type: str = "primary") -> Dict[str, str]:
        """Obtiene estilo para labels."""
        base_style = {
            "bg": self.get_color("bg_primary"),
            "relief": "flat",
            "borderwidth": 0
        }
        
        if label_type == "primary":
            base_style.update({
                "fg": self.get_color("text_primary"),
                "font": ("Segoe UI", 10, "normal")
            })
        elif label_type == "secondary":
            base_style.update({
                "fg": self.get_color("text_secondary"),
                "font": ("Segoe UI", 9, "normal")
            })
        elif label_type == "title":
            base_style.update({
                "fg": self.get_color("text_primary"),
                "font": ("Segoe UI", 14, "bold")
            })
        elif label_type == "subtitle":
            base_style.update({
                "fg": self.get_color("text_accent"),
                "font": ("Segoe UI", 12, "normal")
            })
        
        return base_style

