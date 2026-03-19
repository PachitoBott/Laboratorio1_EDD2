import csv

import Nodo

class Arbol:
    def __init__(self, root=None):
        self.root = root
        
    def __preorder_recursivo(self, node):
        if node is not None:
            print(node.data)
            self.__preorder_recursivo(node.left)
            self.__preorder_recursivo(node.right)
            
 
    def get_course_data(self, course_id):
        csv_path = '\dataset_courses_with_reviews.csv'
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == str(course_id):
                    return {
                        'rating': float(row['rating']),
                        'positive_reviews': int(row['positive_reviews']),
                        'neutral_reviews': int(row['neutral_reviews']),
                        'negative_reviews': int(row['negative_reviews']),
                        'number_of_reviews': int(row['number_of_reviews'])  
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
        
        new_node = Nodo((course_id, satisfaction_level))
        
        if self.root is None:
            self.root = new_node
        else:
            self.__insert_recursively(self.root, new_node)
            
    def __insert_recursively(self, current_node, new_node):
        if new_node.data[1] < current_node.data[1]: 
            if current_node.left is None:
                current_node.left = new_node
            else:
                self.__insert_recursively(current_node.left, new_node)
        else:
            if current_node.right is None:
                current_node.right = new_node
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
    
    def find(self, course_id):
        return self.__find_recursively(self.root, course_id)
    
    def __find_recursively(self, current_node, course_id):
        if current_node is None:
            return None
        
        if course_id == current_node.data[0]:
            return current_node.data
        elif course_id < current_node.data[0]:
            return self.__find_recursively(current_node.left, course_id)
        else:
            return self.__find_recursively(current_node.right, course_id)
    