import pickle as pkl
from structures.cluster import Cluster


# Зчитуємо граф
path_graph = "./data/output_data/wb_graph.pkl"
with open(path_graph, "rb") as gr_s:
    wb_graph = pkl.load(gr_s)

# Ключ - Путін
key = 880

# Побудуємо кластер за Путіним (зберемо усі пов'язані із його ключем інші)
key_cluster = Cluster(wb_graph)
key_cluster.fit(key)
