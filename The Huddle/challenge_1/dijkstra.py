class Graph:
    def __init__(self, graph: dict={}):
        self.graph = graph

    def distancias_cortas(self, source):
        distancias = {node: float("inf") for node in self.graph}
        distancias[source] = 0 # se inicializa la fuente en cero
        print(distancias)

if __name__=="__main__":
    test_adj = {
        'A': {'B':1, 'C':3},
        'B': {'C':2}
    }
    graph = Graph(test_adj)
    print(graph.graph)
    graph.distancias_cortas('A')