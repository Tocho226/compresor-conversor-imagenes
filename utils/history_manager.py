#!/usr/bin/env python3
"""
HistoryManager - Gestión de historial de compresiones
Maneja el historial persistente y exportación
"""

import json
import os
import csv
from datetime import datetime
from typing import Dict, Any, List, Optional

class HistoryManager:
    """Gestor de historial con persistencia y exportación."""
    
    def __init__(self, history_file: str = "compression_history.json", max_items: int = 100):
        self.history_file = history_file
        self.max_items = max_items
        self.history = self.load_history()
    
    def load_history(self) -> List[Dict[str, Any]]:
        """Carga el historial desde el archivo."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                
                # Validar estructura del historial
                if isinstance(history, list):
                    return history[-self.max_items:]  # Mantener solo los últimos elementos
                else:
                    return []
            else:
                return []
                
        except Exception as e:
            print(f"⚠️ Error cargando historial: {e}")
            return []
    
    def save_history(self) -> bool:
        """Guarda el historial al archivo."""
        try:
            # Mantener solo los últimos elementos
            self.history = self.history[-self.max_items:]
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"⚠️ Error guardando historial: {e}")
            return False
    
    def add_entry(self, compression_result: Dict[str, Any], input_path: str) -> None:
        """Añade una entrada al historial."""
        try:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "input_path": input_path,
                "input_filename": os.path.basename(input_path),
                "output_path": compression_result.get("output_path", ""),
                "output_filename": os.path.basename(compression_result.get("output_path", "")),
                "original_size": compression_result.get("original_size", 0),
                "compressed_size": compression_result.get("compressed_size", 0),
                "compression_ratio": compression_result.get("compression_ratio", 0),
                "original_dimensions": compression_result.get("original_dimensions", [0, 0]),
                "final_dimensions": compression_result.get("final_dimensions", [0, 0]),
                "format": compression_result.get("format", ""),
                "success": compression_result.get("success", False),
                "message": compression_result.get("message", ""),
                "fallback": compression_result.get("fallback", False)
            }
            
            self.history.append(entry)
            self.save_history()
            
        except Exception as e:
            print(f"⚠️ Error añadiendo entrada al historial: {e}")
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Obtiene el historial completo o limitado."""
        if limit:
            return self.history[-limit:]
        return self.history.copy()
    
    def get_recent_entries(self, count: int = 10) -> List[Dict[str, Any]]:
        """Obtiene las entradas más recientes."""
        return self.history[-count:]
    
    def clear_history(self) -> bool:
        """Limpia todo el historial."""
        try:
            self.history = []
            return self.save_history()
        except Exception as e:
            print(f"❌ Error limpiando historial: {e}")
            return False
    
    def remove_entry(self, index: int) -> bool:
        """Elimina una entrada específica del historial."""
        try:
            if 0 <= index < len(self.history):
                self.history.pop(index)
                return self.save_history()
            return False
        except Exception as e:
            print(f"❌ Error eliminando entrada: {e}")
            return False
    
    def export_to_csv(self, export_path: str) -> bool:
        """Exporta el historial a un archivo CSV."""
        try:
            with open(export_path, 'w', newline='', encoding='utf-8') as csvfile:
                if not self.history:
                    return True  # Archivo vacío pero válido
                
                fieldnames = [
                    'Fecha y Hora', 'Archivo Original', 'Archivo Comprimido',
                    'Tamaño Original (MB)', 'Tamaño Comprimido (MB)', 
                    'Reducción (%)', 'Dimensiones Originales', 'Dimensiones Finales',
                    'Formato', 'Estado', 'Mensaje', 'Conversión Automática'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for entry in self.history:
                    # Formatear datos para CSV
                    original_size_mb = round(entry.get('original_size', 0) / (1024 * 1024), 2)
                    compressed_size_mb = round(entry.get('compressed_size', 0) / (1024 * 1024), 2)
                    
                    original_dims = entry.get('original_dimensions', [0, 0])
                    final_dims = entry.get('final_dimensions', [0, 0])
                    
                    row = {
                        'Fecha y Hora': entry.get('timestamp', ''),
                        'Archivo Original': entry.get('input_filename', ''),
                        'Archivo Comprimido': entry.get('output_filename', ''),
                        'Tamaño Original (MB)': original_size_mb,
                        'Tamaño Comprimido (MB)': compressed_size_mb,
                        'Reducción (%)': round(entry.get('compression_ratio', 0), 1),
                        'Dimensiones Originales': f"{original_dims[0]}x{original_dims[1]}",
                        'Dimensiones Finales': f"{final_dims[0]}x{final_dims[1]}",
                        'Formato': entry.get('format', ''),
                        'Estado': 'Éxito' if entry.get('success') else 'Error',
                        'Mensaje': entry.get('message', ''),
                        'Conversión Automática': 'Sí' if entry.get('fallback') else 'No'
                    }
                    
                    writer.writerow(row)
            
            return True
            
        except Exception as e:
            print(f"❌ Error exportando historial a CSV: {e}")
            return False
    
    def export_to_json(self, export_path: str) -> bool:
        """Exporta el historial a un archivo JSON."""
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error exportando historial a JSON: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas del historial."""
        try:
            if not self.history:
                return {
                    "total_compressions": 0,
                    "successful_compressions": 0,
                    "failed_compressions": 0,
                    "total_space_saved": 0,
                    "average_compression_ratio": 0,
                    "most_used_format": "",
                    "total_files_processed": 0
                }
            
            successful = [entry for entry in self.history if entry.get('success')]
            failed = [entry for entry in self.history if not entry.get('success')]
            
            # Calcular espacio ahorrado total
            total_space_saved = sum(
                entry.get('original_size', 0) - entry.get('compressed_size', 0)
                for entry in successful
            )
            
            # Calcular ratio promedio
            ratios = [entry.get('compression_ratio', 0) for entry in successful if entry.get('compression_ratio', 0) > 0]
            avg_ratio = sum(ratios) / len(ratios) if ratios else 0
            
            # Formato más usado
            formats = [entry.get('format', '') for entry in successful]
            most_used_format = max(set(formats), key=formats.count) if formats else ""
            
            return {
                "total_compressions": len(self.history),
                "successful_compressions": len(successful),
                "failed_compressions": len(failed),
                "total_space_saved": total_space_saved,
                "total_space_saved_mb": round(total_space_saved / (1024 * 1024), 2),
                "average_compression_ratio": round(avg_ratio, 1),
                "most_used_format": most_used_format,
                "total_files_processed": len(self.history),
                "success_rate": round((len(successful) / len(self.history)) * 100, 1) if self.history else 0
            }
            
        except Exception as e:
            print(f"❌ Error calculando estadísticas: {e}")
            return {}
    
    def search_history(self, query: str) -> List[Dict[str, Any]]:
        """Busca en el historial por nombre de archivo o formato."""
        try:
            query = query.lower()
            results = []
            
            for entry in self.history:
                # Buscar en nombre de archivo original
                if query in entry.get('input_filename', '').lower():
                    results.append(entry)
                # Buscar en nombre de archivo comprimido
                elif query in entry.get('output_filename', '').lower():
                    results.append(entry)
                # Buscar en formato
                elif query in entry.get('format', '').lower():
                    results.append(entry)
                # Buscar en mensaje
                elif query in entry.get('message', '').lower():
                    results.append(entry)
            
            return results
            
        except Exception as e:
            print(f"❌ Error buscando en historial: {e}")
            return []
    
    def get_entry_by_index(self, index: int) -> Optional[Dict[str, Any]]:
        """Obtiene una entrada específica por índice."""
        try:
            if 0 <= index < len(self.history):
                return self.history[index].copy()
            return None
        except Exception as e:
            print(f"❌ Error obteniendo entrada: {e}")
            return None

