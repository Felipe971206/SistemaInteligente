import csv, heapq
from collections import defaultdict, namedtuple
from typing import Dict, List, Tuple, Optional

Edge = namedtuple("Edge", ["to", "time", "line"])

# -------------------------------
# 1. Cargar la red desde el CSV
# -------------------------------
def cargar_red_desde_csv(path_csv: str) -> Dict[str, List[Edge]]:
    """Carga la red desde un CSV (from,to,time,line) y la hace bidireccional."""
    red = defaultdict(list)
    with open(path_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            a = row["from"].strip()
            b = row["to"].strip()
            t = int(row["time"])
            l = row["line"].strip()
            red[a].append(Edge(b, t, l))
            red[b].append(Edge(a, t, l))  # bidireccional
    return red

# -------------------------------
# 2. Algoritmo de búsqueda
# -------------------------------
def mejor_ruta(red: Dict[str, List[Edge]], origen: str, destino: str,
               penalizacion_transbordo: int = 6) -> Tuple[Optional[int], List[Tuple[str, Optional[str]]]]:
    """
    Dijkstra con penalización por transbordo.
    Devuelve (minutos_totales, [(estación, línea_en_uso_hasta_aquí), ...])
    """
    pq = [(0, origen, None, [])]  # (costo, nodo, linea_actual, camino)
    visitado = dict()

    while pq:
        costo, nodo, linea_actual, camino = heapq.heappop(pq)

        clave = (nodo, linea_actual)
        if clave in visitado and visitado[clave] <= costo:
            continue
        visitado[clave] = costo

        nuevo_camino = camino + [(nodo, linea_actual)]
        if nodo == destino:
            return costo, nuevo_camino

        for e in red.get(nodo, []):
            extra = e.time
            if linea_actual is not None and e.line != linea_actual:
                extra += penalizacion_transbordo
            heapq.heappush(pq, (costo + extra, e.to, e.line, nuevo_camino))

    return None, []

# -------------------------------
# 3. Descripción amigable
# -------------------------------
def describir_ruta(camino: List[Tuple[str, Optional[str]]]) -> str:
    if not camino:
        return "No se encontró ruta."
    pasos = []
    for i in range(len(camino) - 1):
        est_actual, _ = camino[i]
        est_sig, linea_sig = camino[i + 1]
        pasos.append((est_actual, est_sig, linea_sig))

    if not pasos:
        return "Origen y destino son la misma estación."

    instrucciones = []
    linea = pasos[0][2]
    tramo_inicio = pasos[0][0]
    ultimo = pasos[0][1]

    for (a, b, l) in pasos[1:]:
        if l == linea:
            ultimo = b
        else:
            instrucciones.append(f"Toma la línea {linea} desde {tramo_inicio} hasta {ultimo}.")
            linea = l
            tramo_inicio = a
            ultimo = b
    instrucciones.append(f"Toma la línea {linea} desde {tramo_inicio} hasta {ultimo}.")
    return "\n".join(instrucciones)

# -------------------------------
# 4. Ejecución principal
# -------------------------------
if __name__ == "__main__":
    red = cargar_red_desde_csv("red_tm.csv")

    # Mostrar todas las estaciones disponibles
    estaciones = sorted(red.keys())
    print("=== PLANIFICADOR DE RUTAS TRANSMILENIO ===\n")
    print("Estaciones disponibles:")
    for i, est in enumerate(estaciones, start=1):
        print(f"{i}. {est}")
    print()

    # Selección de origen
    while True:
        try:
            origen_idx = int(input("Selecciona el número de la estación de ORIGEN: "))
            if 1 <= origen_idx <= len(estaciones):
                origen = estaciones[origen_idx - 1]
                break
            else:
                print("⚠️ Número fuera de rango, intenta de nuevo.")
        except ValueError:
            print("⚠️ Ingresa un número válido.")

    # Selección de destino
    while True:
        try:
            destino_idx = int(input("Selecciona el número de la estación de DESTINO: "))
            if 1 <= destino_idx <= len(estaciones):
                destino = estaciones[destino_idx - 1]
                break
            else:
                print("⚠️ Número fuera de rango, intenta de nuevo.")
        except ValueError:
            print("⚠️ Ingresa un número válido.")

    penalizacion = 6  # minutos por transbordo

    # Ejecutar búsqueda
    minutos, camino = mejor_ruta(red, origen, destino, penalizacion)

    # Mostrar resultado
    print("\n=== RESULTADO ===")
    if minutos is None:
        print("No se encontró ruta.")
    else:
        print(f"Tiempo estimado: {minutos} min")
        print(describir_ruta(camino))
        print("Ruta completa:", " -> ".join([n for n, _ in camino]))
