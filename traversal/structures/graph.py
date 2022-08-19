# Клас "вузол" -- потрібен для реалізації класу "вершина".
# Атрибути:
# key -- ключ вузла, визначається за вказаним в конструкторі
# Методи:
# get_key -- отримати значення ключа вузла
class Node:

    def __init__(self, key, name):
        self.key = key
        self.name = name

    def get_key(self):
        return self.key

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name


# Клас "вершина" -- нащадок класу "вузол", є реалізацією вершини графа.
# Атрибути:
# key <-- Node
# neighbors -- перелік вершин, які виходять із заданої
# Методи:
# add_neighbor -- додати "сусіда" до вершини, вводиться або ключ, або екземпляр відповідного класу
# get_neighbors -- отримати власне "сусідів"
class Vertex(Node):

    def __init__(self, key, name):
        super().__init__(key, name)
        self.neighbors = {}

    def add_neighbor(self, vertex):
        if isinstance(vertex, Node):
            self.neighbors[vertex.get_key()] = 1
        else:
            self.neighbors[vertex] = 1

    def get_neighbors(self):
        return self.neighbors.keys()

# Клас "граф" -- реалізація безпосередньо графа.
# Атрибути:
# vertices -- перелік вершин
# vertex_num -- кількість вершин
# oriented -- чи є граф орієнтованим (True / False)
# Методи:
# add_vertex -- додати вершину до графа
# get_vertex -- повернути вершину графа за вказаним ключем
# get_vertices -- отримати усі вершини графа
# add_edge -- з'єднати одну вершину з іншкою. якщо таких немає, то спочатку додаються
# Перенавантаження на __iter__, __len__, __getitem__ для зручності
class Graph:

    def __init__(self, oriented=False):
        self.vertices = {}
        self.vertex_num = 0
        self.oriented = oriented

    def add_vertex(self, vertex, name):
        if vertex in self:
            return False

        new_vertex = Vertex(vertex, name)
        self.vertices[vertex] = new_vertex
        self.vertex_num += 1

        return True

    def get_vertex(self, vertex):
        assert vertex in self

        key = vertex
        return self.vertices[key]

    def get_vertices(self):
        return self.vertices

    def add_edge(self, from_vertex, name_from, to_vertex, name_to):
        if from_vertex not in self:
            self.add_vertex(from_vertex, name_from)
        if to_vertex not in self:
            self.add_vertex(to_vertex, name_to)

        self[from_vertex].add_neighbor(to_vertex)
        if not self.oriented:
            self[to_vertex].add_neighbor(from_vertex)

    def __contains__(self, vertex):
        if isinstance(vertex, Node):
            return vertex.get_key() in self.vertices
        else:
            return vertex in self.vertices

    def __iter__(self):
        return iter(self.vertices.values())

    def __len__(self):
        return self.vertex_num

    def __getitem__(self, vertex):
        return self.get_vertex(vertex)


# Знаходження найкоротшого шляху на графі graph, що веде з вершини from_vertex до to_vertex
def get_route(graph, from_vertex, to_vertex):
    assert from_vertex != to_vertex
    # Перелік сполучень одного вузла з іншим. Використовується для побудови шляху
    sources = {from_vertex: None}
    # Черга для вершин графа
    vertices_queue = [from_vertex]
    # Поки черга не є порожньою, проходимо граф як то робиться пошуком в ширину
    while len(vertices_queue) > 0:
        current_vertex = vertices_queue.pop(0)
        for neighbor in graph[current_vertex].get_neighbors():
            if neighbor not in sources:
                vertices_queue.append(neighbor)
                sources[neighbor] = current_vertex
                # Якщо один з нащадків є кінцевим вузлом шляху -- зупиняємо цикл
                if neighbor == to_vertex:
                    break

    # Перевірка на досяжність кінцевої вершини із заданого старту
    if to_vertex not in sources:
        return []

    # Якщо все ок, будуємо шлях на основі сполучень з source
    route = []
    current_vertex = to_vertex
    while True:
        route.append(current_vertex)

        if current_vertex == from_vertex:
            break
        current_vertex = sources[current_vertex]

    # Навпаки, бо без цього шлях тоді виходить з кінцевого в початковий
    return route[::-1]


# Знаходження пов'язаних вузлів та шляхів до них
def get_routes(graph, from_vertex):
    # Перелік сполучень одного вузла з іншим. Використовується для побудови шляху
    sources = {from_vertex: None}
    # Черга для вершин графа
    vertices_queue = [from_vertex]
    # Поки черга не є порожньою, проходимо граф як то робиться пошуком в ширину
    while len(vertices_queue) > 0:
        current_vertex = vertices_queue.pop(0)
        for neighbor in graph[current_vertex].get_neighbors():
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
            if current_vertex == from_vertex:
                break
            current_vertex = sources[current_vertex]
        routes[destination] = current_route[::-1]

    # Навпаки, бо без цього шлях тоді виходить з кінцевого в початковий
    return routes
