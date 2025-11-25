#!/usr/bin/env python3
"""
ConfigManager - Gestión de configuración persistente
Maneja configuraciones de usuario y preferencias
"""

import json
import os
from typing import Dict, Any, Optional

class ConfigManager:
    """Gestor de configuración con persistencia automática."""
    
    def __init__(self, config_file: str = "image_compressor_config.json"):
        self.config_file = config_file
        self.default_config = {
            "theme": "modern_light",
            "quality": 85,
            "output_format": ".jpg",
            "maintain_aspect": True,
            "last_input_dir": "",
            "last_output_dir": "",
            "window_geometry": "1200x800",
            "auto_preview": True,
            "show_tooltips": True,
            "compression_level": 9,
            "jpeg_progressive": True,
            "png_optimize": True,
            "webp_method": 6,
            "recent_formats": [".jpg", ".png", ".webp"],
            "max_preview_size": 400,
            "auto_backup": False,
            "confirm_overwrite": True,
            "show_file_info": True,
            "enable_shortcuts": True,
            "language": "es",
            "check_updates": True
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde el archivo."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                
                # Migrar configuraciones antiguas
                migrated_config = self._migrate_config(loaded_config)
                
                # Combinar con valores por defecto para nuevas opciones
                config = self.default_config.copy()
                config.update(migrated_config)
                
                return config
            else:
                return self.default_config.copy()
                
        except Exception as e:
            print(f"⚠️ Error cargando configuración: {e}")
            return self.default_config.copy()
    
    def save_config(self) -> bool:
        """Guarda la configuración actual al archivo."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"⚠️ Error guardando configuración: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor de configuración."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Establece un valor de configuración."""
        self.config[key] = value
        self.save_config()
    
    def get_all(self) -> Dict[str, Any]:
        """Obtiene toda la configuración."""
        return self.config.copy()
    
    def reset_to_defaults(self) -> None:
        """Resetea la configuración a valores por defecto."""
        self.config = self.default_config.copy()
        self.save_config()
    
    def update_multiple(self, updates: Dict[str, Any]) -> None:
        """Actualiza múltiples valores de configuración."""
        self.config.update(updates)
        self.save_config()
    
    def _migrate_config(self, old_config: Dict[str, Any]) -> Dict[str, Any]:
        """Migra configuraciones de versiones anteriores."""
        migrated = old_config.copy()
        
        # Migrar tema antiguo
        if migrated.get("theme") == "light":
            migrated["theme"] = "modern_light"
        elif migrated.get("theme") == "dark":
            migrated["theme"] = "modern_dark"
        
        # Migrar formato de salida
        if "output_format" in migrated:
            format_val = migrated["output_format"]
            if not format_val.startswith("."):
                migrated["output_format"] = f".{format_val}"
        
        # Añadir nuevas configuraciones si no existen
        for key, default_value in self.default_config.items():
            if key not in migrated:
                migrated[key] = default_value
        
        return migrated
    
    def add_recent_format(self, format_ext: str) -> None:
        """Añade un formato a la lista de recientes."""
        recent = self.get("recent_formats", [])
        
        # Remover si ya existe
        if format_ext in recent:
            recent.remove(format_ext)
        
        # Añadir al principio
        recent.insert(0, format_ext)
        
        # Mantener solo los últimos 10
        recent = recent[:10]
        
        self.set("recent_formats", recent)
    
    def get_recent_formats(self) -> list:
        """Obtiene la lista de formatos recientes."""
        return self.get("recent_formats", [".jpg", ".png", ".webp"])
    
    def set_last_directories(self, input_dir: str = None, output_dir: str = None) -> None:
        """Establece los últimos directorios utilizados."""
        if input_dir:
            self.set("last_input_dir", input_dir)
        if output_dir:
            self.set("last_output_dir", output_dir)
    
    def get_last_directories(self) -> tuple:
        """Obtiene los últimos directorios utilizados."""
        return (
            self.get("last_input_dir", ""),
            self.get("last_output_dir", "")
        )
    
    def export_config(self, export_path: str) -> bool:
        """Exporta la configuración a un archivo."""
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error exportando configuración: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """Importa configuración desde un archivo."""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Validar y migrar configuración importada
            migrated_config = self._migrate_config(imported_config)
            
            # Actualizar configuración actual
            self.config.update(migrated_config)
            self.save_config()
            
            return True
        except Exception as e:
            print(f"❌ Error importando configuración: {e}")
            return False
    
    def get_compression_settings(self) -> Dict[str, Any]:
        """Obtiene configuraciones específicas de compresión."""
        return {
            "quality": self.get("quality", 85),
            "compression_level": self.get("compression_level", 9),
            "jpeg_progressive": self.get("jpeg_progressive", True),
            "png_optimize": self.get("png_optimize", True),
            "webp_method": self.get("webp_method", 6),
            "maintain_aspect": self.get("maintain_aspect", True)
        }
    
    def get_ui_settings(self) -> Dict[str, Any]:
        """Obtiene configuraciones específicas de interfaz."""
        return {
            "theme": self.get("theme", "modern_light"),
            "window_geometry": self.get("window_geometry", "1200x800"),
            "auto_preview": self.get("auto_preview", True),
            "show_tooltips": self.get("show_tooltips", True),
            "max_preview_size": self.get("max_preview_size", 400),
            "show_file_info": self.get("show_file_info", True),
            "enable_shortcuts": self.get("enable_shortcuts", True)
        }

