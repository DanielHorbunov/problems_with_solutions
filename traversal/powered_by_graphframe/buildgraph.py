from pyspark.sql import SparkSession
import graphframes as gf

import pandas as pd
import numpy as np
import pickle as pkl

import findspark
findspark.init()

spark = SparkSession.builder.getOrCreate()

path = "./data/input_data/relations.xlsx"
with open(path, "rb") as wb_stream:
    wb = pd.read_excel(wb_stream, engine='openpyxl')

#wbs = spark.createDataFrame(wb)

# Обираємо лише колонки з id (корінь-зв'язки)
#wb = wb[1:]
selected_columns = ["person_id_from", "person_id_to", "person_name_from", "person_name_to"]
first = wb[["person_id_from", "person_id_to", "person_name_from"]]
second = wb[["person_id_to", "person_id_from", "person_name_to"]]
f = first.rename({"person_id_from": "src", "person_id_to": "dst", "person_name_from": "relation"}, axis='columns').reset_index(drop=True)
s = second.rename({"person_id_from": "dst", "person_id_to": "src", "person_name_to": "relation"}, axis='columns').reset_index(drop=True)
wb_shortened = pd.concat([f, s], axis=0)
wb_shortened = wb_shortened.reset_index(drop=True)
wb_shortened = wb_shortened.drop_duplicates()
wb_shortened["relation"][wb_shortened["relation"].isna()] = "undefined"

# Впорядковуємо за person_id_from, далі за person_id_to за зростанням
#wb_shortened.sort_values(by=selected_columns[:2])
# name ?
vertices = pd.DataFrame({"id": pd.unique(wb_shortened["src"][wb_shortened["src"] != 0])})

edges_spark = spark.createDataFrame(wb_shortened[(wb_shortened["dst"] != 0) & (wb_shortened["src"] != 0)])
vertices_spark = spark.createDataFrame(vertices)

graph = gf.GraphFrame(v=vertices_spark, e=edges_spark)

#print("bfs?")
#res = graph.bfs('id = 880', 'id = 767')

# [880, 296, 2079, 17132, 472, 767]