        history_frame = tk.LabelFrame(parent, text="📋 Historial Reciente",
                                     **self.theme.get_frame_style("secondary"))
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Lista de historial
        self.history_listbox = tk.Listbox(history_frame, height=8,
                                         bg=self.theme.get_color("bg_primary"),
                                         fg=self.theme.get_color("text_primary"),
                                         selectbackground=self.theme.get_color("accent_primary"))
        self.history_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.history_listbox.bind("<Double-Button-1>", self.load_from_history)
        
        # Actualizar historial
        self.update_history_display()
    
    def create_preview_panel(self, parent):
        """Crea el panel de vista previa."""
        preview_frame = tk.Frame(parent, **self.theme.get_frame_style("card"))
        preview_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Título del panel
        title_label = tk.Label(preview_frame, text="🖼️ Vista Previa",
                              **self.theme.get_label_style("subtitle"))
        title_label.pack(pady=10)
        
        # Canvas para vista previa
        canvas_frame = tk.Frame(preview_frame, **self.theme.get_frame_style("primary"))
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Vista previa antes/después
        preview_container = tk.Frame(canvas_frame, **self.theme.get_frame_style("primary"))
        preview_container.pack(fill="both", expand=True)
        
        # Antes
        before_frame = tk.Frame(preview_container, **self.theme.get_frame_style("secondary"))
        before_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 5))
        
        tk.Label(before_frame, text="Antes", **self.theme.get_label_style("primary")).pack(pady=5)
        self.before_canvas = tk.Canvas(before_frame, width=280, height=280,
                                      bg=self.theme.get_color("canvas_bg"),
                                      highlightthickness=1,
                                      highlightbackground=self.theme.get_color("border_primary"))
        self.before_canvas.pack(padx=5, pady=5)
        
        # Después
        after_frame = tk.Frame(preview_container, **self.theme.get_frame_style("secondary"))
        after_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=(5, 0))
        
        tk.Label(after_frame, text="Después", **self.theme.get_label_style("primary")).pack(pady=5)
        self.after_canvas = tk.Canvas(after_frame, width=280, height=280,