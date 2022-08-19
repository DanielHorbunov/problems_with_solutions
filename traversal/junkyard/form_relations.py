import pandas as pd
import pickle as pkl
from structures.graph import *

# Приклад застосування

# Зчитуємо граф
path_graph = "wb_graph.pkl"
with open(path_graph, "rb") as gr_s:
    wb_graph = pkl.load(gr_s)

# Ключ - Путін
key = 833

all_routes_from_key = get_routes(wb_graph, key)
all_routes_from_key.pop(key)
L = len(all_routes_from_key)

# check this
excel_file = "./related_key_%d.xlsx" % key
df_to_return = pd.DataFrame({
    "key_id": key,
    "related_id": list(all_routes_from_key.keys()),
    "path": [str(p)[1:-1].replace(",", ";") for p in all_routes_from_key.values()]
})
df_to_return.to_excel(excel_file, index=False)
