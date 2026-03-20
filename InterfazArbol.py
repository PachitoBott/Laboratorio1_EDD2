
import os
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

from graphviz import Digraph

import Arbol


class InterfazArbol:
    def __init__(self, root):
        self.root = root
        self.root.title("Laboratorio 1 - Árbol Binario de Búsqueda")
        self.root.geometry("1200x700")

        self.arbol = Arbol.Arbol()
        self.temp_dir = tempfile.mkdtemp(prefix="abb_graphviz_")
        self.tree_image = None

        self._crear_componentes()
        self._actualizar_vista_arbol()

    def _crear_componentes(self):
        contenedor = ttk.Frame(self.root, padding=10)
        contenedor.pack(fill="both", expand=True)

        panel_izquierdo = ttk.Frame(contenedor)
        panel_izquierdo.pack(side="left", fill="y", padx=(0, 10))

        panel_derecho = ttk.Frame(contenedor)
        panel_derecho.pack(side="right", fill="both", expand=True)

        # -------------------------------
        # Panel de controles
        # -------------------------------
        ttk.Label(panel_izquierdo, text="Operaciones", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))

        ttk.Label(panel_izquierdo, text="ID del curso:").pack(anchor="w")
        self.entry_id = ttk.Entry(panel_izquierdo, width=25)
        self.entry_id.pack(anchor="w", pady=(0, 10))

        ttk.Button(panel_izquierdo, text="Insertar nodo", command=self.insertar_nodo).pack(fill="x", pady=3)
        ttk.Button(panel_izquierdo, text="Eliminar nodo por ID", command=self.eliminar_nodo).pack(fill="x", pady=3)
        ttk.Button(panel_izquierdo, text="Buscar nodo por ID", command=self.buscar_nodo).pack(fill="x", pady=3)
        ttk.Button(panel_izquierdo, text="Mostrar recorrido por niveles", command=self.mostrar_bfs).pack(fill="x", pady=3)
        ttk.Button(panel_izquierdo, text="Mostrar información completa", command=self.mostrar_info_completa).pack(fill="x", pady=3)
        ttk.Button(panel_izquierdo, text="Actualizar árbol", command=self._actualizar_vista_arbol).pack(fill="x", pady=3)
        ttk.Button(panel_izquierdo, text="Limpiar salida", command=self.limpiar_salida).pack(fill="x", pady=3)

        ttk.Separator(panel_izquierdo, orient="horizontal").pack(fill="x", pady=10)

        ttk.Label(panel_izquierdo, text="Búsquedas por criterio", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 10))

        ttk.Button(
            panel_izquierdo,
            text="Positivas > (Negativas + Neutras)",
            command=self.buscar_positivos_mayores
        ).pack(fill="x", pady=3)

        fecha_frame = ttk.Frame(panel_izquierdo)
        fecha_frame.pack(fill="x", pady=3)
        ttk.Label(fecha_frame, text="Fecha (YYYY-MM-DD):").pack(anchor="w")
        self.entry_fecha = ttk.Entry(fecha_frame)
        self.entry_fecha.pack(fill="x")

        ttk.Button(
            panel_izquierdo,
            text="Buscar creados después de fecha",
            command=self.buscar_por_fecha
        ).pack(fill="x", pady=3)

        rango_frame = ttk.Frame(panel_izquierdo)
        rango_frame.pack(fill="x", pady=3)
        ttk.Label(rango_frame, text="Rango de clases").pack(anchor="w")
        self.entry_min_clases = ttk.Entry(rango_frame)
        self.entry_min_clases.pack(fill="x", pady=1)
        self.entry_max_clases = ttk.Entry(rango_frame)
        self.entry_max_clases.pack(fill="x", pady=1)

        ttk.Button(
            panel_izquierdo,
            text="Buscar por rango de clases",
            command=self.buscar_por_rango_clases
        ).pack(fill="x", pady=3)

        ttk.Label(panel_izquierdo, text="Tipo de reseña:").pack(anchor="w", pady=(8, 0))
        self.combo_review = ttk.Combobox(
            panel_izquierdo,
            state="readonly",
            values=["positive", "negative", "neutral"]
        )
        self.combo_review.set("positive")
        self.combo_review.pack(fill="x", pady=(0, 5))

        ttk.Button(
            panel_izquierdo,
            text="Buscar reseñas sobre promedio",
            command=self.buscar_reviews_promedio
        ).pack(fill="x", pady=3)

        # -------------------------------
        # Panel del árbol
        # -------------------------------
        ttk.Label(panel_derecho, text="Visualización del árbol", font=("Arial", 14, "bold")).pack(anchor="w")

        self.label_imagen = ttk.Label(panel_derecho, text="Árbol vacío")
        self.label_imagen.pack(fill="both", expand=False, pady=10)

        ttk.Label(panel_derecho, text="Salida / resultados", font=("Arial", 12, "bold")).pack(anchor="w")
        self.txt_salida = ScrolledText(panel_derecho, height=18, wrap="word")
        self.txt_salida.pack(fill="both", expand=True)

    # ==================================================
    # Operaciones básicas
    # ==================================================
    def insertar_nodo(self):
        try:
            course_id = int(self.entry_id.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return

        ok = self.arbol.insert(course_id)
        if ok:
            self._escribir(f"Se insertó el curso con ID {course_id}.")
            self._actualizar_vista_arbol()
        else:
            self._escribir(f"No se pudo insertar el curso con ID {course_id}.")

    def eliminar_nodo(self):
        try:
            course_id = int(self.entry_id.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return

        ok = self.arbol.delete_by_id(course_id)
        if ok:
            self._escribir(f"Se eliminó el curso con ID {course_id}.")
            self._actualizar_vista_arbol()
        else:
            self._escribir(f"No se encontró el curso con ID {course_id} para eliminar.")

    def buscar_nodo(self):
        try:
            course_id = int(self.entry_id.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return

        node = self.arbol.find(course_id)
        if node:
            salida = [
                "Nodo encontrado:",
                f"ID: {node.data[0]}",
                f"Satisfacción: {node.data[1]:.4f}",
                f"Nivel: {self.arbol.get_node_level(node)}",
                f"Factor de balanceo: {self.arbol.get_balance_factor(node)}"
            ]

            padre = self.arbol.get_parent(node)
            abuelo = self.arbol.get_grandparent(node)
            tio = self.arbol.get_uncle(node)

            salida.append(f"Padre: {padre.data[0] if padre else 'No tiene'}")
            salida.append(f"Abuelo: {abuelo.data[0] if abuelo else 'No tiene'}")
            salida.append(f"Tío: {tio.data[0] if tio else 'No tiene'}")

            self._escribir("\n".join(salida))
        else:
            self._escribir("Nodo no encontrado.")

    def mostrar_bfs(self):
        niveles = self.arbol.level_order_traversal()
        if not niveles:
            self._escribir("El árbol está vacío.")
            return

        texto = ["Recorrido por niveles:"]
        for i, nivel in enumerate(niveles):
            texto.append(f"Nivel {i}: {nivel}")
        self._escribir("\n".join(texto))

    def mostrar_info_completa(self):
        try:
            course_id = int(self.entry_id.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return

        info = self.arbol.get_course_full_info(course_id)
        if info:
            texto = ["Información completa del curso:"]
            for k, v in info.items():
                texto.append(f"{k}: {v}")
            self._escribir("\n".join(texto))
        else:
            self._escribir("No se encontró información para ese curso.")

    # ==================================================
    # Búsquedas por criterio
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

    def buscar_por_rango_clases(self):
        try:
            minimo = int(self.entry_min_clases.get().strip())
            maximo = int(self.entry_max_clases.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Los valores del rango deben ser enteros.")
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
    # Utilidades de salida
    # ==================================================
    def _mostrar_lista_nodos(self, titulo, resultados):
        if not resultados:
            self._escribir(f"{titulo}\nNo se encontraron nodos.")
            return

        lineas = [titulo, f"Total encontrados: {len(resultados)}"]
        for i, node in enumerate(resultados, start=1):
            lineas.append(f"{i}. ID: {node.data[0]} | Satisfacción: {node.data[1]:.4f}")
        self._escribir("\n".join(lineas))

    def _escribir(self, texto):
        self.txt_salida.insert("end", texto + "\n" + ("-" * 60) + "\n")
        self.txt_salida.see("end")

    def limpiar_salida(self):
        self.txt_salida.delete("1.0", "end")

    # ==================================================
    # Graphviz
    # ==================================================
    def _actualizar_vista_arbol(self):
        if self.arbol.root is None:
            self.label_imagen.configure(text="Árbol vacío", image="")
            self.tree_image = None
            return

        try:
            ruta_png = self._generar_imagen_graphviz()
            self.tree_image = tk.PhotoImage(file=ruta_png)
            self.label_imagen.configure(image=self.tree_image, text="")
        except Exception as e:
            self.label_imagen.configure(
                text=f"No se pudo generar la imagen del árbol.\n{str(e)}",
                image=""
            )
            self.tree_image = None

    def _generar_imagen_graphviz(self):
        dot = Digraph(comment="Árbol Binario de Búsqueda")
        dot.attr(rankdir='TB')
        dot.attr('node', shape='circle', style='filled', fillcolor='lightblue', fontname='Arial')

        self._agregar_nodos_y_aristas(dot, self.arbol.root)

        archivo_base = os.path.join(self.temp_dir, "arbol_actual")
        ruta_generada = dot.render(filename=archivo_base, format='png', cleanup=True)
        return ruta_generada

    def _agregar_nodos_y_aristas(self, dot, nodo):
        if nodo is None:
            return

        nombre_nodo = f"node_{id(nodo)}"
        etiqueta = f"ID: {nodo.data[0]}\\nSat: {nodo.data[1]:.2f}"
        dot.node(nombre_nodo, etiqueta)

        if nodo.left:
            nombre_izq = f"node_{id(nodo.left)}"
            self._agregar_nodos_y_aristas(dot, nodo.left)
            dot.edge(nombre_nodo, nombre_izq)
        else:
            null_izq = f"null_left_{id(nodo)}"
            dot.node(null_izq, "", shape="point")
            dot.edge(nombre_nodo, null_izq)

        if nodo.right:
            nombre_der = f"node_{id(nodo.right)}"
            self._agregar_nodos_y_aristas(dot, nodo.right)
            dot.edge(nombre_nodo, nombre_der)
        else:
            null_der = f"null_right_{id(nodo)}"
            dot.node(null_der, "", shape="point")
            dot.edge(nombre_nodo, null_der)