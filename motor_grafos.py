
import tkinter as tk
from tkinter import ttk
import heapq
from collections import deque

NODOS = ["A", "B", "C", "D", "E", "F"]

ARISTAS = [
    ("A", "B", 4), ("A", "C", 2),
    ("B", "C", 1), ("B", "D", 5),
    ("C", "D", 8), ("C", "E", 10),
    ("D", "E", 2), ("D", "F", 6),
    ("E", "F", 3)
]

DIRIGIDAS = [
    ("A", "B"), ("A", "C"),
    ("B", "C"), ("B", "D"),
    ("C", "E"), ("D", "C"),
    ("D", "F"), ("E", "D"),
    ("E", "F")
]


class GrafoApp:

    def __init__(self, ventana, modo=None):

        self.ventana = ventana
        self.modo_fijo = modo

        self.pos_iniciales = {
            "A": [90, 80],
            "B": [300, 65],
            "C": [195, 220],
            "D": [480, 160],
            "E": [360, 355],
            "F": [650, 330]
        }

        self.pos = {
            n: p[:] for n, p in self.pos_iniciales.items()
        }

        self.grafo = {n: {} for n in NODOS}

        for a, b, peso in ARISTAS:
            self.grafo[a][b] = peso
            self.grafo[b][a] = peso

        self.colores = {}
        self.arrastrando = None

        ventana.title("Visualizador de Algoritmos de Grafos")
        ventana.geometry("1280x760")
        ventana.resizable(False, False)
        ventana.configure(bg="#202938")

        titulo = tk.Label(
            ventana,
            text="ALGORITMOS DE GRAFOS",
            font=("Arial", 20, "bold"),
            bg="#202938",
            fg="white"
        )
        titulo.pack(pady=8)

        controles = tk.Frame(ventana, bg="#202938")
        controles.pack(pady=5)

        if modo is None:

            tk.Label(
                controles,
                text="Algoritmo:",
                bg="#202938",
                fg="white"
            ).grid(row=0, column=0, padx=5)

            self.selector = ttk.Combobox(
                controles,
                values=[
                    "Dijkstra",
                    "Floyd",
                    "Warshall",
                    "Kruskal",
                    "Combinar algoritmos"
                ],
                state="readonly",
                width=23
            )

            self.selector.set("Dijkstra")
            self.selector.grid(row=0, column=1, padx=5)
            self.selector.bind(
                "<<ComboboxSelected>>", self.cambio
            )

        else:

            self.selector = None

            tk.Label(
                controles,
                text=modo.upper(),
                bg="#202938",
                fg="#60a5fa",
                font=("Arial", 12, "bold")
            ).grid(row=0, column=0, padx=8)

        tk.Label(
            controles,
            text="Origen:",
            bg="#202938",
            fg="white"
        ).grid(row=0, column=2, padx=4)

        self.origen = ttk.Combobox(
            controles,
            values=NODOS,
            state="readonly",
            width=5
        )
        self.origen.set("A")
        self.origen.grid(row=0, column=3, padx=4)

        tk.Label(
            controles,
            text="Destino:",
            bg="#202938",
            fg="white"
        ).grid(row=0, column=4, padx=4)

        self.destino = ttk.Combobox(
            controles,
            values=NODOS,
            state="readonly",
            width=5
        )
        self.destino.set("F")
        self.destino.grid(row=0, column=5, padx=4)

        self.tipo_floyd = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            controles,
            text="Floyd dirigido",
            variable=self.tipo_floyd
        ).grid(row=0, column=6, padx=8)

        ttk.Button(
            controles,
            text="Ejecutar",
            command=self.ejecutar
        ).grid(row=0, column=7, padx=6)

        ttk.Button(
            controles,
            text="Restablecer",
            command=self.restablecer
        ).grid(row=0, column=8, padx=6)

        contenido = tk.Frame(ventana, bg="#202938")
        contenido.pack(padx=12, pady=8)

        panel_grafo = tk.Frame(contenido, bg="#202938")
        panel_grafo.grid(row=0, column=0, padx=6)

        tk.Label(
            panel_grafo,
            text="GRAFO Y CONEXIONES",
            font=("Arial", 12, "bold"),
            bg="#202938",
            fg="white"
        ).pack(pady=5)

        self.canvas = tk.Canvas(
            panel_grafo,
            width=760,
            height=500,
            bg="#111827",
            highlightthickness=1,
            highlightbackground="#475569"
        )
        self.canvas.pack()

        self.canvas.bind(
            "<Button-1>", self.iniciar_movimiento
        )
        self.canvas.bind(
            "<B1-Motion>", self.mover_nodo
        )
        self.canvas.bind(
            "<ButtonRelease-1>", self.soltar_nodo
        )

        panel_resultados = tk.Frame(
            contenido,
            bg="#202938"
        )
        panel_resultados.grid(row=0, column=1, padx=6)

        tk.Label(
            panel_resultados,
            text="RESULTADOS DEL ALGORITMO",
            font=("Arial", 12, "bold"),
            bg="#202938",
            fg="white"
        ).pack(pady=5)

        self.resultado = tk.Text(
            panel_resultados,
            width=56,
            height=37,
            bg="#0b1220",
            fg="white",
            font=("Consolas", 8),
            relief="flat",
            wrap="none",
            state="disabled"
        )
        self.resultado.pack()

        leyenda = tk.Frame(ventana, bg="#202938")
        leyenda.pack(pady=4)

        tk.Label(
            leyenda,
            text="Gris: conexiones",
            bg="#202938",
            fg="#cbd5e1"
        ).pack(side="left", padx=10)

        tk.Label(
            leyenda,
            text="Verde: camino minimo",
            bg="#202938",
            fg="#22c55e"
        ).pack(side="left", padx=10)

        tk.Label(
            leyenda,
            text="Naranja: arbol de expansion minima",
            bg="#202938",
            fg="#f59e0b"
        ).pack(side="left", padx=10)

        tk.Label(
            ventana,
            text="Arrastra los nodos con el mouse para cambiar su posicion.",
            bg="#202938",
            fg="#93c5fd",
            font=("Arial", 9, "bold")
        ).pack(pady=3)

        self.dibujar()
        self.escribir("Grafo listo. Selecciona un algoritmo y pulsa Ejecutar.")

    def modo(self):

        if self.modo_fijo:
            return self.modo_fijo

        return self.selector.get()

    def escribir(self, texto):

        self.resultado.configure(state="normal")
        self.resultado.insert("end", texto + "\n")
        self.resultado.configure(state="disabled")

    def limpiar(self):

        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.configure(state="disabled")

    def dibujar(self):

        self.canvas.delete("all")

        if self.modo() == "Warshall":
            conexiones = DIRIGIDAS
        else:
            conexiones = ARISTAS

        for conexion in conexiones:

            a, b = conexion[0], conexion[1]

            x1, y1 = self.pos[a]
            x2, y2 = self.pos[b]

            color = self.colores.get(
                frozenset((a, b)), "#64748b"
            )

            grosor = 5 if color != "#64748b" else 2

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=color,
                width=grosor,
                arrow=tk.LAST if self.modo() == "Warshall" else tk.NONE,
                arrowshape=(12, 14, 5)
            )

            if self.modo() != "Warshall":

                peso = conexion[2]

                mx = (x1 + x2) / 2
                my = (y1 + y2) / 2

                self.canvas.create_oval(
                    mx - 13, my - 11,
                    mx + 13, my + 11,
                    fill="white",
                    outline="#94a3b8"
                )

                self.canvas.create_text(
                    mx, my,
                    text=str(peso),
                    fill="black",
                    font=("Arial", 9, "bold")
                )

        for nodo, (x, y) in self.pos.items():

            self.canvas.create_oval(
                x - 24, y - 24,
                x + 24, y + 24,
                fill="#2563eb",
                outline="white",
                width=2
            )

            self.canvas.create_text(
                x, y,
                text=nodo,
                fill="white",
                font=("Arial", 13, "bold")
            )

    def iniciar_movimiento(self, evento):

        self.arrastrando = None

        for nodo, (x, y) in self.pos.items():

            distancia = (
                (evento.x - x) ** 2 +
                (evento.y - y) ** 2
            ) ** 0.5

            if distancia <= 28:
                self.arrastrando = nodo
                break

    def mover_nodo(self, evento):

        if self.arrastrando is not None:

            self.pos[self.arrastrando] = [
                max(30, min(730, evento.x)),
                max(30, min(475, evento.y))
            ]

            self.dibujar()

    def soltar_nodo(self, evento):
        self.arrastrando = None

    def cambio(self, evento=None):

        self.colores = {}
        self.limpiar()
        self.dibujar()
        self.escribir("Algoritmo cambiado. Pulsa Ejecutar.")

    def restablecer(self):

        self.colores = {}

        self.pos = {
            n: p[:] for n, p in self.pos_iniciales.items()
        }

        self.limpiar()
        self.dibujar()

        self.escribir("Grafo restablecido.")

    def pintar(self, caminos=None, arbol=None):

        self.colores = {}

        for a, b in (arbol or []):
            self.colores[frozenset((a, b))] = "#f59e0b"

        for a, b in (caminos or []):
            self.colores[frozenset((a, b))] = "#22c55e"

        self.dibujar()

    def ejecutar(self):

        self.limpiar()

        modo = self.modo()

        if modo == "Dijkstra":
            self.dijkstra()

        elif modo == "Floyd":
            self.floyd()

        elif modo == "Warshall":
            self.warshall()

        elif modo == "Kruskal":
            self.kruskal()

        elif modo == "Combinar algoritmos":
            self.combinar()

    # DIJKSTRA

    def dijkstra(self, mostrar=True):

        inicio = self.origen.get()

        distancias = {
            n: float("inf") for n in NODOS
        }

        anteriores = {
            n: None for n in NODOS
        }

        distancias[inicio] = 0
        cola = [(0, inicio)]

        while cola:

            costo, actual = heapq.heappop(cola)

            if costo > distancias[actual]:
                continue

            for vecino, peso in self.grafo[actual].items():

                nuevo = costo + peso

                if nuevo < distancias[vecino]:

                    distancias[vecino] = nuevo
                    anteriores[vecino] = actual

                    heapq.heappush(
                        cola, (nuevo, vecino)
                    )

        caminos = {}

        for destino in NODOS:

            if distancias[destino] == float("inf"):
                caminos[destino] = None
                continue

            camino = []
            actual = destino

            while actual is not None:

                camino.insert(0, actual)
                actual = anteriores[actual]

            caminos[destino] = camino

        if mostrar:

            elegido = self.destino.get()
            camino = caminos[elegido]

            if camino:
                self.pintar(
                    caminos=list(zip(camino, camino[1:]))
                )

            self.escribir("========== DIJKSTRA ==========")
            self.escribir("Origen: " + inicio)
            self.escribir("CAMINOS MINIMOS HACIA TODOS LOS NODOS")

            for nodo in NODOS:

                if caminos[nodo] is None:

                    self.escribir(nodo + ": Sin conexion")

                else:

                    ruta = " -> ".join(caminos[nodo])

                    self.escribir(
                        f"{nodo}: {ruta} | Costo: {distancias[nodo]}"
                    )

        return caminos, distancias

    # FLOYD

    def matriz_costos(self, dirigido=False):

        n = len(NODOS)

        matriz = [
            [float("inf")] * n for _ in range(n)
        ]

        for i in range(n):
            matriz[i][i] = 0

        for a, b, peso in ARISTAS:

            i = NODOS.index(a)
            j = NODOS.index(b)

            matriz[i][j] = peso

            if not dirigido:
                matriz[j][i] = peso

        return matriz

    def floyd(self, mostrar=True, dirigido=None):

        if dirigido is None:
            dirigido = self.tipo_floyd.get()

        n = len(NODOS)

        distancias = self.matriz_costos(dirigido)

        siguiente = [
            [None] * n for _ in range(n)
        ]

        for i in range(n):
            for j in range(n):

                if distancias[i][j] != float("inf") and i != j:
                    siguiente[i][j] = j

        for k in range(n):
            for i in range(n):
                for j in range(n):

                    nuevo = (
                        distancias[i][k] +
                        distancias[k][j]
                    )

                    if nuevo < distancias[i][j]:

                        distancias[i][j] = nuevo
                        siguiente[i][j] = siguiente[i][k]

        inicio = NODOS.index(self.origen.get())
        fin = NODOS.index(self.destino.get())

        camino = None

        if siguiente[inicio][fin] is not None:

            camino = [self.origen.get()]
            actual = inicio

            while actual != fin:

                actual = siguiente[actual][fin]
                camino.append(NODOS[actual])

        if mostrar:

            self.escribir("========== FLOYD-WARSHALL ==========")

            self.escribir(
                "Tipo: " + ("Dirigido" if dirigido else "No dirigido")
            )

            self.escribir("MATRIZ DE DISTANCIAS MINIMAS")

            self.escribir(
                "      " + " ".join(f"{n:>4}" for n in NODOS)
            )

            for i, fila in enumerate(distancias):

                valores = [
                    "INF" if x == float("inf") else str(int(x))
                    for x in fila
                ]

                self.escribir(
                    f"{NODOS[i]:>5} " +
                    " ".join(f"{x:>4}" for x in valores)
                )

            if camino:

                self.pintar(
                    caminos=list(zip(camino, camino[1:]))
                )

                self.escribir(
                    "\nRuta seleccionada: " + " -> ".join(camino)
                )

                self.escribir(
                    "Costo minimo: " +
                    str(int(distancias[inicio][fin]))
                )

            else:

                self.escribir("\nNo existe camino.")

        return distancias, camino

    # WARSHALL

    def warshall(self, mostrar=True):

        n = len(NODOS)

        alcance = [
            [0] * n for _ in range(n)
        ]

        for i in range(n):
            alcance[i][i] = 1

        for a, b in DIRIGIDAS:

            i = NODOS.index(a)
            j = NODOS.index(b)

            alcance[i][j] = 1

        for k in range(n):
            for i in range(n):
                for j in range(n):

                    if alcance[i][k] and alcance[k][j]:
                        alcance[i][j] = 1

        if mostrar:

            inicio = self.origen.get()
            fin = self.destino.get()

            self.escribir("========== WARSHALL ==========")
            self.escribir("GRAFO DIRIGIDO")
            self.escribir("1 = Alcanzable | 0 = No alcanzable")
            self.escribir("MATRIZ DE ALCANZABILIDAD")

            self.escribir(
                "      " + " ".join(f"{n:>3}" for n in NODOS)
            )

            for i, fila in enumerate(alcance):

                self.escribir(
                    f"{NODOS[i]:>5} " +
                    " ".join(f"{x:>3}" for x in fila)
                )

            self.escribir("\nNODOS ALCANZABLES DESDE " + inicio)

            for j, nodo in enumerate(NODOS):

                if alcance[NODOS.index(inicio)][j]:
                    self.escribir(nodo + ": SI")
                else:
                    self.escribir(nodo + ": NO")

            existe = alcance[
                NODOS.index(inicio)
            ][
                NODOS.index(fin)
            ]

            self.escribir(
                f"\n¿Existe camino de {inicio} a {fin}? " +
                ("SI" if existe else "NO")
            )

            self.dibujar()

        return alcance

    # KRUSKAL

    def kruskal(self, mostrar=True):

        padre = {n: n for n in NODOS}
        rango = {n: 0 for n in NODOS}

        def encontrar(nodo):

            if padre[nodo] != nodo:
                padre[nodo] = encontrar(padre[nodo])

            return padre[nodo]

        def unir(a, b):

            ra = encontrar(a)
            rb = encontrar(b)

            if ra == rb:
                return False

            if rango[ra] < rango[rb]:
                padre[ra] = rb

            elif rango[ra] > rango[rb]:
                padre[rb] = ra

            else:
                padre[rb] = ra
                rango[ra] += 1

            return True

        seleccionadas = []
        rechazadas = []
        total = 0

        for a, b, peso in sorted(
            ARISTAS, key=lambda x: x[2]
        ):

            if unir(a, b):

                seleccionadas.append((a, b, peso))
                total += peso

            else:

                rechazadas.append((a, b, peso))

        arbol = [
            (a, b) for a, b, peso in seleccionadas
        ]

        conectado = len(seleccionadas) == len(NODOS) - 1

        if mostrar:

            self.pintar(arbol=arbol)

            self.escribir("========== KRUSKAL ==========")
            self.escribir("ARBOL DE EXPANSION MINIMA")

            for a, b, peso in seleccionadas:

                self.escribir(
                    f"{a} -- {b} | Costo: {peso}"
                )

            self.escribir("\nCONEXIONES RECHAZADAS")

            for a, b, peso in rechazadas:

                self.escribir(
                    f"{a} -- {b} | Forma ciclo"
                )

            self.escribir(
                "\nAristas seleccionadas: " +
                str(len(seleccionadas))
            )

            self.escribir(
                "Costo total minimo: " + str(total)
            )

            self.escribir(
                "Resultado: " +
                ("Arbol completo" if conectado else "Grafo desconectado")
            )

        return arbol, total, conectado

    # RUTA DENTRO DEL ARBOL

    def ruta_en_arbol(self, arbol):

        inicio = self.origen.get()
        fin = self.destino.get()

        adyacencia = {n: [] for n in NODOS}

        for a, b in arbol:

            adyacencia[a].append(b)
            adyacencia[b].append(a)

        cola = deque([inicio])
        anterior = {inicio: None}

        while cola:

            actual = cola.popleft()

            if actual == fin:
                break

            for vecino in adyacencia[actual]:

                if vecino not in anterior:

                    anterior[vecino] = actual
                    cola.append(vecino)

        if fin not in anterior:
            return None

        camino = []
        actual = fin

        while actual is not None:

            camino.insert(0, actual)
            actual = anterior[actual]

        return camino

    # COMBINACION

    def combinar(self):

        inicio = self.origen.get()
        fin = self.destino.get()

        self.escribir("======= COMBINACION DE ALGORITMOS =======")
        self.escribir(f"Origen: {inicio} | Destino: {fin}")

        alcance = self.warshall(False)

        conectado = alcance[
            NODOS.index(inicio)
        ][
            NODOS.index(fin)
        ]

        self.escribir("\n1. WARSHALL")
        self.escribir(
            "Existe conexion dirigida: " +
            ("SI" if conectado else "NO")
        )

        matriz, camino_floyd = self.floyd(
            False, dirigido=False
        )

        costo_floyd = matriz[
            NODOS.index(inicio)
        ][
            NODOS.index(fin)
        ]

        self.escribir("\n2. FLOYD")

        if camino_floyd:
            self.escribir(
                "Ruta: " + " -> ".join(camino_floyd)
            )
            self.escribir(
                "Costo: " + str(int(costo_floyd))
            )
        else:
            self.escribir("Sin ruta.")

        caminos, distancias = self.dijkstra(False)

        camino_dijkstra = caminos[fin]
        costo_dijkstra = distancias[fin]

        self.escribir("\n3. DIJKSTRA")

        if camino_dijkstra:
            self.escribir(
                "Ruta: " + " -> ".join(camino_dijkstra)
            )
            self.escribir(
                "Costo: " + str(int(costo_dijkstra))
            )
        else:
            self.escribir("Sin ruta.")

        arbol, costo_arbol, conectado_total = self.kruskal(False)

        self.escribir("\n4. KRUSKAL")

        for a, b in arbol:
            self.escribir(a + " -- " + b)

        self.escribir(
            "Costo del arbol: " + str(costo_arbol)
        )

        self.escribir("\n5. RESULTADO COMBINADO")

        if camino_dijkstra and camino_floyd:

            self.escribir(
                "Ruta minima: " + " -> ".join(camino_dijkstra)
            )

            self.escribir(
                "Costo minimo: " + str(int(costo_dijkstra))
            )

            if costo_dijkstra == costo_floyd:
                self.escribir("Dijkstra y Floyd coinciden.")

            ruta_arbol = self.ruta_en_arbol(arbol)

            if ruta_arbol:

                self.escribir(
                    "Ruta del arbol: " + " -> ".join(ruta_arbol)
                )

                costo_ruta = sum(
                    self.grafo[a][b]
                    for a, b in zip(ruta_arbol, ruta_arbol[1:])
                )

                self.escribir(
                    "Costo de esa ruta: " + str(costo_ruta)
                )

        else:

            self.escribir("No fue posible construir la ruta.")

        ruta = (
            list(zip(camino_dijkstra, camino_dijkstra[1:]))
            if camino_dijkstra else []
        )

        self.pintar(
            caminos=ruta,
            arbol=arbol
        )


if __name__ == "__main__":

    ventana = tk.Tk()
    app = GrafoApp(ventana)
    ventana.mainloop()
