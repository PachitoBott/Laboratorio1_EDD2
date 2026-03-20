# Laboratorio 1 - Estructuras de Datos 2

## Descripción General
Sistema de gestión de cursos Udemy mediante un **Árbol Binario de Búsqueda (ABB)** ordenado por nivel de satisfacción. El árbol se construye a partir de datos de un CSV que contiene información sobre cursos, reseñas y calificaciones.

## Estructura del Proyecto

### Archivos Principales

- **`Nodo.py`**: Clase que representa un nodo del árbol con:
  - `data`: tupla (id_curso, nivel_satisfaccion)
  - `left`: referencia al hijo izquierdo
  - `right`: referencia al hijo derecho
  - `parent`: referencia al padre (para operaciones de búsqueda de ancestros)

- **`Arbol.py`**: Clase principal que implementa el Árbol Binario de Búsqueda con todas las operaciones requeridas

- **`Main.py`**: Interfaz de menú interactivo para usar el sistema

- **`dataset_courses_with_reviews.csv`**: Archivo de datos con información de cursos

---

## Funcionalidades Implementadas

### 1. Insertar un Nodo por ID
```python
arbol.insert(course_id)
```
- Calcula automáticamente el nivel de satisfacción del curso
- Inserta el nodo en la posición correcta manteniendo la propiedad de ABB
- Mantiene referencias padre-hijo

---

### 2. Eliminar un Nodo
Dos opciones:

**a) Por ID del curso:**
```python
arbol.delete_by_id(course_id)
```

**b) Por nivel de satisfacción (métrica):**
```python
arbol.delete_by_satisfaction(satisfaction_level)
```
- Implementa el algoritmo estándar de eliminación en ABB
- Maneja casos: nodo sin hijos, con un hijo, con dos hijos

---

### 3. Buscar un Nodo
Dos opciones:

**a) Por ID del curso:**
```python
node = arbol.find(course_id)
```

**b) Por nivel de satisfacción (métrica):**
```python
node = arbol.find_by_satisfaction(satisfaction_level)
```
- Retorna el objeto nodo completo para operaciones posteriores

---

### 4. Buscar Nodos por Criterios

#### a) Reseñas Positivas > (Negativas + Neutras)
```python
results = arbol.search_by_positive_reviews_criterion()
```
- Retorna lista de nodos que cumplen la condición

#### b) Creados Después de una Fecha
```python
results = arbol.search_by_creation_date('2020-01-01')
```
- Parámetro en formato `'YYYY-MM-DD'`
- Retorna nodos con fecha de creación posterior

#### c) Cantidad de Clases en un Rango
```python
results = arbol.search_by_classes_range(min_classes, max_classes)
```
- Busca nodos donde `num_published_lectures` esté en `[min, max]`

#### d) Reseñas por Encima del Promedio
```python
results = arbol.search_by_reviews_above_average(review_type)
```
- Parámetro `review_type`: `'positive'`, `'negative'`, o `'neutral'`
- Calcula el promedio de todas las reseñas del árbol
- Retorna nodos que superan el promedio

---

### 5. Recorrido por Niveles (BFS)
```python
arbol.level_order_traversal()
```
- Implementación **recursiva** usando cola (deque)
- Muestra solo los **IDs de los cursos**
- Formato: `Nivel 0: [ID1, ID2, ...], Nivel 1: [ID3, ID4, ...], ...`

---

### 6. Operaciones sobre Nodo Seleccionado

Después de buscar un nodo, se pueden realizar:

#### a) Obtener Información Completa del Curso
```python
info = arbol.get_course_full_info(course_id)
```
Retorna diccionario con:
- ID, título, URL
- Calificación (rating)
- Número de reseñas (total, positivas, negativas, neutras)
- Número de clases
- Fechas de creación y última actualización
- Duración

#### b) Obtener Nivel del Nodo
```python
nivel = arbol.get_node_level(node)
```
- Retorna el nivel del nodo en el árbol (raíz = 0)
- Implementación **recursiva**

#### c) Obtener Factor de Balanceo
```python
balance = arbol.get_balance_factor(node)
```
- Retorna: `altura_izquierda - altura_derecha`
- Indica si el subárbol está equilibrado

#### d) Encontrar el Padre del Nodo
```python
padre = arbol.get_parent(node)
```
- Retorna el nodo padre
- **Recursivamente** (mediante referencia parent)

#### e) Encontrar el Abuelo del Nodo
```python
abuelo = arbol.get_grandparent(node)
```
- Retorna el padre del padre
- **Recursivamente** (padre.parent.parent)

#### f) Encontrar el Tío del Nodo
```python
tio = arbol.get_uncle(node)
```
- Retorna el hermano del padre (hijo del abuelo)
- **Recursivamente**

---

## Cómo Usar

### Ejecución Interactiva
```bash
python Main.py
```

Se abrirá un menú interactivo con opciones para:
1. Insertar cursos
2. Eliminar cursos
3. Buscar cursos
4. Buscar por criterios
5. Ver recorrido por niveles
6. Operaciones sobre nodos seleccionados

### Uso Programático
```python
import Arbol

# Crear árbol
arbol = Arbol.Arbol()

# Insertar cursos
arbol.insert(567828)
arbol.insert(1565838)
arbol.insert(625204)

# Buscar
node = arbol.find(567828)

# Operaciones
info = arbol.get_course_full_info(567828)
nivel = arbol.get_node_level(node)
balance = arbol.get_balance_factor(node)

# Recorrido
arbol.level_order_traversal()

# Búsquedas por criterio
positivos = arbol.search_by_positive_reviews_criterion()
recientes = arbol.search_by_creation_date('2020-01-01')
rango_clases = arbol.search_by_classes_range(100, 500)
```

---

## Nivel de Satisfacción

Se calcula como:
```
Satisfacción = (rating × 0.7) + (((5×positivas + 3×neutras + negativas) / total_reviews) × 0.3)
```

Este valor se usa como clave de ordenamiento en el árbol.

---

## Características Importantes

✅ **Árbol Binario de Búsqueda** ordenado por satisfacción  
✅ **Búsquedas recursivas** en multiple formatos  
✅ **Operaciones sobre ancestros** (padre, abuelo, tío)  
✅ **Recorrido por niveles** (BFS)  
✅ **Búsquedas por criterios múltiples**  
✅ **Gestión completa** de inserción y eliminación  
✅ **Interfaz interactiva** fácil de usar  
✅ **Manejo de errores** y validaciones  

---

## Requisitos

- Python 3.6+
- Archivo CSV `dataset_courses_with_reviews.csv` en el mismo directorio

---

## Notas para Estudiantes

- Los métodos de búsqueda recursiva están claramente identificados
- Todas las operaciones retornan nodos o información útil
- El factor de balanceo puede usarse para análisis de equilibrio del árbol
- Las búsquedas por criterios utilizan recorrido en profundidad (DFS)

