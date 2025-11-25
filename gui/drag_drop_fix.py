#!/usr/bin/env python3
"""
Drag & Drop alternativo sin tkinterdnd2
Implementación usando eventos nativos de tkinter
"""

import tkinter as tk
import os
from typing import List, Callable, Optional

class NativeDragDrop:
    """Implementación de drag & drop usando eventos nativos de tkinter."""
    
    def __init__(self, widget: tk.Widget, callback: Callable[[List[str]], None]):
        self.widget = widget
        self.callback = callback
        self.setup_native_drop()
    
    def setup_native_drop(self):
        """Configura drag & drop nativo."""
        try:
            # Intentar configuración nativa para Windows
            self.widget.drop_target_register('DND_Files')
            self.widget.dnd_bind('<<Drop>>', self._on_drop_native)
            self.widget.dnd_bind('<<DragEnter>>', self._on_drag_enter)
            self.widget.dnd_bind('<<DragLeave>>', self._on_drag_leave)
            print("✅ Drag & drop nativo configurado")
            return True
        except:
            pass
        
        try:
            # Configuración alternativa usando tkinterdnd2 si está disponible
            import tkinterdnd2 as tkdnd
            self.widget.drop_target_register(tkdnd.DND_FILES)
            self.widget.dnd_bind('<<Drop>>', self._on_drop_tkdnd)
            self.widget.dnd_bind('<<DragEnter>>', self._on_drag_enter)
            self.widget.dnd_bind('<<DragLeave>>', self._on_drag_leave)
            print("✅ Drag & drop con tkinterdnd2 configurado")
            return True
        except Exception as e:
            print(f"⚠️ Error con tkinterdnd2: {e}")
        
        # Fallback: configurar eventos de clic mejorados
        self.setup_enhanced_click()
        print("⚠️ Usando drag & drop simulado con clic")
        return False
    
    def setup_enhanced_click(self):
        """Configura eventos de clic mejorados como fallback."""
        # Efectos visuales mejorados
        def on_enter(event):
            self.widget.configure(relief="raised", borderwidth=3)
            self.widget.configure(bg="#e3f2fd")  # Azul claro
        
        def on_leave(event):
            self.widget.configure(relief="solid", borderwidth=2)
            self.widget.configure(bg="#f5f5f5")  # Gris claro
        
        def on_click(event):
            # Simular drop abriendo diálogo
            from tkinter import filedialog
            
            filetypes = [
                ("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.webp *.avif *.heic *.heif *.ico *.ppm *.pgm *.pbm *.svg *.dds *.tga *.eps *.im *.pdf *.psd *.icns *.fits *.msp *.pcx *.sgi *.spider *.xbm *.xpm"),
                ("Todos los archivos", "*.*")
            ]
            
            files = filedialog.askopenfilenames(
                title="Seleccionar imágenes",
                filetypes=filetypes
            )
            
            if files:
                self.callback(list(files))
        
        # Bind eventos
        self.widget.bind("<Enter>", on_enter)
        self.widget.bind("<Leave>", on_leave)
        self.widget.bind("<Button-1>", on_click)
        
        # Bind también a elementos hijos
        for child in self.widget.winfo_children():
            child.bind("<Button-1>", on_click)
    
    def _on_drop_native(self, event):
        """Maneja drop nativo."""
        try:
            files = self._parse_file_list(event.data)
            if files:
                self.callback(files)
        except Exception as e:
            print(f"❌ Error en drop nativo: {e}")
    
    def _on_drop_tkdnd(self, event):
        """Maneja drop con tkinterdnd2."""
        try:
            files = self._parse_file_list(event.data)
            if files:
                self.callback(files)
        except Exception as e:
            print(f"❌ Error en drop tkdnd: {e}")
    
    def _parse_file_list(self, data: str) -> List[str]:
        """Parsea la lista de archivos del evento drop."""
        files = []
        
        # Limpiar y separar archivos
        if isinstance(data, str):
            # Remover llaves y separar por espacios
            clean_data = data.strip('{}')
            file_paths = clean_data.split()
            
            for path in file_paths:
                path = path.strip('{}')
                if os.path.exists(path) and os.path.isfile(path):
                    files.append(path)
        
        return files
    
    def _on_drag_enter(self, event):
        """Efecto visual al entrar en área de drop."""
        try:
            self.widget.configure(relief="raised", borderwidth=3)
            self.widget.configure(bg="#e8f5e8")  # Verde claro
        except:
            pass
    
    def _on_drag_leave(self, event):
        """Efecto visual al salir del área de drop."""
        try:
            self.widget.configure(relief="solid", borderwidth=2)
            self.widget.configure(bg="#f5f5f5")  # Gris claro
        except:
            pass

def setup_drag_drop_for_widget(widget: tk.Widget, callback: Callable[[List[str]], None]) -> NativeDragDrop:
    """
    Configura drag & drop para un widget específico.
    
    Args:
        widget: Widget de tkinter donde configurar drag & drop
        callback: Función a llamar cuando se suelten archivos
        
    Returns:
        Instancia de NativeDragDrop
    """
    return NativeDragDrop(widget, callback)

