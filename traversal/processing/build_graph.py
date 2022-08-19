import pandas as pd
import pickle as pkl
from structures.graph import *
import numpy as np

# Зчитування даних
path = "../traversal/input_data/relations.xlsx"
with open(path, "rb") as wb_stream:
    wb = pd.read_excel(wb_stream, engine='openpyxl')

# Обираємо лише колонки з id (корінь-зв'язки)
wb = wb[1:]
# _DO_NOT_FILL_IT_OUT_1_ = Name correponds to person_id_from
# _DO_NOT_FILL_IT_OUT_2_ = Name corresponds to person_id_to
selected_columns = ["person_id_from", "person_id_to", "_DO_NOT_FILL_IT_OUT_1_", "_DO_NOT_FILL_IT_OUT_2_"]
wb_shortened = wb[selected_columns]

# Впорядковуємо за person_id_from, далі за person_id_to за зростанням
wb_shortened.sort_values(by=selected_columns[:2])

# Будуємо граф
wb_graph = Graph(oriented=False)

# По суті переносимо дані з "списку суміжностей" в екземпляр Graph
# Витратний за часом
for from_key in iter(set(wb_shortened["person_id_from"])):
    wb_subset = wb_shortened[wb_shortened["person_id_from"] == from_key]
    for to_key in wb_subset["person_id_to"]:
        if not to_key:
            name_for_id_to = wb_subset[wb_subset["person_id_to"] == to_key]["_DO_NOT_FILL_IT_OUT_1_"]
            wb_graph.add_vertex(from_key, name_for_id_to)
        else:
            name_for_id_from = np.squeeze(wb_subset[wb_subset["person_id_to"] == to_key]["_DO_NOT_FILL_IT_OUT_1_"])
            name_for_id_to = np.squeeze(wb_subset[wb_subset["person_id_to"] == to_key]["_DO_NOT_FILL_IT_OUT_2_"])
            wb_graph.add_edge(to_key, name_for_id_to, from_key, name_for_id_from)

# Збереження графа
path_graph = "../traversal/output_data/wb_graph.pkl"

with open(path_graph, "wb") as out:
    pkl.dump(wb_graph, out)
