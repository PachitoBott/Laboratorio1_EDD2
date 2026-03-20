import Arbol

# Crear árbol y probar inserción
arbol = Arbol.Arbol()
print('Testing inserción...')
arbol.insert(567828)
print(f'Raíz insertada: ID {arbol.root.data[0]}, Satisfacción: {arbol.root.data[1]:.4f}')

arbol.insert(1565838)
arbol.insert(625204)
print(f'Árbol con 3 nodos creado')

# Probar búsqueda
node = arbol.find(567828)
print(f'Búsqueda por ID: {node.data[0]}')

# Probar información
info = arbol.get_course_full_info(567828)
print(f'Título: {info["title"]}')

# Probar nivel
nivel = arbol.get_node_level(node)
print(f'Nivel del nodo: {nivel}')

# Probar recorrido
print('\nRecorrido por niveles:')
arbol.level_order_traversal()

# Probar búsquedas por criterios
print('\n\nBúsquedas por criterios:')
print('\n1. Reseñas positivas > (negativas + neutras):')
positivos = arbol.search_by_positive_reviews_criterion()
print(f"   Encontrados: {len(positivos)} nodos")

print('\n2. Factor de balanceo:')
balance = arbol.get_balance_factor(node)
print(f"   Factor de balanceo del nodo {node.data[0]}: {balance}")

print('\n✅ Todas las pruebas exitosas!')
