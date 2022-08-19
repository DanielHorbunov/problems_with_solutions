import pickle as pkl
from structures.cluster import Cluster, split_graph


# Зчитуємо граф
path_graph = "./data/output_data/wb_graph.pkl"
with open(path_graph, "rb") as gr_s:
    wb_graph = pkl.load(gr_s)

# Ключ - Путін
key = 880

# Побудуємо кластер за Путіним (зберемо усі пов'язані із його ключем інші)
key_cluster = Cluster(wb_graph)
key_cluster.fit(key)

# Розбиваємо граф на кластери
clusters_list = split_graph(wb_graph)

