# Algoritmos-grafos


# Algoritmos de Grafos en Python

## Descripcion del proyecto

Este proyecto contiene cinco programas visuales desarrollados en Python utilizando Tkinter. Su objetivo es representar grafos mediante nodos y conexiones, permitiendo observar el funcionamiento de diferentes algoritmos.

## Algoritmos incluidos

1. **Dijkstra:** Calcula el camino mas corto desde un nodo de origen hacia todos los demas nodos, tomando en cuenta los costos de las conexiones.
2. **Floyd:** Calcula las distancias minimas entre todos los pares de nodos.
3. **Warshall:** Determina si existe un camino entre los diferentes nodos de un grafo dirigido.
4. **Kruskal:** Encuentra el arbol de expansion minima, conectando todos los nodos con el menor costo posible y sin formar ciclos.
5. **Todos los algoritmos:** Integra los algoritmos anteriores en un solo programa, permitiendo seleccionar uno o combinar sus resultados.

## Funcionamiento

Cada programa muestra una ventana grafica donde se representan los nodos mediante circulos y las conexiones mediante lineas. Las conexiones ponderadas muestran sus respectivos costos.

El usuario puede seleccionar nodos, ejecutar los algoritmos y visualizar los resultados, como rutas, distancias, conexiones seleccionadas y costos totales. Tambien es posible mover los nodos arrastrandolos con el mouse.

## Archivos del proyecto

- `motor_grafos.py`: Contiene las funciones y elementos visuales compartidos.
- `dijkstra.py`: Ejecuta el algoritmo de Dijkstra.
- `floyd.py`: Ejecuta el algoritmo de Floyd.
- `warshall.py`: Ejecuta el algoritmo de Warshall.
- `kruskal.py`: Ejecuta el algoritmo de Kruskal.
- `todos_algoritmos.py`: Integra los algoritmos en un solo programa.

## Requisitos

- Python 3.
- Biblioteca Tkinter (incluida normalmente en Python).

## Ejecucion

Para iniciar un programa, abre su archivo correspondiente en Visual Studio Code y ejecutalo.

Por ejemplo:

```bash
python dijkstra.py
```

Para iniciar el programa integrado:

```bash
python todos_algoritmos.py
```
