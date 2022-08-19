from processing.structures.graph import Graph


# TODO: subgraph based on cluster - DONE?
class Cluster:

    def __init__(self, graph: Graph):
        self.base_graph = graph
        self.subgraph = Graph()
        self.key_node = None
        self.elements = {}

    def delve(self):
        # Перелік сполучень одного вузла з іншим. Використовується для побудови шляху
        sources = {self.key_node: None}
        # Черга для вершин графа
        vertices_queue = [self.key_node]
        # Поки черга не є порожньою, проходимо граф як то робиться пошуком в ширину
        while len(vertices_queue) > 0:
            current_vertex = vertices_queue.pop(0)
            for neighbor in self.base_graph[current_vertex].get_neighbors():
                if neighbor not in sources:
                    vertices_queue.append(neighbor)
                    sources[neighbor] = current_vertex

        # source має мапу переходів. скористаємося цим для побудови маршрутів для кожного вузла
        routes = dict()
        for destination in sources:
            current_route = []
            current_vertex = destination
            while True:
                current_route.append(current_vertex)
                if current_vertex == self.key_node:
                    break
                current_vertex = sources[current_vertex]
            routes[destination] = current_route[::-1]

        # Навпаки, бо без цього шлях тоді виходить з кінцевого в початковий
        return routes

    def clean_contents(self):
        self.subgraph.clean_vertices()
        self.elements = {}

    def fit(self, key_node):
        self.key_node = key_node
        self.clean_contents()
        self.delve()

    def get_contents(self):
        return self.elements

    def get_key(self):
        return self.key_node

    def update_key(self, new_key):
        self.key_node = new_key
        self.delve()

    def build_subgraph(self):
        for key in self.elements.keys():
            for neighbor_key in self.base_graph[key].get_neighbors():
                vertex_name = self.base_graph[key].get_name()
                vertex_neighbor_name = self.base_graph[neighbor_key].get_name()
                self.subgraph.add_edge(key, vertex_name, neighbor_key, vertex_neighbor_name)

    def get_subgraph(self):
        return self.subgraph
