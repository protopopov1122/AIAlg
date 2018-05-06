class Vertex:
    def __init__(self, name):
        self.name = name
        self.predecessors: list = list()
        self.successors: list = list()

    def add_predecessors(self, *args):
        for pred in args:
            if pred not in self.predecessors:
                self.predecessors.append(pred)
        return self

    def add_successors(self, *args):
        for suc in args:
            if suc not in self.successors:
                self.successors.append(suc)
        return self

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    @staticmethod
    def create(struct: dict):
        vertices = dict()
        Vertex._struct_vertices(struct, vertices)
        Vertex._connect_vertices(struct, vertices)
        return vertices

    @staticmethod
    def _struct_vertices(graph: dict, vertices: dict):
        for key, value in graph.items():
            if key not in vertices:
                vertex = Vertex(key)
                vertices[key] = vertex
            if type(value) == dict:
                Vertex._struct_vertices(value, vertices)

    @staticmethod
    def _connect_vertices(graph: dict, vertices: dict):
        for key, value in graph.items():
            vertex = vertices[key]
            if type(value) == dict:
                for nkey in value:
                    nver = vertices[nkey]
                    vertex.add_successors(nver)
                    nver.add_predecessors(vertex)
                Vertex._connect_vertices(value, vertices)
            elif type(value) == list:
                for nkey in value:
                    nver = vertices[nkey]
                    vertex.add_successors(nver)
                    nver.add_predecessors(vertex)
            elif value is not None:
                nver = vertices[value]
                vertex.add_successors(nver)
                nver.add_predecessors(vertex)


class DFSOpened:
    def __init__(self):
        self.opened = []

    def add_vertex(self, vertex):
        self.opened.append(vertex)

    def get_vertex(self):
        if self.opened:
            return self.opened.pop()
        else:
            return None

    def is_empty(self):
        return len(self.opened) == 0

    def __str__(self):
        return str(self.opened)


class BFSOpened:
    def __init__(self):
        self.opened = []

    def add_vertex(self, vertex):
        self.opened.append(vertex)

    def get_vertex(self):
        if self.opened:
            return self.opened.pop(0)
        else:
            return None

    def is_empty(self):
        return len(self.opened) == 0

    def __str__(self):
        return str(self.opened)


def _traverse_backtrack(source: [Vertex], targets: [Vertex], meta: {Vertex: Vertex}, backwards: bool):
    path = dict()
    for target in targets:
        if target in meta:
            current = target
            path[target] = [current]
            while current not in source:
                current = meta[current]
                path[target].append(current)
            path[target].reverse()
        else:
            path[target] = None
    return path


def traverse(source: [Vertex], targets: [Vertex], opened_class, backwards: bool = False, any_target: bool = False):
    meta = dict()
    opened = opened_class()
    closed = set()
    if not backwards:
        for src in source:
            opened.add_vertex(src)
    else:
        for dst in targets:
            opened.add_vertex(dst)
    iter = 0

    def targets_found(targets, meta):
        return sum([1 for dst in targets if dst in meta])
    while not opened.is_empty() and targets_found(targets if not backwards else source, meta) < (1 if any_target else len(targets)):
        iter += 1
        subroot: Vertex = opened.get_vertex()
        closed.add(subroot)
        vertices: [Vertex] = subroot.successors if not backwards else subroot.predecessors
        for vert in vertices:
            if vert not in closed:
                iter += 1
                meta[vert] = subroot
                opened.add_vertex(vert)
    return _traverse_backtrack(source if not backwards else targets, targets if not backwards else source, meta, backwards), iter


def main():
    graph = {
        1: {
            2: {
                5: {},
                6: {},
                7: {}
            },
            3: {
                8: {},
                9: {},
                10: {}
            },
            4: {
                11: {},
                12: {
                    100: 101,
                    101: 102,
                    102: None
                },
                13: {}
            }
        }
    }
    vertices = Vertex.create(graph)
    path, iterations = traverse([vertices[1]], [vertices[13], vertices[102]], DFSOpened)
    print(path)
    print(iterations)


if __name__ == '__main__':
    main()
