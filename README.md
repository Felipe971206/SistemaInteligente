# TransMilenio Route Planner (AI + Reglas)

Sistema inteligente en **Python** que calcula la **mejor ruta** entre estaciones de **TransMilenio** usando:
- **Base de conocimiento** en CSV (`from,to,time,line`).
- **Búsqueda de caminos** con **Dijkstra** (equivalente a A* con heurística 0).
- **Penalización de transbordos** configurable para reducir cambios de línea.

> Proyecto académico/didáctico. Los tiempos incluidos son referenciales.

---

## 🚀 Características
- Red modelada como **grafo** bidireccional a partir de un CSV.
- **Penalización por transbordos** (p. ej., 4–8 min) para simular esperas.
- Instrucciones de viaje compactadas por línea (detecta transbordos).
- Fácil de **extender**: agrega filas al CSV sin tocar el código.
