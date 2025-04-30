from collections import deque
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Створюємо граф
G = nx.DiGraph()

# Додаємо ребра з пропускною здатністю
edges = [
    ("Термінал 1", "Склад 1", 25),  # Термінал 1 ->	Склад 1
    ("Термінал 1", "Склад 2", 20),  # Термінал 1 ->	Склад 2
    ("Термінал 1", "Склад 3", 15),  # Термінал 1 ->	Склад 3
    ("Термінал 2", "Склад 3", 15),  # Термінал 2 ->	Склад 3
    ("Термінал 2", "Склад 4", 30),  # Термінал 2 ->	Склад 4
    ("Термінал 2", "Склад 2", 10),  # Термінал 2 ->	Склад 2
    ("Склад 1", "Магазин 1", 15),  # Склад 1 ->	Магазин 1
    ("Склад 1", "Магазин 2", 10),  # Склад 1 ->	Магазин 2
    ("Склад 1", "Магазин 3", 20),  # Склад 1 ->	Магазин 3
    ("Склад 2", "Магазин 4", 15),  # Склад 2 ->	Магазин 4
    ("Склад 2", "Магазин 5", 10),  # Склад 2 ->	Магазин 5
    ("Склад 2", "Магазин 6", 25),  # Склад 2 ->	Магазин 6
    ("Склад 3", "Магазин 7", 20),  # Склад 3 ->	Магазин 7
    ("Склад 3", "Магазин 8", 15),  # Склад 3 ->	Магазин 8
    ("Склад 3", "Магазин 9", 10),  # Склад 3 ->	Магазин 9
    ("Склад 4", "Магазин 10", 20), # Склад 4 ->	Магазин 10
    ("Склад 4", "Магазин 11", 10), # Склад 4 ->	Магазин 11
    ("Склад 4", "Магазин 12", 15), # Склад 4 ->	Магазин 12
    ("Склад 4", "Магазин 13", 5),  # Склад 4 ->	Магазин 13
    ("Склад 4", "Магазин 14", 10)  # Склад 4 ->	Магазин 14
]

# Додаємо всі ребра до графа
G.add_weighted_edges_from(edges)

# Позиції для малювання графа
pos = {
    "Термінал 1": (1, 2),
    "Термінал 2": (5, 2),
    "Склад 1": (2, 3),
    "Склад 2": (4, 3),
    "Склад 3": (2, 1),
    "Склад 4": (4, 1),
    "Магазин 1": (0, 4),
    "Магазин 2": (1, 4),
    "Магазин 3": (2, 4),
    "Магазин 4": (3, 4),
    "Магазин 5": (4, 4),
    "Магазин 6": (5, 4),
    "Магазин 7": (0, 0),
    "Магазин 8": (1, 0),
    "Магазин 9": (2, 0),
    "Магазин 10": (3, 0),
    "Магазин 11": (4, 0),
    "Магазин 12": (5, 0),
    "Магазин 13": (6, 0),
    "Магазин 14": (7, 0)
}

# Малюємо граф
plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=7, font_weight="bold", arrows=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Відображаємо граф
plt.show()


# Визначення вузлів
TERMINALS = [0, 1]
WAREHOUSES = [2, 3, 4, 5]
SHOPS = list(range(6, 20))
SRC, SNK = 20, 21
N = 22  # загальна кількість вузлів

# Матриця пропускної здатності
capacity_matrix = np.zeros((N, N), dtype=int)

# Вихідна матриця 20x20 з умови задачі
base_rows = [
    # T1  T2  С1  С2  С3  С4  M1  M2  M3  M4  M5  M6  M7  M8  M9  M10 M11 M12 M13 M14 
    [ 0,  0,  25, 20, 15,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # T1
    [ 0,  0,   0, 10, 15, 30,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # T2
    [ 0,  0,   0,  0,  0,  0, 15, 10, 20,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # S1
    [ 0,  0,   0,  0,  0,  0,  0,  0,  0, 15, 10, 25,  0,  0,  0,  0,  0,  0,  0,  0],  # S2
    [ 0,  0,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 20, 15, 10,  0,  0,  0,  0,  0],  # S3
    [ 0,  0,   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 20, 10, 15,  5, 10]   # S4
] + [[0]*20 for _ in range(14)]  # Магазини: нулі

capacity_matrix[:20, :20] = base_rows

# Додаємо супер-джерело та супер-стік
BIG = 1_000_000
for t in TERMINALS:
    capacity_matrix[SRC][t] = BIG
for s in SHOPS:
    capacity_matrix[s][SNK] = BIG

# BFS пошук шляху
def bfs(capacity_matrix, flow, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True
    while queue:
        u = queue.popleft()
        for v in range(len(capacity_matrix)):
            if not visited[v] and capacity_matrix[u][v] - flow[u][v] > 0:
                parent[v] = u
                visited[v] = True
                if v == sink:
                    return True
                queue.append(v)
    return False

# Алгоритм Едмондса-Карпа
def edmonds_karp(capacity_matrix, source, sink):
    n = len(capacity_matrix)
    flow = np.zeros((n, n), dtype=int)
    parent = [-1] * n
    max_flow = 0
    while bfs(capacity_matrix, flow, source, sink, parent):
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, capacity_matrix[u][v] - flow[u][v])
            v = u
        max_flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u
    return max_flow, flow

# Запуск алгоритму
max_flow, flow = edmonds_karp(capacity_matrix, SRC, SNK)

# Розрахунок термінал → магазин
result = []
remaining = flow.copy()
for t in TERMINALS:
    for w in WAREHOUSES:
        tw = remaining[t][w]
        if tw > 0:
            for m in SHOPS:
                wm = remaining[w][m]
                sent = min(tw, wm)
                if sent > 0:
                    result.append((f"Термінал {t+1}", f"Магазин {m-5}", sent))
                    remaining[t][w] -= sent
                    remaining[w][m] -= sent
                    tw -= sent

# Вивід
df = pd.DataFrame(result, columns=["Термінал", "Магазин", "Фактичний Потік (одиниць)"])
df = df.sort_values(by=["Термінал", "Магазин"])

print(f"Максимальний потік: {max_flow}")
print(df.to_markdown(index=False))