import numpy as np
import pickle as pkl
from structures.graph import *

# Приклад застосування

# Зчитуємо граф
path_graph = "wb_graph.pkl"
with open(path_graph, "rb") as gr_s:
    wb_graph = pkl.load(gr_s)

vertices = np.array(list(wb_graph.get_vertices().keys()))
components = []

while len(vertices) > 0:
    pivot = vertices[0]
    all_routes_from_key = get_routes(wb_graph, pivot)
    components.append(all_routes_from_key)
    vertices = np.setdiff1d(vertices, list(all_routes_from_key.keys()))

lengths = [len(c) for c in components]
mx_comp = components[np.argmax(lengths)]
mn_comp = components[np.argmin(lengths)]

from collections import Counter
c = Counter(lengths)
print({i: c[i] for i in sorted(c.keys())})

