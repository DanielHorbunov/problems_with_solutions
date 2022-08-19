import pandas as pd
import pickle as pkl
from processing.structures.graph import *

# Приклад застосування

# Зчитуємо граф
path_graph = "../traversal/processing/data/output_data/wb_graph.pkl"
with open(path_graph, "rb") as gr_s:
    wb_graph = pkl.load(gr_s)

# Ключ - Путін
key = 880

# Знаходимо шляхи для осіб з наступними id
destinations = [995, 1856, 16440, 3130, 6039, 767]

# Маршрути записуємо у масив
results = []
results_n = []

# Знаходимо маршрути, якщо існують; в іншому разі None
for destination in destinations:
    current_path = get_route(wb_graph, key, destination)
    results.append(str(current_path))

# Комбінуємо у датафрейм
df_results = pd.DataFrame({"destination": destinations, "path": results})