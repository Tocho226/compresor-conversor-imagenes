#!/usr/bin/env python3
"""
CompressionEngine - Motor de compresión de imágenes
Maneja la compresión real con vista previa en tiempo real
"""

import os
from typing import Dict, Any, Optional, Tuple, List, Callable
from PIL import Image
from .format_handler import FormatHandler

class CompressionEngine:
    """Motor de compresión con soporte para todos los formatos."""
    
    def __init__(self):
        self.format_handler = FormatHandler()
    
    def compress_image(self, input_path: str, output_path: str, quality: int = 85, 
                      new_size: Optional[Tuple[int, int]] = None, 
                      maintain_aspect: bool = True,
                      progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Comprime una imagen con soporte universal para todos los formatos.
        
        Args:
            input_path: Ruta de la imagen de entrada
            output_path: Ruta de salida deseada
            quality: Calidad de compresión (10-100)
            new_size: Nuevo tamaño opcional (ancho, alto)
            maintain_aspect: Si mantener la relación de aspecto
            progress_callback: Función callback para reportar progreso
            
        Returns:
            Diccionario con resultado de la compresión
        """
        try:
            if progress_callback:
                progress_callback("Cargando imagen...")
            
            # Obtener información del archivo original
            original_size = os.path.getsize(input_path)
            
            # Cargar imagen
            with Image.open(input_path) as img:
                original_dimensions = img.size
                
                if progress_callback:
                    progress_callback("Procesando imagen...")
                
                # Redimensionar si se especifica
                if new_size and new_size != (0, 0):
                    if maintain_aspect:
                        img.thumbnail(new_size, Image.Resampling.LANCZOS)
                    else:
                        img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                if progress_callback:
                    progress_callback("Guardando imagen...")
                
                # Guardar con soporte universal
                save_result = self.format_handler.save_image_universal(img, output_path, quality)
                
                if not save_result["success"]:
                    return {
                        "success": False,
                        "error": save_result.get("error", "Error desconocido al guardar"),
                        "message": save_result.get("message", "❌ Error al guardar")
                    }
                
                # Obtener información del archivo comprimido
                final_output_path = save_result["output_path"]
                compressed_size = os.path.getsize(final_output_path)
                compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
                
                output_ext = os.path.splitext(final_output_path)[1].upper().lstrip(".")
                
                if progress_callback:
                    progress_callback("Compresión completada")
                
                return {
                    "success": True,
                    "original_size": original_size,
                    "compressed_size": compressed_size,
                    "compression_ratio": compression_ratio,
                    "original_dimensions": original_dimensions,
                    "final_dimensions": img.size,
                    "format": output_ext,
                    "output_path": final_output_path,
                    "fallback": save_result.get("fallback", False),
                    "message": save_result.get("message", f"✅ Comprimido como {output_ext}")
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"❌ Error: {str(e)}"
            }
    
    def compress_multiple_images(self, image_paths: List[str], output_dir: str, 
                                output_format: str, quality: int = 85,
                                new_size: Optional[Tuple[int, int]] = None,
                                maintain_aspect: bool = True,
                                progress_callback: Optional[Callable] = None,
                                image_callback: Optional[Callable] = None) -> List[Dict[str, Any]]:
        """
        Comprime múltiples imágenes con callbacks para progreso e imagen actual.
        
        Args:
            image_paths: Lista de rutas de imágenes
            output_dir: Directorio de salida
            output_format: Formato de salida (ej: '.jpg')
            quality: Calidad de compresión
            new_size: Nuevo tamaño opcional
            maintain_aspect: Mantener relación de aspecto
            progress_callback: Callback para progreso general
            image_callback: Callback cuando se procesa cada imagen
            
        Returns:
            Lista de resultados de compresión
        """
        results = []
        total_images = len(image_paths)
        
        for i, input_path in enumerate(image_paths):
            try:
                # Generar nombre de archivo de salida
                base_name = os.path.splitext(os.path.basename(input_path))[0]
                output_filename = f"{base_name}{output_format}"
                output_path = os.path.join(output_dir, output_filename)
                
                # Callback de progreso general
                if progress_callback:
                    progress = (i / total_images) * 100
                    progress_callback(f"Procesando {i+1}/{total_images}: {base_name}", progress)
                
                # Comprimir imagen individual
                def individual_progress(msg):
                    if progress_callback:
                        progress_callback(f"{msg} ({i+1}/{total_images})")
                
                result = self.compress_image(
                    input_path, output_path, quality, new_size, maintain_aspect, individual_progress
                )
                
                # Callback cuando se completa una imagen (para vista previa en tiempo real)
                if image_callback and result["success"]:
                    image_callback(input_path, result["output_path"], result)
                
                results.append(result)
                
            except Exception as e:
                error_result = {
                    "success": False,
                    "error": str(e),
                    "message": f"❌ Error procesando {os.path.basename(input_path)}: {str(e)}",
                    "input_path": input_path
                }
                results.append(error_result)
        
        # Progreso final
        if progress_callback:
            progress_callback("Compresión completada", 100)
        
        return results
    
    def get_image_info(self, image_path: str) -> Dict[str, Any]:
        """Obtiene información detallada de una imagen."""
        try:
            with Image.open(image_path) as img:
                file_size = os.path.getsize(image_path)
                
                return {
                    "success": True,
                    "dimensions": img.size,
                    "mode": img.mode,
                    "format": img.format,
                    "file_size": file_size,
                    "file_size_mb": round(file_size / (1024 * 1024), 2)
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def estimate_compressed_size(self, image_path: str, quality: int, 
                                new_size: Optional[Tuple[int, int]] = None) -> Dict[str, Any]:
        """Estima el tamaño de la imagen comprimida sin guardarla."""
        try:
            import io
            
            with Image.open(image_path) as img:
                # Redimensionar si es necesario
                if new_size and new_size != (0, 0):
                    img.thumbnail(new_size, Image.Resampling.LANCZOS)
                
                # Simular compresión en memoria
                buffer = io.BytesIO()
                
                if img.mode in ("RGBA", "LA", "P"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                    img = background
                elif img.mode != "RGB":
                    img = img.convert("RGB")
                
                img.save(buffer, format="JPEG", quality=quality, optimize=True)
                estimated_size = buffer.tell()
                
                original_size = os.path.getsize(image_path)
                compression_ratio = (1 - estimated_size / original_size) * 100 if original_size > 0 else 0
                
                return {
                    "success": True,
                    "estimated_size": estimated_size,
                    "original_size": original_size,
                    "compression_ratio": compression_ratio,
                    "estimated_size_mb": round(estimated_size / (1024 * 1024), 2)
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

