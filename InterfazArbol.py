import os
import shutil
import tempfile
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from graphviz import Digraph

import Arbol


# Asegurar que Graphviz funciona si está instalado pero no en el PATH de la terminal actual
import os
import shutil

graphviz_bin = r"C:\Program Files\Graphviz\bin"
if shutil.which("dot") is None:
    if os.path.exists(graphviz_bin):
        os.environ["PATH"] += os.pathsep + graphviz_bin
    elif os.path.exists(r"C:\Program Files (x86)\Graphviz\bin"):
        os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Graphviz\bin"


class ModernButton(tk.Button):
    def __init__(
        self,
        master,
        text,
        command,
        bg="#3B82F6",
        hover_bg="#2563EB",
        fg="white",
        active_fg="white",
        font=("Segoe UI", 10, "bold"),
        height=1,
        padx=14,
        pady=10,
        relief="flat",
        bd=0,
        cursor="hand2",
        **kwargs
    ):
        super().__init__(
            master,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=active_fg,
            font=font,
            relief=relief,
            bd=bd,
            cursor=cursor,
            padx=padx,
            pady=pady,
            highlightthickness=0,
            **kwargs
        )
        self.default_bg = bg
        self.hover_bg = hover_bg
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event):
        self.configure(bg=self.hover_bg)

    def _on_leave(self, _event):
        self.configure(bg=self.default_bg)


class InterfazArbol:
    def __init__(self, root):
        self.root = root
        self.root.title("Árbol Binario de Búsqueda - Visualizador y Gestor")
        self.root.geometry("1450x840")
        self.root.minsize(1220, 720)
        self.root.configure(bg="#F5F7FA")

        self.arbol = Arbol.Arbol()
        self.temp_dir = tempfile.mkdtemp(prefix="abb_graphviz_")
        self.tree_image = None

        self.highlighted_node_id = None
        self.selected_node_id = None

        self._crear_estilos_base()
        self._crear_componentes()
        self._actualizar_vista_arbol()

    # ==================================================
    # ESTILO BASE
    # ==================================================
    def _crear_estilos_base(self):
        self.colors = {
            "bg_main": "#F5F7FA",
            "bg_panel": "#E9EEF5",
            "bg_card": "#FFFFFF",
            "bg_card_alt": "#F8FAFC",
            "text": "#1F2937",
            "muted": "#6B7280",
            "border": "#D7DEE8",
            "primary": "#3B82F6",
            "primary_hover": "#2563EB",
            "success": "#10B981",
            "success_hover": "#059669",
            "danger": "#EF4444",
            "danger_hover": "#DC2626",
            "secondary": "#64748B",
            "secondary_hover": "#475569",
            "purple": "#8B5CF6",
            "purple_hover": "#7C3AED",
            "orange": "#F59E0B",
            "orange_hover": "#D97706",
            "output_bg": "#F8FAFC",
            "ok": "#047857",
            "error": "#B91C1C",
            "info": "#1D4ED8",
            "warning": "#B45309",
        }

        self.fonts = {
            "title": ("Segoe UI", 22, "bold"),
            "section": ("Segoe UI", 12, "bold"),
            "subtitle": ("Segoe UI", 11, "bold"),
            "text": ("Segoe UI", 10),
            "text_small": ("Segoe UI", 9),
            "button": ("Segoe UI", 10, "bold"),
            "output": ("Consolas", 10),
        }

    # ==================================================
    # CONSTRUCCIÓN UI
    # ==================================================
    def _crear_componentes(self):
        # Contenedor principal
        self.main_container = tk.Frame(self.root, bg=self.colors["bg_main"])
        self.main_container.pack(fill="both", expand=True, padx=18, pady=18)

        # Header
        self._crear_header()

        # Body
        self.body = tk.Frame(self.main_container, bg=self.colors["bg_main"])
        self.body.pack(fill="both", expand=True, pady=(16, 0))

        self.body.grid_columnconfigure(0, weight=0, minsize=360)
        self.body.grid_columnconfigure(1, weight=1)
        self.body.grid_rowconfigure(0, weight=1)
        self.body.grid_rowconfigure(1, weight=0)

        # Panel izquierdo
        self.sidebar = tk.Frame(
            self.body,
            bg=self.colors["bg_panel"],
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            bd=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 16), pady=(0, 12))

        # Área central
        self.center_area = tk.Frame(self.body, bg=self.colors["bg_main"])
        self.center_area.grid(row=0, column=1, sticky="nsew", pady=(0, 12))
        self.center_area.grid_rowconfigure(1, weight=1)
        self.center_area.grid_columnconfigure(0, weight=1)

        # Salida inferior
        self.bottom_area = tk.Frame(
            self.body,
            bg=self.colors["bg_card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        self.bottom_area.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self._crear_sidebar()
        self._crear_visualizacion()
        self._crear_salida()

    def _crear_header(self):
        header = tk.Frame(
            self.main_container,
            bg=self.colors["bg_card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        header.pack(fill="x")

        title_frame = tk.Frame(header, bg=self.colors["bg_card"])
        title_frame.pack(fill="x", padx=20, pady=16)

        tk.Label(
            title_frame,
            text="Árbol Binario de Búsqueda",
            font=self.fonts["title"],
            fg=self.colors["text"],
            bg=self.colors["bg_card"]
        ).pack(anchor="w")



    def _crear_sidebar(self):
        # Canvas + scroll del panel lateral
        sidebar_canvas = tk.Canvas(
            self.sidebar,
            bg=self.colors["bg_panel"],
            highlightthickness=0,
            bd=0
        )
        sidebar_scroll = tk.Scrollbar(self.sidebar, orient="vertical", command=sidebar_canvas.yview)
        self.sidebar_content = tk.Frame(sidebar_canvas, bg=self.colors["bg_panel"])

        self.sidebar_content.bind(
            "<Configure>",
            lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
        )

        sidebar_canvas.create_window((0, 0), window=self.sidebar_content, anchor="nw")
        sidebar_canvas.configure(yscrollcommand=sidebar_scroll.set)

        sidebar_canvas.pack(side="left", fill="both", expand=True)
        sidebar_scroll.pack(side="right", fill="y")

        # Título lateral
        tk.Label(
            self.sidebar_content,
            text="Panel de control",
            font=("Segoe UI", 15, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg_panel"]
        ).pack(anchor="w", padx=16, pady=(16, 4))



        # Tarjeta: Operaciones
        ops_card = self._crear_card(self.sidebar_content, "Operaciones del árbol")
        self._crear_operaciones_card(ops_card)

        # Tarjeta: Búsquedas
        search_card = self._crear_card(self.sidebar_content, "Búsquedas por criterio")
        self._crear_busquedas_card(search_card)

        # Tarjeta: Estado
        state_card = self._crear_card(self.sidebar_content, "Estado / ayuda visual")
        self._crear_estado_card(state_card)

    def _crear_operaciones_card(self, parent):
        tk.Label(
            parent,
            text="ID del curso",
            font=self.fonts["subtitle"],
            fg=self.colors["text"],
            bg=self.colors["bg_card"]
        ).pack(anchor="w", padx=16, pady=(16, 6))

        self.entry_id = tk.Entry(
            parent,
            font=self.fonts["text"],
            bg="white",
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["primary"],
            bd=0
        )
        self.entry_id.pack(fill="x", padx=16, pady=(0, 14), ipady=9)

        btn_container = tk.Frame(parent, bg=self.colors["bg_card"])
        btn_container.pack(fill="x", padx=16, pady=(0, 14))

        ModernButton(
            btn_container,
            text="Insertar nodo",
            command=self.insertar_nodo,
            bg=self.colors["success"],
            hover_bg=self.colors["success_hover"],
            font=self.fonts["button"]
        ).pack(fill="x", pady=4)

        ModernButton(
            btn_container,
            text="Eliminar nodo por ID",
            command=self.eliminar_nodo,
            bg=self.colors["danger"],
            hover_bg=self.colors["danger_hover"],
            font=self.fonts["button"]
        ).pack(fill="x", pady=4)

        ModernButton(
            btn_container,
            text="Buscar nodo por ID",
            command=self.buscar_nodo,
            bg=self.colors["primary"],
            hover_bg=self.colors["primary_hover"],
            font=self.fonts["button"]
        ).pack(fill="x", pady=4)

        ModernButton(
            btn_container,
            text="Mostrar recorrido por niveles",
            command=self.mostrar_bfs,
            bg=self.colors["secondary"],
            hover_bg=self.colors["secondary_hover"],
            font=self.fonts["button"]
        ).pack(fill="x", pady=4)

        ModernButton(
            btn_container,
            text="Mostrar información completa",
            command=self.mostrar_info_completa,
            bg=self.colors["purple"],
            hover_bg=self.colors["purple_hover"],
            font=self.fonts["button"]
        ).pack(fill="x", pady=4)



        ModernButton(
            btn_container,
            text="Refrescar visualización",
            command=self._actualizar_vista_arbol,
            bg="#94A3B8",
            hover_bg="#64748B",
            font=self.fonts["button"]
        ).pack(fill="x", pady=4)

        ModernButton(
            btn_container,
            text="Limpiar salida",
            command=self.limpiar_salida,
            bg="#CBD5E1",
            hover_bg="#94A3B8",
            fg="#1F2937",
            active_fg="white",
            font=self.fonts["button"]
        ).pack(fill="x", pady=4)

    def _crear_busquedas_card(self, parent):
        content = tk.Frame(parent, bg=self.colors["bg_card"])
        content.pack(fill="x", padx=16, pady=(14, 16))

        ModernButton(
            content,
            text="Positivas > (Negativas + Neutras)",
            command=self.buscar_positivos_mayores,
            bg=self.colors["primary"],
            hover_bg=self.colors["primary_hover"],
            font=self.fonts["button"]
        ).pack(fill="x", pady=(0, 10))

        # Fecha
        tk.Label(
            content,
            text="Fecha de creación (YYYY-MM-DD)",
            font=self.fonts["subtitle"],
            fg=self.colors["text"],
            bg=self.colors["bg_card"]
        ).pack(anchor="w", pady=(0, 6))

        self.entry_fecha = tk.Entry(
            content,
            font=self.fonts["text"],
            bg="white",
            fg=self.colors["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["primary"],
            bd=0
        )
        self.entry_fecha.pack(fill="x", ipady=8, pady=(0, 8))

        ModernButton(
            content,
            text="Buscar creados después de fecha",
            command=self.buscar_por_fecha,
            bg=self.colors["secondary"],
            hover_bg=self.colors["secondary_hover"],
            font=self.fonts["button"]
        ).pack(fill="x", pady=(0, 12))

        # Rango clases
        tk.Label(
            content,
            text="Rango de clases",
            font=self.fonts["subtitle"],
            fg=self.colors["text"],
            bg=self.colors["bg_card"]
        ).pack(anchor="w", pady=(0, 6))

        range_row = tk.Frame(content, bg=self.colors["bg_card"])
        range_row.pack(fill="x", pady=(0, 8))

        self.entry_min_clases = tk.Entry(
            range_row,
            font=self.fonts["text"],
            bg="white",
            fg=self.colors["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["primary"],
            bd=0
        )
        self.entry_min_clases.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 6))

        self.entry_max_clases = tk.Entry(
            range_row,
            font=self.fonts["text"],
            bg="white",
            fg=self.colors["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            highlightcolor=self.colors["primary"],
            bd=0
        )
        self.entry_max_clases.pack(side="left", fill="x", expand=True, ipady=8, padx=(6, 0))

        ModernButton(
            content,
            text="Buscar por rango de clases",
            command=self.buscar_por_rango_clases,
            bg=self.colors["secondary"],
            hover_bg=self.colors["secondary_hover"],
            font=self.fonts["button"]
        ).pack(fill="x", pady=(0, 12))

        tk.Label(
            content,
            text="Tipo de reseña",
            font=self.fonts["subtitle"],
            fg=self.colors["text"],
            bg=self.colors["bg_card"]
        ).pack(anchor="w", pady=(0, 6))

        self.combo_review = tk.StringVar(value="positive")
        combo_frame = tk.Frame(
            content,
            bg="white",
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        combo_frame.pack(fill="x", pady=(0, 8))

        self.review_menu = tk.OptionMenu(
            combo_frame,
            self.combo_review,
            "positive",
            "negative",
            "neutral"
        )
        self.review_menu.config(
            font=self.fonts["text"],
            bg="white",
            fg=self.colors["text"],
            activebackground=self.colors["bg_card_alt"],
            activeforeground=self.colors["text"],
            relief="flat",
            bd=0,
            highlightthickness=0
        )
        self.review_menu["menu"].config(
            font=self.fonts["text"],
            bg="white",
            fg=self.colors["text"],
            activebackground=self.colors["bg_card_alt"],
            activeforeground=self.colors["text"]
        )
        self.review_menu.pack(fill="x")

        ModernButton(
            content,
            text="Buscar reseñas sobre promedio",
            command=self.buscar_reviews_promedio,
            bg=self.colors["purple"],
            hover_bg=self.colors["purple_hover"],
            font=self.fonts["button"]
        ).pack(fill="x")

    def _crear_estado_card(self, parent):
        content = tk.Frame(parent, bg=self.colors["bg_card"])
        content.pack(fill="x", padx=16, pady=(14, 16))

        legend_items = [
            ("Nodo raíz", "#93C5FD"),
            ("Nodo normal", "#BFDBFE"),
            ("Nodo encontrado / seleccionado", "#FDE68A"),
            ("Nodo desbalanceado", "#FCA5A5"),
            ("Acción importante", "#F59E0B"),
        ]

        tk.Label(
            content,
            text="Referencia visual",
            font=self.fonts["subtitle"],
            fg=self.colors["text"],
            bg=self.colors["bg_card"]
        ).pack(anchor="w", pady=(0, 8))

        for text, color in legend_items:
            row = tk.Frame(content, bg=self.colors["bg_card"])
            row.pack(fill="x", pady=3)

            sample = tk.Canvas(row, width=18, height=18, bg=self.colors["bg_card"], highlightthickness=0)
            sample.pack(side="left")
            sample.create_oval(2, 2, 16, 16, fill=color, outline="#64748B", width=1)

            tk.Label(
                row,
                text=text,
                font=self.fonts["text"],
                fg=self.colors["text"],
                bg=self.colors["bg_card"]
            ).pack(side="left", padx=8)

        tk.Label(
            content,
            text="Tip: usa “Balancear árbol” cuando el árbol crezca mucho hacia un lado.",
            font=self.fonts["text_small"],
            fg=self.colors["muted"],
            bg=self.colors["bg_card"],
            justify="left",
            wraplength=280
        ).pack(anchor="w", pady=(12, 0))

    def _crear_visualizacion(self):
        # Título de visualización
        vis_header = tk.Frame(self.center_area, bg=self.colors["bg_main"])
        vis_header.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        tk.Label(
            vis_header,
            text="Visualización del árbol",
            font=("Segoe UI", 16, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg_main"]
        ).pack(side="left")



        # Tarjeta de visualización
        visual_card = tk.Frame(
            self.center_area,
            bg=self.colors["bg_card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        visual_card.grid(row=1, column=0, sticky="nsew")
        visual_card.grid_rowconfigure(0, weight=1)
        visual_card.grid_columnconfigure(0, weight=1)
        # Canvas con scroll
        tree_frame = tk.Frame(visual_card, bg=self.colors["bg_card_alt"])
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        self.tree_canvas = tk.Canvas(
            tree_frame,
            bg="#FCFDFE",
            highlightbackground=self.colors["border"],
            highlightthickness=1,
            bd=0
        )
        self.tree_canvas.pack(side="left", fill="both", expand=True)

        y_scroll = tk.Scrollbar(tree_frame, orient="vertical", command=self.tree_canvas.yview)
        y_scroll.pack(side="right", fill="y")

        x_scroll = tk.Scrollbar(visual_card, orient="horizontal", command=self.tree_canvas.xview)
        x_scroll.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 14))

        self.tree_canvas.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        self.tree_canvas.bind("<Configure>", self._centrar_imagen_arbol)

    def _crear_salida(self):
        top = tk.Frame(self.bottom_area, bg=self.colors["bg_card"])
        top.pack(fill="x", padx=18, pady=(14, 8))

        tk.Label(
            top,
            text="Salida / resultados",
            font=("Segoe UI", 14, "bold"),
            fg=self.colors["text"],
            bg=self.colors["bg_card"]
        ).pack(side="left")



        self.txt_salida = ScrolledText(
            self.bottom_area,
            height=11,
            wrap="word",
            font=self.fonts["output"],
            bg=self.colors["output_bg"],
            fg=self.colors["text"],
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=self.colors["border"],
            insertbackground=self.colors["text"],
            padx=14,
            pady=12
        )
        self.txt_salida.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.txt_salida.tag_configure("ok", foreground=self.colors["ok"])
        self.txt_salida.tag_configure("error", foreground=self.colors["error"])
        self.txt_salida.tag_configure("info", foreground=self.colors["info"])
        self.txt_salida.tag_configure("warning", foreground=self.colors["warning"])
        self.txt_salida.tag_configure("divider", foreground="#94A3B8")

    def _crear_card(self, parent, title):
        wrapper = tk.Frame(
            parent,
            bg=self.colors["bg_card"],
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        wrapper.pack(fill="x", padx=16, pady=(0, 14))

        title_bar = tk.Frame(wrapper, bg=self.colors["bg_card"])
        title_bar.pack(fill="x", padx=16, pady=(14, 0))

        tk.Label(
            title_bar,
            text=title,
            font=self.fonts["section"],
            fg=self.colors["text"],
            bg=self.colors["bg_card"]
        ).pack(anchor="w")

        return wrapper

    # ==================================================
    # OPERACIONES BÁSICAS
    # ==================================================
    def insertar_nodo(self):
        try:
            course_id = int(self.entry_id.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            self._escribir("[ERROR] El ID debe ser un número entero.", "error")
            return

        ok = self.arbol.insert(course_id)
        if ok:
            self.highlighted_node_id = course_id
            self.selected_node_id = course_id
            self._escribir(f"[OK] Se insertó el curso con ID {course_id}.", "ok")
            self._actualizar_vista_arbol()
        else:
            self._escribir(f"[ERROR] No se pudo insertar el curso con ID {course_id}.", "error")

    def eliminar_nodo(self):
        try:
            course_id = int(self.entry_id.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            self._escribir("[ERROR] El ID debe ser un número entero.", "error")
            return

        ok = self.arbol.delete_by_id(course_id)
        if ok:
            if self.highlighted_node_id == course_id:
                self.highlighted_node_id = None
            if self.selected_node_id == course_id:
                self.selected_node_id = None
            self._escribir(f"[OK] Se eliminó el curso con ID {course_id}.", "ok")
            self._actualizar_vista_arbol()
        else:
            self._escribir(f"[ERROR] No se encontró el curso con ID {course_id} para eliminar.", "error")

    def buscar_nodo(self):
        try:
            course_id = int(self.entry_id.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            self._escribir("[ERROR] El ID debe ser un número entero.", "error")
            return

        node = self.arbol.find(course_id)
        if node:
            self.highlighted_node_id = course_id
            self.selected_node_id = course_id
            salida = [
                "[INFO] Nodo encontrado:",
                f"ID: {node.data[0]}",
                f"Satisfacción: {node.data[1]:.5f}",
                f"Nivel: {self.arbol.get_node_level(node)}",
                f"Factor de balanceo: {self.arbol.get_balance_factor(node)}"
            ]

            padre = self.arbol.get_parent(node)
            abuelo = self.arbol.get_grandparent(node)
            tio = self.arbol.get_uncle(node)

            salida.append(f"Padre: {padre.data[0] if padre else 'No tiene'}")
            salida.append(f"Abuelo: {abuelo.data[0] if abuelo else 'No tiene'}")
            salida.append(f"Tío: {tio.data[0] if tio else 'No tiene'}")

            self._escribir("\n".join(salida), "info")
            self._actualizar_vista_arbol()
        else:
            self.highlighted_node_id = None
            self._escribir("[ERROR] Nodo no encontrado.", "error")
            self._actualizar_vista_arbol()

    def mostrar_bfs(self):
        niveles = self.arbol.level_order_traversal()
        if not niveles:
            self._escribir("[INFO] El árbol está vacío.", "info")
            return

        texto = ["[INFO] Recorrido por niveles:"]
        for i, nivel in enumerate(niveles):
            texto.append(f"Nivel {i}: {nivel}")
        self._escribir("\n".join(texto), "info")

    def mostrar_info_completa(self):
        try:
            course_id = int(self.entry_id.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            self._escribir("[ERROR] El ID debe ser un número entero.", "error")
            return

        info = self.arbol.get_course_full_info(course_id)
        if info:
            self.highlighted_node_id = course_id
            self.selected_node_id = course_id
            texto = ["[INFO] Información completa del curso:"]
            for k, v in info.items():
                texto.append(f"{k}: {v}")
            self._escribir("\n".join(texto), "info")
            self._actualizar_vista_arbol()
        else:
            self._escribir("[ERROR] No se encontró información para ese curso.", "error")

    def balancear_arbol(self):
        if self.arbol.root is None:
            self._escribir("[INFO] El árbol está vacío. No hay nada que balancear.", "info")
            return

        if hasattr(self.arbol, "rebalance"):
            ok = self.arbol.rebalance()
            if ok:
                self._escribir("[OK] El árbol fue balanceado correctamente.", "ok")
                self._actualizar_vista_arbol()
            else:
                self._escribir("[ERROR] No se pudo balancear el árbol.", "error")
        else:
            self._escribir("[ERROR] El método rebalance() no existe en Arbol.py.", "error")

    # ==================================================
    # BÚSQUEDAS POR CRITERIO
    # ==================================================
    def buscar_positivos_mayores(self):
        resultados = self.arbol.search_by_positive_reviews_criterion()
        self._mostrar_lista_nodos("Cursos con positivas > (negativas + neutras)", resultados)

    def buscar_por_fecha(self):
        fecha = self.entry_fecha.get().strip()
        try:
            resultados = self.arbol.search_by_creation_date(fecha)
            self._mostrar_lista_nodos(f"Cursos creados después de {fecha}", resultados)
        except ValueError:
            messagebox.showerror("Error", "La fecha debe tener formato YYYY-MM-DD.")
            self._escribir("[ERROR] La fecha debe tener formato YYYY-MM-DD.", "error")

    def buscar_por_rango_clases(self):
        try:
            minimo = int(self.entry_min_clases.get().strip())
            maximo = int(self.entry_max_clases.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Los valores del rango deben ser enteros.")
            self._escribir("[ERROR] Los valores del rango deben ser enteros.", "error")
            return

        resultados = self.arbol.search_by_classes_range(minimo, maximo)
        self._mostrar_lista_nodos(
            f"Cursos con número de clases entre {minimo} y {maximo}",
            resultados
        )

    def buscar_reviews_promedio(self):
        review_type = self.combo_review.get()
        resultados = self.arbol.search_by_reviews_above_average(review_type)
        self._mostrar_lista_nodos(
            f"Cursos con reseñas '{review_type}' por encima del promedio",
            resultados
        )

    # ==================================================
    # UTILIDADES DE SALIDA
    # ==================================================
    def _mostrar_lista_nodos(self, titulo, resultados):
        if not resultados:
            self._escribir(f"[INFO] {titulo}\nNo se encontraron nodos.", "info")
            return

        lineas = [f"[INFO] {titulo}", f"Total encontrados: {len(resultados)}"]
        for i, node in enumerate(resultados, start=1):
            lineas.append(f"{i}. ID: {node.data[0]} | Satisfacción: {node.data[1]:.5f}")
        lineas.append("\nEscribe el número del nodo para ver sus detalles, o deja vacío para omitir.")

        self._escribir("\n".join(lineas), "info")
        self._actualizar_vista_arbol()

        # Ventana de selección
        self._abrir_ventana_seleccion(titulo, resultados)

    def _abrir_ventana_seleccion(self, titulo, resultados):
        """Abre una ventana con la lista de nodos encontrados para que el
        usuario seleccione uno y realice operaciones sobre él."""
        import tkinter as tk

        ventana = tk.Toplevel(self.root)
        ventana.title("Seleccionar nodo")
        ventana.geometry("520x520")
        ventana.configure(bg="#F5F7FA")
        ventana.grab_set()

        tk.Label(ventana, text=titulo, font=("Segoe UI", 12, "bold"),
                 bg="#F5F7FA", fg="#1F2937").pack(padx=16, pady=(16, 4))
        tk.Label(ventana, text="Selecciona un nodo para ver sus propiedades:",
                 font=("Segoe UI", 10), bg="#F5F7FA", fg="#6B7280").pack(padx=16)

        frame_lista = tk.Frame(ventana, bg="#F5F7FA")
        frame_lista.pack(fill="both", expand=True, padx=16, pady=8)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(frame_lista, font=("Consolas", 10),
                             bg="white", fg="#1F2937",
                             selectbackground="#3B82F6", selectforeground="white",
                             yscrollcommand=scrollbar.set, relief="flat",
                             highlightthickness=1, highlightbackground="#D7DEE8")
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        for i, node in enumerate(resultados, start=1):
            listbox.insert("end", f"{i:>3}. ID: {node.data[0]}  |  Sat: {node.data[1]:.5f}")

        def seleccionar():
            seleccion = listbox.curselection()
            if not seleccion:
                return
            idx = seleccion[0]
            nodo_sel = resultados[idx]
            nid = nodo_sel.data[0]
            self.highlighted_node_id = nid
            self.selected_node_id = nid
            self._actualizar_vista_arbol()
            self._mostrar_propiedades_nodo(nodo_sel)
            ventana.destroy()

        ModernButton(ventana, text="Ver propiedades del nodo seleccionado",
                     command=seleccionar).pack(fill="x", padx=16, pady=(0, 8))
        ModernButton(ventana, text="Cerrar", command=ventana.destroy,
                     bg="#CBD5E1", hover_bg="#94A3B8", fg="#1F2937",
                     active_fg="white").pack(fill="x", padx=16, pady=(0, 16))

    def _mostrar_propiedades_nodo(self, node):
        """Muestra un panel completo de propiedades de un nodo seleccionado."""
        import tkinter as tk

        nid = node.data[0]
        ventana = tk.Toplevel(self.root)
        ventana.title(f"Propiedades del nodo ID {nid}")
        ventana.geometry("480x520")
        ventana.configure(bg="#F5F7FA")
        ventana.grab_set()

        # Datos del árbol
        nivel = self.arbol.get_node_level(node)
        balance = self.arbol.get_balance_factor(node)
        padre = self.arbol.get_parent(node)
        abuelo = self.arbol.get_grandparent(node)
        tio = self.arbol.get_uncle(node)
        info = self.arbol.get_course_full_info(nid)

        from tkinter.scrolledtext import ScrolledText
        txt = ScrolledText(ventana, font=("Consolas", 10), bg="white",
                           fg="#1F2937", relief="flat", padx=14, pady=12,
                           highlightthickness=1, highlightbackground="#D7DEE8")
        txt.pack(fill="both", expand=True, padx=16, pady=16)

        lineas = [
            f"=== PROPIEDADES DEL NODO ===",
            f"ID:                {nid}",
            f"Satisfacción:      {node.data[1]:.5f}",
            f"Nivel en el árbol: {nivel}",
            f"Factor de balance: {balance}",
            f"Padre:             {padre.data[0] if padre else 'No tiene (es raíz)'}",
            f"Abuelo:            {abuelo.data[0] if abuelo else 'No tiene'}",
            f"Tío:               {tio.data[0] if tio else 'No tiene'}",
        ]

        if info:
            lineas += [
                "",
                "=== INFORMACIÓN COMPLETA DEL CURSO ===",
                f"Título:    {info.get('title', 'N/A')}",
                f"Rating:    {info.get('rating', 'N/A')}",
                f"Reviews:   {info.get('num_reviews', 'N/A')}",
                f"Clases:    {info.get('num_published_lectures', 'N/A')}",
                f"Creado:    {info.get('created', 'N/A')}",
                f"Actualiz.: {info.get('last_update_date', 'N/A')}",
                f"Duración:  {info.get('duration', 'N/A')}",
                f"Positivas: {info.get('positive_reviews', 'N/A')}",
                f"Negativas: {info.get('negative_reviews', 'N/A')}",
                f"Neutras:   {info.get('neutral_reviews', 'N/A')}",
            ]

        txt.insert("end", "\n".join(lineas))
        txt.configure(state="disabled")

        ModernButton(ventana, text="Cerrar", command=ventana.destroy,
                     bg="#CBD5E1", hover_bg="#94A3B8", fg="#1F2937",
                     active_fg="white").pack(fill="x", padx=16, pady=(0, 16))

    def _escribir(self, texto, tipo="info"):
        self.txt_salida.insert("end", texto + "\n", tipo)
        self.txt_salida.insert("end", "─" * 72 + "\n", "divider")
        self.txt_salida.see("end")

    def limpiar_salida(self):
        self.txt_salida.delete("1.0", "end")
        self._escribir("[INFO] Salida limpiada.", "info")

    # ==================================================
    # VISUALIZACIÓN GRAPHVIZ
    # ==================================================
    def _actualizar_vista_arbol(self):
        if self.arbol.root is None:
            self.tree_canvas.delete("all")
            self.tree_canvas.create_text(
                400, 220,
                text="Árbol vacío",
                fill=self.colors["muted"],
                font=("Segoe UI", 18, "bold")
            )
            self.tree_canvas.configure(scrollregion=(0, 0, 800, 800))
            return

        try:
            ruta_png = self._generar_imagen_graphviz()
            self.tree_image = tk.PhotoImage(file=ruta_png)

            self.tree_canvas.delete("all")
            self.tree_canvas.create_image(0, 0, image=self.tree_image, anchor="nw", tags="tree_img")

            width = self.tree_image.width()
            height = self.tree_image.height()
            self.tree_canvas.configure(scrollregion=(0, 0, width + 40, height + 40))
            self._centrar_imagen_arbol()

            total_nodes = len(self.arbol.all_nodes) if hasattr(self.arbol, "all_nodes") else "?"
        except Exception as e:
            self.tree_canvas.delete("all")
            self.tree_canvas.create_text(
                450, 220,
                text=f"No se pudo generar la imagen del árbol.\n{str(e)}",
                fill=self.colors["error"],
                font=("Segoe UI", 12, "bold"),
                justify="center"
            )
            self.tree_canvas.configure(scrollregion=(0, 0, 900, 800))

    def _centrar_imagen_arbol(self, _event=None):
        if self.tree_image is None:
            return

        canvas_w = self.tree_canvas.winfo_width()
        canvas_h = self.tree_canvas.winfo_height()
        img_w = self.tree_image.width()
        img_h = self.tree_image.height()

        x = max((canvas_w - img_w) // 2, 20)
        y = 20

        self.tree_canvas.delete("tree_img")
        self.tree_canvas.create_image(x, y, image=self.tree_image, anchor="nw", tags="tree_img")
        self.tree_canvas.configure(scrollregion=(0, 0, max(canvas_w, img_w + 40), max(canvas_h, img_h + 40)))

    def _generar_imagen_graphviz(self):
        dot = Digraph(comment="Árbol Binario de Búsqueda")
        dot.attr(rankdir='TB', splines='true', nodesep='0.3', ranksep='0.5')
        dot.attr(bgcolor="transparent")
        dot.attr('graph', dpi='90')

        self._agregar_nodos_y_aristas(dot, self.arbol.root, is_root=True)

        archivo_base = os.path.join(self.temp_dir, "arbol_actual")
        ruta_generada = dot.render(filename=archivo_base, format='png', cleanup=True)
        return ruta_generada

    def _agregar_nodos_y_aristas(self, dot, nodo, is_root=False):
        if nodo is None:
            return

        nombre_nodo = f"node_{id(nodo)}"
        node_id = nodo.data[0]
        balance = self.arbol.get_balance_factor(nodo)

        # Colores por estado
        fill = "#BFDBFE"          # normal
        border = "#5B7C99"
        font_color = "#1F2937"
        penwidth = "1.5"

        if is_root:
            fill = "#93C5FD"      # raíz
            border = "#2563EB"
            penwidth = "2.0"

        if abs(balance) > 1:
            fill = "#FCA5A5"      # desbalanceado
            border = "#DC2626"

        if self.highlighted_node_id == node_id or self.selected_node_id == node_id:
            fill = "#FDE68A"      # encontrado / seleccionado
            border = "#D97706"
            penwidth = "2.3"

        # Obtener titulo del curso
        try:
            info = self.arbol.get_course_full_info(nodo.data[0])
            titulo = info['title'] if info and info.get('title') else ""
        except Exception:
            titulo = ""

        if titulo:
            etiqueta = f"{titulo}\\nID: {nodo.data[0]}\\nSat: {nodo.data[1]:.5f}"
        else:
            etiqueta = f"ID: {nodo.data[0]}\\nSat: {nodo.data[1]:.5f}"

        dot.node(
            nombre_nodo,
            etiqueta,
            shape="box",
            style="filled,rounded",
            fillcolor=fill,
            color=border,
            fontcolor=font_color,
            fontname="Arial",
            fontsize="9",
            penwidth=penwidth,
            margin="0.06"
        )

        if nodo.left:
            nombre_izq = f"node_{id(nodo.left)}"
            self._agregar_nodos_y_aristas(dot, nodo.left, is_root=False)
            dot.edge(
                nombre_nodo,
                nombre_izq,
                color="#94A3B8",
                penwidth="1.4"
            )
        else:
            null_izq = f"null_left_{id(nodo)}"
            dot.node(null_izq, "", shape="point", width="0.08", color="#CBD5E1")
            dot.edge(nombre_nodo, null_izq, color="#E2E8F0", style="dashed")

        if nodo.right:
            nombre_der = f"node_{id(nodo.right)}"
            self._agregar_nodos_y_aristas(dot, nodo.right, is_root=False)
            dot.edge(
                nombre_nodo,
                nombre_der,
                color="#94A3B8",
                penwidth="1.4"
            )
        else:
            null_der = f"null_right_{id(nodo)}"
            dot.node(null_der, "", shape="point", width="0.08", color="#CBD5E1")
            dot.edge(nombre_nodo, null_der, color="#E2E8F0", style="dashed")