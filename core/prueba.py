import os
import json
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
from PIL import Image
import ttkbootstrap as tb

HISTORY_FILE = "historial.json"

# ----------------- FUNCIONES DE CONVERSIÓN -----------------
SUPPORTED_FORMATS = [
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp",
    ".ico", ".ppm", ".pgm", ".pbm",
    ".avif", ".heic", ".heif",
    ".svg", ".dds", ".tga", ".eps", ".im",
    ".pdf", ".psd", ".icns", ".fits", ".msp",
    ".pcx", ".sgi", ".spider", ".xbm", ".xpm"
]

# ----------------- HISTORIAL -----------------
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_to_history(history, input_file, output_file, output_ext, status):
    entry = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entrada": os.path.basename(input_file),
        "salida": os.path.basename(output_file) if output_file else "-",
        "formato": output_ext,
        "estado": status
    }
    history.append(entry)
    save_history(history)
    return entry

# ----------------- CONVERSIÓN -----------------
def convert_file(input_path, output_ext, progress, total, idx, tree, history):
    output_path = None
    try:
        img = Image.open(input_path)
        base, _ = os.path.splitext(input_path)
        output_path = base + output_ext

        if output_ext == ".pdf":
            img.convert("RGB").save(output_path, "PDF")
        elif output_ext == ".icns":
            sizes = [16, 32, 64, 128, 256, 512, 1024]
            img.save(output_path, format="ICNS", sizes=[(s, s) for s in sizes])
        else:
            img.save(output_path)

        entry = add_to_history(history, input_path, output_path, output_ext, "✅ OK")

    except Exception as e:
        entry = add_to_history(history, input_path, output_path, output_ext, f"❌ {e}")

    # Añadir fila a la tabla
    tree.insert("", "end", values=(entry["fecha"], entry["entrada"], entry["salida"], entry["formato"], entry["estado"]))
    progress["value"] = (idx + 1) / total * 100


def convert_directory(input_dir, output_ext, progress, tree, start_btn, history):
    files = [f for f in os.listdir(input_dir) if os.path.splitext(f)[1].lower() in SUPPORTED_FORMATS]
    total = len(files)
    if total == 0:
        messagebox.showwarning("Aviso", "No se encontraron imágenes compatibles en la carpeta.")
        start_btn.config(state="normal")
        return

    progress["value"] = 0
    for idx, filename in enumerate(files):
        convert_file(os.path.join(input_dir, filename), output_ext, progress, total, idx, tree, history)

    messagebox.showinfo("Finalizado", f"Conversión completada: {total} archivos")
    start_btn.config(state="normal")


# ----------------- INTERFAZ -----------------
def run_gui():
    root = tb.Window(themename="superhero")
    root.title("Universal Image Converter")
    root.geometry("900x600")

    # Cargar historial existente
    history = load_history()

    # Frame principal
    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    # Selección de carpeta
    folder_label = ttk.Label(frame, text="Carpeta de entrada:")
    folder_label.pack(anchor="w")

    folder_var = tk.StringVar()
    folder_entry = ttk.Entry(frame, textvariable=folder_var)
    folder_entry.pack(fill="x", padx=5, pady=5)

    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            folder_var.set(folder)
    browse_btn = ttk.Button(frame, text="📂 Seleccionar carpeta", command=browse_folder)
    browse_btn.pack(pady=5)

    # Selección de formato de salida
    format_label = ttk.Label(frame, text="Formato de salida:")
    format_label.pack(anchor="w", pady=(10,0))

    output_var = tk.StringVar(value=".png")
    format_menu = ttk.Combobox(frame, textvariable=output_var, values=SUPPORTED_FORMATS, state="readonly")
    format_menu.pack(fill="x", padx=5, pady=5)

    # Botón de inicio
    start_btn = ttk.Button(frame, text="▶ Iniciar conversión", style="success.TButton")
    start_btn.pack(pady=10)

    # Barra de progreso
    progress = ttk.Progressbar(frame, length=500, mode="determinate")
    progress.pack(pady=5)

    # Tabla de historial
    log_label = ttk.Label(frame, text="Historial de conversiones:")
    log_label.pack(anchor="w", pady=(10,0))

    columns = ("Fecha", "Entrada", "Salida", "Formato", "Estado")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150 if col != "Entrada" and col != "Salida" else 200)
    tree.pack(fill="both", expand=True, padx=5, pady=5)

    # Mostrar historial guardado
    for entry in history:
        tree.insert("", "end", values=(entry["fecha"], entry["entrada"], entry["salida"], entry["formato"], entry["estado"]))

    def clear_history():
        for row in tree.get_children():
            tree.delete(row)
        history.clear()
        save_history(history)

    clear_btn = ttk.Button(frame, text="🧹 Limpiar historial", command=clear_history, style="danger.TButton")
    clear_btn.pack(pady=5)

    # Acción de inicio
    def start_conversion():
        folder = folder_var.get().strip()
        output_ext = output_var.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Selecciona una carpeta válida.")
            return
        start_btn.config(state="disabled")
        threading.Thread(
            target=convert_directory,
            args=(folder, output_ext, progress, tree, start_btn, history),
            daemon=True
        ).start()

    start_btn.config(command=start_conversion)

    root.mainloop()


if __name__ == "__main__":
    run_gui()
