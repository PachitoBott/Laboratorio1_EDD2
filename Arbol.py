import csv
import os
from datetime import datetime
# deque ya no es necesario: BFS implementado recursivamente
import Nodo

# Ruta absoluta al CSV, funciona sin importar el directorio de trabajo
_CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset_courses_with_reviews.csv')

class Arbol:
    def __init__(self, root=None):
        self.root = root
        self.all_nodes = []

    def insert(self, course_id):
        satisfaction_level = self.calculate_satisfaction_level(course_id)
        if satisfaction_level is None:
            print(f"Course ID {course_id} not found.")
            return

        new_node = Nodo.Nodo((course_id, satisfaction_level))

        if self.root is None:
            self.root = new_node
            self.all_nodes.append(new_node)
        else:
            self.__insert_recursively(self.root, new_node)
            self.all_nodes.append(new_node)
        
   # =========================
    # RECORRIDOS
    # =========================

    def __preorder_recursivo(self, node):
         if node is not None:
            print(node.data)
            self.__preorder_recursivo(node.left)
            self.__preorder_recursivo(node.right)

    # =========================
    # DATOS DEL CSV
    # =========================
    def get_course_data(self, course_id):
        csv_path = _CSV_PATH
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == str(course_id):
                    return {
                        'rating': float(row['rating']),
                        'positive_reviews': int(row['positive_reviews']),
                        'neutral_reviews': int(row['neutral_reviews']),
                        'negative_reviews': int(row['negative_reviews']),
                        'number_of_reviews': int(row['num_reviews'])
                    }
        return None

    def calculate_satisfaction_level(self, course_id):
        data = self.get_course_data(course_id)
        if data is None:
            return None

        satisfaction = (
            (data['rating'] * 0.7)
            + (
                ((5 * data['positive_reviews'])
                + (3 * data['neutral_reviews'])
                + data['negative_reviews']) / data['number_of_reviews']
            ) * 0.3
        )
        return satisfaction

    # =========================
    # INSERCIÓN
    # =========================
    def insert(self, course_id):
        # Evitar duplicados por ID
        if self.find(course_id) is not None:
            print(f"El curso con ID {course_id} ya existe en el árbol.")
            return False

        satisfaction_level = self.calculate_satisfaction_level(course_id)
        if satisfaction_level is None:
            print(f"Course ID {course_id} not found.")
            return False

        new_node = Nodo.Nodo((course_id, satisfaction_level))

        if self.root is None:
            self.root = new_node
            self.all_nodes.append(new_node)
            return True
        else:
            self.__insert_recursively(self.root, new_node)
            self.all_nodes.append(new_node)
            self.rebalance()  # Auto-balanceo trucho
            return True

    def __insert_recursively(self, current_node, new_node):
        # El árbol está ordenado por satisfacción
        if new_node.data[1] < current_node.data[1]:
            if current_node.left is None:
                current_node.left = new_node
                new_node.parent = current_node
            else:
                self.__insert_recursively(current_node.left, new_node)
        else:
            if current_node.right is None:
                current_node.right = new_node
                new_node.parent = current_node
            else:
                self.__insert_recursively(current_node.right, new_node)

    # =========================
    # ELIMINACIÓN
    # =========================
    def __find_min(self, node):
        current = node
        while current and current.left is not None:
            current = current.left
        return current

    def __delete_recursively_by_key(self, current_node, satisfaction_level, course_id=None, tolerance=0.0001):
        """
        Elimina respetando el orden real del árbol: satisfacción.
        Si course_id se envía, sirve para distinguir nodos con misma satisfacción.
        """
        if current_node is None:
            return None, False

        deleted = False

        if satisfaction_level < current_node.data[1] - tolerance:
            current_node.left, deleted = self.__delete_recursively_by_key(
                current_node.left, satisfaction_level, course_id, tolerance
            )
            if current_node.left:
                current_node.left.parent = current_node

        elif satisfaction_level > current_node.data[1] + tolerance:
            current_node.right, deleted = self.__delete_recursively_by_key(
                current_node.right, satisfaction_level, course_id, tolerance
            )
            if current_node.right:
                current_node.right.parent = current_node

        else:
            # Misma satisfacción aproximada: validamos ID si fue suministrado
            if course_id is not None and current_node.data[0] != course_id:
                # Como los iguales se insertan a la derecha, seguimos buscando allí
                current_node.right, deleted = self.__delete_recursively_by_key(
                    current_node.right, satisfaction_level, course_id, tolerance
                )
                if current_node.right:
                    current_node.right.parent = current_node
                return current_node, deleted

            deleted = True

            # Caso 1: sin hijo izquierdo
            if current_node.left is None:
                replacement = current_node.right
                if replacement:
                    replacement.parent = current_node.parent
                return replacement, True

            # Caso 2: sin hijo derecho
            if current_node.right is None:
                replacement = current_node.left
                if replacement:
                    replacement.parent = current_node.parent
                return replacement, True

            # Caso 3: dos hijos
            successor = self.__find_min(current_node.right)
            current_node.data = successor.data

            current_node.right, _ = self.__delete_recursively_by_key(
                current_node.right, successor.data[1], successor.data[0], tolerance
            )
            if current_node.right:
                current_node.right.parent = current_node

        return current_node, deleted

    def delete_by_id(self, course_id):
        """
        Busca el nodo por ID con DFS, porque el árbol NO está ordenado por ID.
        Luego lo elimina usando la clave real del árbol: satisfacción.
        """
        node = self.find(course_id)
        if node is None:
            print(f"No se encontró nodo con ID {course_id}.")
            return False

        self.root, deleted = self.__delete_recursively_by_key(
            self.root, node.data[1], node.data[0]
        )

        if self.root:
            self.root.parent = None

        if deleted:
            self.all_nodes = [n for n in self.all_nodes if n.data[0] != course_id]
            self.rebalance()  # Auto-balanceo trucho
            print(f"Nodo con ID {course_id} eliminado.")
            return True

        print(f"No se pudo eliminar el nodo con ID {course_id}.")
        return False

    def delete_by_satisfaction(self, satisfaction_level):
        found_node = self.__find_by_satisfaction(self.root, satisfaction_level)
        if found_node:
            return self.delete_by_id(found_node.data[0])
        else:
            print(f"No se encontró nodo con satisfacción {satisfaction_level}")
            return False

    def __find_by_satisfaction(self, node, satisfaction_level, tolerance=0.01):
        if node is None:
            return None

        if abs(node.data[1] - satisfaction_level) < tolerance:
            return node

        left_result = self.__find_by_satisfaction(node.left, satisfaction_level, tolerance)
        if left_result:
            return left_result

        return self.__find_by_satisfaction(node.right, satisfaction_level, tolerance)

    # =========================
    # BÚSQUEDAS POR CRITERIO
    # =========================
    def search_by_positive_reviews_criterion(self):
        results = []
        self.__search_criterion_recursive(
            self.root,
            results,
            lambda n: self.__positive_reviews_criterion(n.data[0])
        )
        return results

    def __positive_reviews_criterion(self, course_id):
        data = self.get_course_data(course_id)
        if data:
            return data['positive_reviews'] > (data['negative_reviews'] + data['neutral_reviews'])
        return False

    def search_by_creation_date(self, target_date):
        results = []
        target_dt = datetime.strptime(target_date, '%Y-%m-%d')
        self.__search_criterion_recursive(
            self.root,
            results,
            lambda n: self.__date_criterion(n.data[0], target_dt)
        )
        return results

    def __date_criterion(self, course_id, target_date):
        csv_path = _CSV_PATH
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == str(course_id):
                    creation_date = datetime.strptime(row['created'][:10], '%Y-%m-%d')
                    return creation_date > target_date
        return False

    def search_by_classes_range(self, min_classes, max_classes):
        results = []
        self.__search_criterion_recursive(
            self.root,
            results,
            lambda n: self.__classes_range_criterion(n.data[0], min_classes, max_classes)
        )
        return results

    def __classes_range_criterion(self, course_id, min_val, max_val):
        csv_path = _CSV_PATH
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == str(course_id):
                    num_lectures = int(row['num_published_lectures'])
                    return min_val <= num_lectures <= max_val
        return False

    def search_by_reviews_above_average(self, review_type='positive'):
        average = self.__calculate_review_average(review_type)

        results = []
        self.__search_criterion_recursive(
            self.root,
            results,
            lambda n: self.__above_average_criterion(n.data[0], review_type, average)
        )
        return results

    def __calculate_review_average(self, review_type):
        if not self.all_nodes:
            return 0

        total = 0
        count = 0
        for node in self.all_nodes:
            data = self.get_course_data(node.data[0])
            if data:
                if review_type == 'positive':
                    total += data['positive_reviews']
                elif review_type == 'negative':
                    total += data['negative_reviews']
                elif review_type == 'neutral':
                    total += data['neutral_reviews']
                count += 1

        return total / count if count > 0 else 0

    def __above_average_criterion(self, course_id, review_type, average):
        data = self.get_course_data(course_id)
        if data:
            if review_type == 'positive':
                return data['positive_reviews'] > average
            elif review_type == 'negative':
                return data['negative_reviews'] > average
            elif review_type == 'neutral':
                return data['neutral_reviews'] > average
        return False

    def __search_criterion_recursive(self, node, results, criterion):
        if node is None:
            return

        if criterion(node):
            results.append(node)

        self.__search_criterion_recursive(node.left, results, criterion)
        self.__search_criterion_recursive(node.right, results, criterion)

    # =========================
    # BFS RECURSIVO
    # =========================
    def level_order_traversal(self):
        if self.root is None:
            print("El árbol está vacío.")
            return []

        levels = []
        self.__bfs_recursive([self.root], levels)

        for i, level in enumerate(levels):
            print(f"Nivel {i}: {[n for n in level]}")

        return levels

    def __bfs_recursive(self, current_level_nodes, levels):
        """Recorre el árbol por niveles de forma recursiva.
        current_level_nodes: lista de nodos del nivel actual.
        levels: lista acumuladora donde se añaden los IDs por nivel.
        """
        if not current_level_nodes:
            return

        ids_nivel = [node.data[0] for node in current_level_nodes]
        levels.append(ids_nivel)

        siguiente_nivel = []
        for node in current_level_nodes:
            if node.left:
                siguiente_nivel.append(node.left)
            if node.right:
                siguiente_nivel.append(node.right)

        self.__bfs_recursive(siguiente_nivel, levels)

    # =========================
    # OPERACIONES SOBRE NODOS
    # =========================
    def get_course_full_info(self, course_id):
        csv_path = _CSV_PATH
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == str(course_id):
                    return {
                        'id': row['id'],
                        'title': row['title'],
                        'rating': float(row['rating']),
                        'num_reviews': int(row['num_reviews']),
                        'num_published_lectures': int(row['num_published_lectures']),
                        'created': row['created'],
                        'last_update_date': row['last_update_date'],
                        'duration': row['duration'],
                        'positive_reviews': int(row['positive_reviews']),
                        'negative_reviews': int(row['negative_reviews']),
                        'neutral_reviews': int(row['neutral_reviews'])
                    }
        return None

    def get_node_level(self, node):
        return self.__get_level_recursive(self.root, node, 0)

    def __get_level_recursive(self, current_node, target_node, level):
        if current_node is None:
            return -1

        if current_node is target_node:
            return level

        left_level = self.__get_level_recursive(current_node.left, target_node, level + 1)
        if left_level != -1:
            return left_level

        return self.__get_level_recursive(current_node.right, target_node, level + 1)

    def get_balance_factor(self, node):
        left_height = self.__get_height(node.left)
        right_height = self.__get_height(node.right)
        return left_height - right_height

    def __get_height(self, node):
        if node is None:
            return 0
        return 1 + max(self.__get_height(node.left), self.__get_height(node.right))

    def get_parent(self, node):
        """Encuentra el padre del nodo de manera recursiva desde la raíz."""
        if node is None or node is self.root:
            return None
        return self.__find_parent_recursive(self.root, node)

    def __find_parent_recursive(self, current, target):
        if current is None:
            return None
        if current.left is target or current.right is target:
            return current
        left_result = self.__find_parent_recursive(current.left, target)
        if left_result:
            return left_result
        return self.__find_parent_recursive(current.right, target)

    def get_grandparent(self, node):
        """Encuentra el abuelo del nodo de manera recursiva desde la raíz."""
        parent = self.get_parent(node)
        if parent is None:
            return None
        return self.get_parent(parent)

    def get_uncle(self, node):
        """Encuentra el tío del nodo de manera recursiva desde la raíz."""
        parent = self.get_parent(node)
        if parent is None:
            return None
        grandparent = self.get_parent(parent)
        if grandparent is None:
            return None
        if grandparent.left is parent:
            return grandparent.right
        return grandparent.left

    # =========================
    # REBALANCEO MANUAL
    # =========================
    def rebalance(self):
        """Reconstruye el árbol como un BST perfectamente balanceado
        usando el recorrido inorder existente (ordenado por satisfacción).
        """
        if self.root is None:
            return False

        # 1. Obtener todos los nodos ordenados por satisfacción (inorder)
        nodos_ordenados = []
        self.__inorder_collect(self.root, nodos_ordenados)

        # 2. Reconstruir el árbol balanceado
        self.root = self.__build_balanced(nodos_ordenados, 0, len(nodos_ordenados) - 1, None)
        return True

    def __inorder_collect(self, node, resultado):
        """Recorre el árbol en inorder y acumula los nodos."""
        if node is None:
            return
        self.__inorder_collect(node.left, resultado)
        resultado.append(node)
        self.__inorder_collect(node.right, resultado)

    def __build_balanced(self, nodos, inicio, fin, parent):
        """Construye recursivamente un BST balanceado a partir de
        una lista ordenada de nodos.
        """
        if inicio > fin:
            return None
        mid = (inicio + fin) // 2
        nodo = nodos[mid]
        nodo.parent = parent
        nodo.left = self.__build_balanced(nodos, inicio, mid - 1, nodo)
        nodo.right = self.__build_balanced(nodos, mid + 1, fin, nodo)
        return nodo

    # =========================
    # BÚSQUEDAS DIRECTAS
    # =========================
    def find(self, course_id):
        """
        Busca por ID recorriendo TODO el árbol (DFS),
        porque el árbol está ordenado por satisfacción, no por ID.
        """
        return self.__find_node_by_id_dfs(self.root, course_id)

    def __find_node_by_id_dfs(self, current_node, course_id):
        if current_node is None:
            return None

        if current_node.data[0] == course_id:
            return current_node

        left_result = self.__find_node_by_id_dfs(current_node.left, course_id)
        if left_result:
            return left_result

        return self.__find_node_by_id_dfs(current_node.right, course_id)

    def find_by_satisfaction(self, satisfaction_level):
        return self.__find_by_satisfaction(self.root, satisfaction_level)

    # =========================
    # APOYO PARA GUI
    # =========================
    def find_by_satisfaction(self, satisfaction_level):
        return self.__find_by_satisfaction(self.root, satisfaction_level)

    def is_empty(self):
        return self.root is None