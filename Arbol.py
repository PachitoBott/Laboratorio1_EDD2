import csv

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
                        'negative_reviews': int(row['negative_reviews'])
                    }
        return None

    def calculate_satisfaction_level(self, course_id):
        data = self.get_course_data(course_id)
        if data is None:
            return None
        # Aquí puedes agregar tu fórmula usando data['rating'], data['positive_reviews'], etc.
        # Ejemplo placeholder: satisfaction = (data['rating'] / 5) * (data['positive_reviews'] / (data['positive_reviews'] + data['neutral_reviews'] + data['negative_reviews']))
        # Reemplaza con tu fórmula real
        return data  # Devuelve los datos para que los uses en tu fórmula