import Arbol

def main():
    # Crear el árbol
    arbol = Arbol.Arbol()
    
    print("=" * 80)
    print("LABORATORIO 1 - ESTRUCTURAS DE DATOS 2")
    print("Árbol Binario de Búsqueda - Gestión de Cursos")
    print("=" * 80)
    
    while True:
        print("\n" + "=" * 80)
        print("MENÚ PRINCIPAL")
        print("=" * 80)
        print("1. Insertar un nodo (por ID de curso)")
        print("2. Eliminar un nodo")
        print("3. Buscar un nodo")
        print("4. Buscar nodos por criterios")
        print("5. Mostrar recorrido por niveles")
        print("6. Operaciones sobre nodo seleccionado")
        print("7. Salir")
        print("=" * 80)
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            menu_insertar(arbol)
        elif opcion == "2":
            menu_eliminar(arbol)
        elif opcion == "3":
            menu_buscar(arbol)
        elif opcion == "4":
            menu_buscar_criterios(arbol)
        elif opcion == "5":
            menu_recorrido(arbol)
        elif opcion == "6":
            menu_operaciones_nodo(arbol)
        elif opcion == "7":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

def menu_insertar(arbol):
    print("\n--- INSERTAR NODO ---")
    try:
        course_id = int(input("Ingrese el ID del curso: "))
        arbol.insert(course_id)
        print(f"Curso {course_id} insertado exitosamente.")
    except ValueError:
        print("Error: El ID debe ser un número entero.")

def menu_eliminar(arbol):
    print("\n--- ELIMINAR NODO ---")
    print("1. Eliminar por ID")
    print("2. Eliminar por satisfacción (métrica)")
    sub_opcion = input("Seleccione: ").strip()
    
    if sub_opcion == "1":
        try:
            course_id = int(input("Ingrese el ID del curso a eliminar: "))
            arbol.delete_by_id(course_id)
        except ValueError:
            print("Error: El ID debe ser un número entero.")
    elif sub_opcion == "2":
        try:
            satisfaction = float(input("Ingrese el nivel de satisfacción: "))
            arbol.delete_by_satisfaction(satisfaction)
        except ValueError:
            print("Error: La satisfacción debe ser un número.")
    else:
        print("Opción no válida.")

def menu_buscar(arbol):
    print("\n--- BUSCAR NODO ---")
    print("1. Buscar por ID")
    print("2. Buscar por satisfacción (métrica)")
    sub_opcion = input("Seleccione: ").strip()
    
    if sub_opcion == "1":
        try:
            course_id = int(input("Ingrese el ID del curso: "))
            node = arbol.find(course_id)
            if node:
                print(f"\nNodo encontrado:")
                print(f"  ID: {node.data[0]}")
                print(f"  Satisfacción: {node.data[1]:.4f}")
            else:
                print("Nodo no encontrado.")
        except ValueError:
            print("Error: El ID debe ser un número entero.")
    elif sub_opcion == "2":
        try:
            satisfaction = float(input("Ingrese el nivel de satisfacción: "))
            node = arbol.find_by_satisfaction(satisfaction)
            if node:
                print(f"\nNodo encontrado:")
                print(f"  ID: {node.data[0]}")
                print(f"  Satisfacción: {node.data[1]:.4f}")
            else:
                print("Nodo no encontrado.")
        except ValueError:
            print("Error: La satisfacción debe ser un número.")
    else:
        print("Opción no válida.")

def menu_buscar_criterios(arbol):
    print("\n--- BUSCAR NODOS POR CRITERIOS ---")
    print("1. Reseñas positivas > (negativas + neutras)")
    print("2. Creados después de una fecha")
    print("3. Cantidad de clases en un rango")
    print("4. Reseñas por encima del promedio")
    sub_opcion = input("Seleccione un criterio: ").strip()
    
    if sub_opcion == "1":
        results = arbol.search_by_positive_reviews_criterion()
        mostrar_resultados_busqueda(results)
    
    elif sub_opcion == "2":
        fecha = input("Ingrese la fecha (YYYY-MM-DD): ").strip()
        try:
            results = arbol.search_by_creation_date(fecha)
            mostrar_resultados_busqueda(results)
        except ValueError:
            print("Error: Formato de fecha inválido.")
    
    elif sub_opcion == "3":
        try:
            min_clases = int(input("Ingrese el mínimo de clases: "))
            max_clases = int(input("Ingrese el máximo de clases: "))
            results = arbol.search_by_classes_range(min_clases, max_clases)
            mostrar_resultados_busqueda(results)
        except ValueError:
            print("Error: Los valores deben ser números enteros.")
    
    elif sub_opcion == "4":
        print("¿Qué tipo de reseña?")
        print("1. Positivas")
        print("2. Negativas")
        print("3. Neutras")
        tipo_opcion = input("Seleccione: ").strip()
        
        tipo_mapa = {"1": "positive", "2": "negative", "3": "neutral"}
        tipo = tipo_mapa.get(tipo_opcion)
        
        if tipo:
            results = arbol.search_by_reviews_above_average(tipo)
            mostrar_resultados_busqueda(results)
        else:
            print("Opción no válida.")
    else:
        print("Opción no válida.")

def mostrar_resultados_busqueda(results):
    if results:
        print(f"\nSe encontraron {len(results)} nodo(s):\n")
        for i, node in enumerate(results, 1):
            print(f"{i}. ID: {node.data[0]} | Satisfacción: {node.data[1]:.4f}")
    else:
        print("No se encontraron nodos que cumplan el criterio.")

def menu_recorrido(arbol):
    print("\n--- RECORRIDO POR NIVELES ---")
    arbol.level_order_traversal()

def menu_operaciones_nodo(arbol):
    print("\n--- OPERACIONES SOBRE NODO SELECCIONADO ---")
    
    try:
        course_id = int(input("Ingrese el ID del nodo: "))
    except ValueError:
        print("Error: El ID debe ser un número entero.")
        return
    
    node = arbol.find(course_id)
    
    if not node:
        print("Nodo no encontrado.")
        return
    
    print(f"\nNodo seleccionado: ID {node.data[0]}")
        
    while True:
        print("\n" + "-" * 60)
        print("OPERACIONES DISPONIBLES")
        print("-" * 60)
        print("1. Obtener toda la información del curso")
        print("2. Obtener el nivel del nodo")
        print("3. Obtener el factor de balanceo")
        print("4. Encontrar el padre del nodo")
        print("5. Encontrar el abuelo del nodo")
        print("6. Encontrar el tío del nodo")
        print("7. Volver al menú principal")
        print("-" * 60)
        
        op = input("Seleccione una operación: ").strip()
        
        if op == "1":
            info = arbol.get_course_full_info(course_id)
            if info:
                print("\n=== INFORMACIÓN COMPLETA DEL CURSO ===")
                for key, value in info.items():
                    print(f"{key}: {value}")
            else:
                print("No se encontró información del curso.")
        
        elif op == "2":
            nivel = arbol.get_node_level(node)
            print(f"\nNivel del nodo: {nivel}")
        
        elif op == "3":
            balance = arbol.get_balance_factor(node)
            print(f"\nFactor de balanceo: {balance}")
        
        elif op == "4":
            padre = arbol.get_parent(node)
            if padre:
                print(f"\nPadre del nodo: ID {padre.data[0]} | Satisfacción: {padre.data[1]:.4f}")
            else:
                print("\nEste nodo es la raíz (no tiene padre).")
        
        elif op == "5":
            abuelo = arbol.get_grandparent(node)
            if abuelo:
                print(f"\nAbuelo del nodo: ID {abuelo.data[0]} | Satisfacción: {abuelo.data[1]:.4f}")
            else:
                print("\nEste nodo no tiene abuelo.")
        
        elif op == "6":
            tio = arbol.get_uncle(node)
            if tio:
                print(f"\nTío del nodo: ID {tio.data[0]} | Satisfacción: {tio.data[1]:.4f}")
            else:
                print("\nEste nodo no tiene tío.")
        
        elif op == "7":
            break
        
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
