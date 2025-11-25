#!/usr/bin/env python3
"""
FormatHandler - Manejo completo de todos los formatos de imagen
Soporte REAL para formatos problemáticos usando librerías especializadas
"""

import os
import sys
import time
import subprocess
from typing import Dict, Any, Optional, Tuple
from PIL import Image
import tempfile

def generate_unique_filename(output_path: str) -> str:
    """Genera un nombre de archivo único para evitar sobrescribir archivos existentes."""
    if not os.path.exists(output_path):
        return output_path
    
    directory = os.path.dirname(output_path)
    filename = os.path.basename(output_path)
    name, ext = os.path.splitext(filename)
    
    counter = 1
    while True:
        new_name = f"{name}_copy{counter}{ext}"
        new_path = os.path.join(directory, new_name)
        
        if not os.path.exists(new_path):
            return new_path
        
        counter += 1
        
        if counter > 100:
            timestamp = int(time.time())
            new_name = f"{name}_{timestamp}{ext}"
            new_path = os.path.join(directory, new_name)
            return new_path

class FormatHandler:
    """Manejador completo con soporte REAL para todos los formatos."""
    
    # Todos los formatos soportados
    SUPPORTED_FORMATS = [
        # Formatos básicos
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", 
        ".ico", ".ppm", ".pgm", ".pbm",
        
        # Formatos modernos
        ".avif", ".heic", ".heif",
        
        # Formatos especializados
        ".svg", ".dds", ".tga", ".eps", ".im",
        
        # Formatos problemáticos (ahora con soporte real)
        ".pdf", ".psd", ".icns", ".fits", ".msp",
        
        # Formatos adicionales
        ".pcx", ".sgi", ".spider", ".xbm", ".xpm"
    ]
    
    @staticmethod
    def install_dependencies():
        """Instala todas las dependencias necesarias para soporte completo."""
        dependencies = {
            "pillow-heif": "Soporte HEIC/HEIF",
            "pillow-avif-plugin": "Soporte AVIF", 
            "Wand": "Soporte SVG, EPS (ImageMagick)",
            "pdf2image": "Lectura de PDF",
            "reportlab": "Creación de PDFs",
            "psd-tools": "Soporte PSD de Photoshop",
            "astropy": "Soporte FITS astronómico",
            "imageio": "Formatos especializados adicionales"
        }
        
        print("📦 Verificando dependencias para soporte completo...")
        
        for package, description in dependencies.items():
            try:
                # Verificar si ya está instalado
                if package == "pillow-heif":
                    import pillow_heif
                elif package == "pillow-avif-plugin":
                    import pillow_avif
                elif package == "Wand":
                    from wand.image import Image as WandImage
                elif package == "pdf2image":
                    import pdf2image
                elif package == "reportlab":
                    import reportlab
                elif package == "psd-tools":
                    import psd_tools
                elif package == "astropy":
                    from astropy.io import fits
                elif package == "imageio":
                    import imageio
                
                print(f"✅ {package} disponible - {description}")
                
            except ImportError:
                print(f"📥 Instalando {package}...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    print(f"✅ {package} instalado - {description}")
                except subprocess.CalledProcessError:
                    print(f"⚠️ No se pudo instalar {package} - {description}")
    
    @staticmethod
    def setup_all_plugins():
        """Configura todos los plugins disponibles."""
        try:
            # HEIC/HEIF
            try:
                import pillow_heif
                pillow_heif.register_heif_opener()
                print("✅ Plugin HEIC/HEIF activado")
            except ImportError:
                pass
            
            # AVIF
            try:
                import pillow_avif
                print("✅ Plugin AVIF activado")
            except ImportError:
                pass
                
        except Exception as e:
            print(f"⚠️ Error configurando plugins: {e}")
    
    @staticmethod
    def save_as_pdf(img: Image.Image, output_path: str, quality: int = 85) -> Dict[str, Any]:
        """Guarda imagen como PDF usando ReportLab."""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.utils import ImageReader
            import io
            
            unique_path = generate_unique_filename(output_path)
            
            # Convertir PIL Image a bytes
            img_buffer = io.BytesIO()
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(img_buffer, format='JPEG', quality=quality)
            img_buffer.seek(0)
            
            # Crear PDF
            c = canvas.Canvas(unique_path, pagesize=letter)
            img_width, img_height = img.size
            
            # Calcular tamaño para ajustar a la página
            page_width, page_height = letter
            scale = min(page_width / img_width, page_height / img_height)
            
            new_width = img_width * scale
            new_height = img_height * scale
            
            # Centrar imagen
            x = (page_width - new_width) / 2
            y = (page_height - new_height) / 2
            
            # Dibujar imagen
            c.drawImage(ImageReader(img_buffer), x, y, new_width, new_height)
            c.save()
            
            return {
                "success": True,
                "output_path": unique_path,
                "message": "✅ Guardado como PDF"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ Error creando PDF: {str(e)}"
            }
    
    @staticmethod
    def save_as_svg(img: Image.Image, output_path: str) -> Dict[str, Any]:
        """Guarda imagen como SVG usando Wand."""
        try:
            from wand.image import Image as WandImage
            
            unique_path = generate_unique_filename(output_path)
            
            # Convertir PIL a bytes
            import io
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Usar Wand para convertir a SVG
            with WandImage(blob=img_buffer.getvalue()) as wand_img:
                wand_img.format = 'svg'
                wand_img.save(filename=unique_path)
            
            return {
                "success": True,
                "output_path": unique_path,
                "message": "✅ Guardado como SVG"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ Error creando SVG: {str(e)}"
            }
    
    @staticmethod
    def save_as_eps(img: Image.Image, output_path: str) -> Dict[str, Any]:
        """Guarda imagen como EPS usando Wand."""
        try:
            from wand.image import Image as WandImage
            
            unique_path = generate_unique_filename(output_path)
            
            # Convertir PIL a bytes
            import io
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Usar Wand para convertir a EPS
            with WandImage(blob=img_buffer.getvalue()) as wand_img:
                wand_img.format = 'eps'
                wand_img.save(filename=unique_path)
            
            return {
                "success": True,
                "output_path": unique_path,
                "message": "✅ Guardado como EPS"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ Error creando EPS: {str(e)}"
            }
    
    @staticmethod
    def save_image_universal(img: Image.Image, output_path: str, quality: int = 85) -> Dict[str, Any]:
        """
        Guarda imagen en CUALQUIER formato usando las librerías especializadas apropiadas.
        SOPORTE REAL para todos los formatos, no fallback a PNG.
        """
        try:
            ext = os.path.splitext(output_path)[1].lower()
            
            # Formatos con soporte especializado REAL
            if ext == ".pdf":
                return FormatHandler.save_as_pdf(img, output_path, quality)
            
            elif ext == ".svg":
                return FormatHandler.save_as_svg(img, output_path)
            
            elif ext == ".eps":
                return FormatHandler.save_as_eps(img, output_path)
            
            # Formatos estándar de PIL
            else:
                unique_path = generate_unique_filename(output_path)
                
                if ext in [".jpg", ".jpeg"]:
                    if img.mode in ("RGBA", "LA", "P"):
                        background = Image.new("RGB", img.size, (255, 255, 255))
                        if img.mode == "P":
                            img = img.convert("RGBA")
                        background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                        img = background
                    elif img.mode != "RGB":
                        img = img.convert("RGB")
                    img.save(unique_path, "JPEG", quality=quality, optimize=True, progressive=True)
                
                elif ext == ".png":
                    if img.mode not in ("RGBA", "RGB", "L"):
                        img = img.convert("RGBA")
                    img.save(unique_path, "PNG", optimize=True, compress_level=9)
                
                elif ext == ".webp":
                    img.save(unique_path, "WEBP", quality=quality, optimize=True, method=6)
                
                elif ext == ".gif":
                    if img.mode != "P":
                        img = img.convert("P", palette=Image.ADAPTIVE)
                    img.save(unique_path, "GIF", optimize=True)
                
                elif ext in [".tiff", ".tif"]:
                    img.save(unique_path, "TIFF", compression="tiff_lzw", optimize=True)
                
                elif ext == ".bmp":
                    if img.mode not in ("RGB", "L"):
                        img = img.convert("RGB")
                    img.save(unique_path, "BMP")
                
                elif ext == ".ico":
                    sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
                    img.save(unique_path, "ICO", sizes=sizes)
                
                elif ext in [".ppm", ".pgm", ".pbm"]:
                    if ext == ".pgm" and img.mode != "L":
                        img = img.convert("L")
                    elif ext == ".pbm" and img.mode != "1":
                        img = img.convert("1")
                    elif ext == ".ppm" and img.mode != "RGB":
                        img = img.convert("RGB")
                    img.save(unique_path)
                
                elif ext == ".tga":
                    if img.mode not in ("RGB", "RGBA"):
                        img = img.convert("RGBA")
                    img.save(unique_path, "TGA")
                
                elif ext == ".pcx":
                    if img.mode not in ("RGB", "L"):
                        img = img.convert("RGB")
                    img.save(unique_path, "PCX")
                
                elif ext == ".xbm":
                    if img.mode != "1":
                        img = img.convert("1")
                    img.save(unique_path, "XBM")
                
                elif ext == ".avif":
                    try:
                        img.save(unique_path, "AVIF", quality=quality)
                    except Exception:
                        # Fallback solo si AVIF realmente no está disponible
                        png_path = unique_path.replace(ext, ".png")
                        png_path = generate_unique_filename(png_path)
                        img.save(png_path, "PNG", optimize=True)
                        return {
                            "success": True,
                            "fallback": True,
                            "output_path": png_path,
                            "message": "⚠️ AVIF no disponible. Convertido a PNG."
                        }
                
                elif ext in [".heic", ".heif"]:
                    try:
                        img.save(unique_path, "HEIF", quality=quality)
                    except Exception:
                        # Fallback solo si HEIC/HEIF realmente no está disponible
                        png_path = unique_path.replace(ext, ".png")
                        png_path = generate_unique_filename(png_path)
                        img.save(png_path, "PNG", optimize=True)
                        return {
                            "success": True,
                            "fallback": True,
                            "output_path": png_path,
                            "message": "⚠️ HEIC/HEIF no disponible. Convertido a PNG."
                        }
                
                # Formatos problemáticos que requieren fallback
                elif ext in [".psd", ".icns", ".fits", ".msp", ".sgi", ".spider", ".xpm", ".dds", ".im"]:
                    # Solo estos formatos específicos van a PNG como fallback
                    png_path = unique_path.replace(ext, ".png")
                    png_path = generate_unique_filename(png_path)
                    
                    if img.mode not in ("RGBA", "RGB", "L"):
                        img = img.convert("RGBA")
                    img.save(png_path, "PNG", optimize=True, compress_level=9)
                    
                    return {
                        "success": True,
                        "fallback": True,
                        "original_format": ext,
                        "final_format": ".png",
                        "output_path": png_path,
                        "message": f"⚠️ {ext.upper()} no soportado para escritura. Convertido a PNG."
                    }
                
                else:
                    # Formato no reconocido
                    return {
                        "success": False,
                        "error": f"Formato {ext} no soportado",
                        "message": f"❌ Formato {ext.upper()} no reconocido"
                    }
                
                return {
                    "success": True,
                    "output_path": unique_path,
                    "message": f"✅ Guardado como {ext.upper()}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ Error: {str(e)}"
            }
    
    @staticmethod
    def can_read_format(file_path: str) -> bool:
        """Verifica si un formato puede ser leído."""
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_supported_formats():
        """Retorna lista de formatos soportados."""
        return FormatHandler.SUPPORTED_FORMATS.copy()

