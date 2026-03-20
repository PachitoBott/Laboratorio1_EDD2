import csv
from datetime import datetime
from collections import deque
import Nodo

class Arbol:
    def __init__(self, root=None):
        self.root = root
        self.all_nodes = []  # Para rastrear todos los nodos del árbol
        
    def __preorder_recursivo(self, node):
        if node is not None:
            print(node.data)
            self.__preorder_recursivo(node.left)
            self.__preorder_recursivo(node.right)
            
 
    def get_course_data(self, course_id):
        csv_path = 'dataset_courses_with_reviews.csv'
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
        
        satisfaction = (data['rating'] * 0.7) + (((5*data['positive_reviews'])  + (3*data['neutral_reviews']) + data['negative_reviews']) / data['number_of_reviews']) * 0.3

        return satisfaction  
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
            
    def __insert_recursively(self, current_node, new_node):
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

    def __delete_recursively(self, current_node, course_id):
        if current_node is None:
            return current_node
        
        if course_id < current_node.data[0]:
            current_node.left = self.__delete_recursively(current_node.left, course_id)
        elif course_id > current_node.data[0]:
            current_node.right = self.__delete_recursively(current_node.right, course_id)
        else:
            if current_node.left is None:
                return current_node.right
            elif current_node.right is None:
                return current_node.left
            
            min_larger_node = self.__find_min(current_node.right)
            current_node.data = min_larger_node.data
            current_node.right = self.__delete_recursively(current_node.right, min_larger_node.data[0])
        
        return current_node
    
    def __find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    # ============== FUNCIONES PARA ELIMINAR NODOS ==============
    
    def delete_by_id(self, course_id):
        """Elimina un nodo por su ID"""
        self.root = self.__delete_recursively(self.root, course_id)
        # Remover del registro de nodos
        self.all_nodes = [n for n in self.all_nodes if n.data[0] != course_id]
        print(f"Nodo con ID {course_id} eliminado.")
    
    def delete_by_satisfaction(self, satisfaction_level):
        """Elimina un nodo por su nivel de satisfacción (métrica)"""
        found_node = self.__find_by_satisfaction(self.root, satisfaction_level)
        if found_node:
            self.delete_by_id(found_node.data[0])
        else:
            print(f"No se encontró nodo con satisfacción {satisfaction_level}")
    
    def __find_by_satisfaction(self, node, satisfaction_level, tolerance=0.01):
        """Busca un nodo por su satisfacción con tolerancia"""
        if node is None:
            return None
        
        if abs(node.data[1] - satisfaction_level) < tolerance:
            return node
        
        left_result = self.__find_by_satisfaction(node.left, satisfaction_level, tolerance)
        if left_result:
            return left_result
        
        return self.__find_by_satisfaction(node.right, satisfaction_level, tolerance)
    
    # ============== FUNCIONES PARA BUSCAR NODOS POR CRITERIOS ==============
    
    def search_by_positive_reviews_criterion(self):
        """Busca nodos donde reseñas positivas > (negativas + neutras)"""
        results = []
        self.__search_criterion_recursive(self.root, results, 
                                         lambda n: self.__positive_reviews_criterion(n.data[0]))
        return results
    
    def __positive_reviews_criterion(self, course_id):
        """Verifica si reseñas positivas > (negativas + neutras)"""
        data = self.get_course_data(course_id)
        if data:
            return data['positive_reviews'] > (data['negative_reviews'] + data['neutral_reviews'])
        return False
    
    def search_by_creation_date(self, target_date):
        """Busca nodos creados después de una fecha dada
        target_date debe ser string en formato 'YYYY-MM-DD'
        """
        results = []
        target_dt = datetime.strptime(target_date, '%Y-%m-%d')
        self.__search_criterion_recursive(self.root, results,
                                         lambda n: self.__date_criterion(n.data[0], target_dt))
        return results
    
    def __date_criterion(self, course_id, target_date):
        """Verifica si la fecha de creación es posterior a target_date"""
        csv_path = 'dataset_courses_with_reviews.csv'
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == str(course_id):
                    creation_date = datetime.strptime(row['created'][:10], '%Y-%m-%d')
                    return creation_date > target_date
        return False
    
    def search_by_classes_range(self, min_classes, max_classes):
        """Busca nodos donde num_published_lectures está en el rango [min, max]"""
        results = []
        self.__search_criterion_recursive(self.root, results,
                                         lambda n: self.__classes_range_criterion(n.data[0], min_classes, max_classes))
        return results
    
    def __classes_range_criterion(self, course_id, min_val, max_val):
        """Verifica si num_published_lectures está en el rango"""
        csv_path = 'dataset_courses_with_reviews.csv'
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == str(course_id):
                    num_lectures = int(row['num_published_lectures'])
                    return min_val <= num_lectures <= max_val
        return False
    
    def search_by_reviews_above_average(self, review_type='positive'):
        """Busca nodos con reseñas positivas/negativas/neutras por encima del promedio
        review_type: 'positive', 'negative', o 'neutral'
        """
        # Calcular promedio de todas las reseñas
        average = self.__calculate_review_average(review_type)
        
        results = []
        self.__search_criterion_recursive(self.root, results,
                                         lambda n: self.__above_average_criterion(n.data[0], review_type, average))
        return results
    
    def __calculate_review_average(self, review_type):
        """Calcula el promedio de un tipo de reseña en todos los nodos"""
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
        """Verifica si el tipo de reseña está por encima del promedio"""
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
        """Busca recursivamente todos los nodos que cumplen un criterio"""
        if node is None:
            return
        
        if criterion(node):
            results.append(node)
        
        self.__search_criterion_recursive(node.left, results, criterion)
        self.__search_criterion_recursive(node.right, results, criterion)
    
    # ============== RECORRIDO POR NIVELES (BFS) ==============
    
    def level_order_traversal(self):
        """Recorrido por niveles del árbol (BFS) - Muestra solo IDs"""
        if self.root is None:
            print("El árbol está vacío.")
            return []
        
        result = []
        queue = deque([(self.root, 0)])  # (nodo, nivel)
        current_level = 0
        level_nodes = []
        
        while queue:
            node, level = queue.popleft()
            
            if level > current_level:
                result.append(level_nodes)
                level_nodes = []
                current_level = level
            
            level_nodes.append(node.data[0])
            
            if node.left:
                queue.append((node.left, level + 1))
            if node.right:
                queue.append((node.right, level + 1))
        
        if level_nodes:
            result.append(level_nodes)
        
        # Mostrar el recorrido
        for i, level in enumerate(result):
            print(f"Nivel {i}: {level}")
        
        return result
    
    # ============== OPERACIONES SOBRE NODOS SELECCIONADOS ==============
    
    def get_course_full_info(self, course_id):
        """Obtiene toda la información del curso"""
        csv_path = 'dataset_courses_with_reviews.csv'
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
        """Obtiene el nivel del nodo en el árbol (recursivamente)"""
        return self.__get_level_recursive(self.root, node, 0)
    
    def __get_level_recursive(self, current_node, target_node, level):
        """Encuentra el nivel del nodo recursivamente"""
        if current_node is None:
            return -1
        
        if current_node is target_node:
            return level
        
        left_level = self.__get_level_recursive(current_node.left, target_node, level + 1)
        if left_level != -1:
            return left_level
        
        return self.__get_level_recursive(current_node.right, target_node, level + 1)
    
    def get_balance_factor(self, node):
        """Obtiene el factor de balanceo (equilibrio) del nodo"""
        left_height = self.__get_height(node.left)
        right_height = self.__get_height(node.right)
        return left_height - right_height
    
    def __get_height(self, node):
        """Calcula la altura de un subárbol"""
        if node is None:
            return 0
        return 1 + max(self.__get_height(node.left), self.__get_height(node.right))
    
    def get_parent(self, node):
        """Encuentra el padre del nodo (recursivamente)"""
        if node is None:
            return None
        return node.parent
    
    def get_grandparent(self, node):
        """Encuentra el abuelo del nodo (recursivamente)"""
        if node is None or node.parent is None:
            return None
        return node.parent.parent
    
    def get_uncle(self, node):
        """Encuentra el tío del nodo (recursivamente)"""
        if node is None or node.parent is None or node.parent.parent is None:
            return None
        
        grandparent = node.parent.parent
        parent = node.parent
        
        if grandparent.left == parent:
            return grandparent.right
        else:
            return grandparent.left
    
    # ============== FUNCIONES DE BÚSQUEDA ADICIONALES ==============
    
    def find(self, course_id):
        """Busca un nodo por su ID y retorna el nodo completo"""
        return self.__find_node_by_id(self.root, course_id)
    
    def __find_node_by_id(self, current_node, course_id):
        """Busca recursivamente un nodo por su ID"""
        if current_node is None:
            return None
        
        if course_id == current_node.data[0]:
            return current_node
        elif course_id < current_node.data[0]:
            return self.__find_node_by_id(current_node.left, course_id)
        else:
            return self.__find_node_by_id(current_node.right, course_id)
    
    def find_by_satisfaction(self, satisfaction_level):
        """Busca un nodo por su nivel de satisfacción"""
        return self.__find_by_satisfaction(self.root, satisfaction_level)
        
        return result
    