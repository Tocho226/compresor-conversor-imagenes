#!/usr/bin/env python3
"""
Compresor Avanzado de Imágenes v9.1 - CORREGIDO
Archivo principal que usa la versión corregida con TODOS los problemas solucionados

PROBLEMAS SOLUCIONADOS:
✅ 1. Drag & drop funcional
✅ 2. Sufijos automáticos para duplicados  
✅ 3. Scroll en pantalla comprimida
✅ 4. Redimensionado con unidades (píxeles)
✅ 5. Historial reubicado con más espacio
✅ 6. Información del historial corregida
✅ 7. Vista previa en tiempo real durante compresión
✅ 8. Vista previa desde historial funcional
"""

import sys
import io
import os
import tkinter as tk
from tkinter import messagebox

# Forzar UTF-8 en Windows para evitar errores con emojis
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
# Añadir el directorio actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def check_dependencies():
    """Verifica e instala dependencias necesarias."""
    try:
        from core.format_handler import FormatHandler
        print("🔧 Verificando dependencias...")
        FormatHandler.install_dependencies()
        FormatHandler.setup_all_plugins()
        print("✅ Dependencias verificadas")
        return True
    except Exception as e:
        print(f"❌ Error verificando dependencias: {e}")
        return False

def main():
    """Función principal de la aplicación CORREGIDA."""
    try:
        print("🎨 Iniciando Compresor Avanzado de Imágenes v9.1 - CORREGIDO...")
        print("🔧 TODOS los problemas específicos han sido solucionados")
        
        # Verificar dependencias
        if not check_dependencies():
            print("⚠️ Algunas dependencias no están disponibles, pero la aplicación funcionará con funcionalidad básica")
        
        # Importar y crear la aplicación GUI CORREGIDA
        from gui.app import ImageCompressorApp
        
        # Crear ventana principal con soporte DnD
        try:
            import tkinterdnd2 as tkdnd
            root = tkdnd.Tk()
            print("✅ Ventana con soporte DnD creada")
        except ImportError:
            root = tk.Tk()
            print("⚠️ tkinterdnd2 no disponible, usando Tk normal")
        
        # Configurar manejo de errores de tkinter
        def handle_tk_error(exc, val, tb):
            error_str = str(val)
            if "tkdnd" in error_str or "drop_target" in error_str:
                print(f"⚠️ Error de drag & drop: {val}")
                print("⚠️ Continuando con funcionalidad de clic...")
                return
            else:
                # Error más serio
                print(f"❌ Error inesperado: {val}")
                try:
                    messagebox.showerror("Error", f"Error inesperado: {val}")
                except:
                    pass
        
        # Configurar manejo de errores
        root.report_callback_exception = handle_tk_error
        
        # Crear aplicación CORREGIDA
        app = ImageCompressorApp(root)
        
        print("✅ Aplicación CORREGIDA iniciada correctamente")
        print("📖 Usa F1 para ayuda, Ctrl+O para abrir archivos, Ctrl+S para comprimir")
        print("🎯 TODAS las funcionalidades han sido corregidas y mejoradas")
        
        # Configurar cierre
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Iniciar loop principal
        root.mainloop()
        
    except ImportError as e:
        error_msg = f"Error importando módulos: {e}\n\nAsegúrate de que todos los archivos estén en el mismo directorio."
        print(f"❌ {error_msg}")
        
        # Mostrar error en GUI si es posible
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error de Importación", error_msg)
        except:
            pass
        
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"Error inesperado: {e}"
        print(f"❌ {error_msg}")
        
        # Mostrar error en GUI si es posible
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error Fatal", error_msg)
        except:
            pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()

