from graph import get_routes, Graph


# TODO: subgraph based on cluster
class Cluster:

    def __init__(self, graph: Graph):
        self.base_graph = graph
        self.key_node = None
        self.elements = {}

    def delve(self):
        self.elements = get_routes(self.base_graph, self.key_node)

    def fit(self, key_node):
        self.key_node = key_node
        self.delve()

    def get_contents(self):
        return self.elements

    def get_key(self):
        return self.key_node

    def update_key(self, new_key):
        self.key_node = new_key
        self.delve()
