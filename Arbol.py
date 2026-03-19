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
   