import random


class Edge:
    def __init__(self, destination):
        self.destination = destination


class Vertex:
    def __init__(self, value='default', **pos):  # TODO: Test default arguments
        self.value = value
        self.color = 'white'
        self.pos = pos
        self.edges = []


class Graph:
    def __init__(self):
        self.vertexes = []

    def debug_create_test_data(self):
        debug_vertex_1 = Vertex('t1', x=40, y=40)
        debug_vertex_2 = Vertex('t2', x=140, y=140)
        debug_vertex_3 = Vertex('t3', x=300, y=400)
        debug_vertex_4 = Vertex('t4', x=350, y=250)
        debug_vertex_5 = Vertex('t5', x=400, y=300)

        debug_edge_1 = Edge(debug_vertex_1)
        debug_edge_2 = Edge(debug_vertex_2)
        debug_edge_3 = Edge(debug_vertex_3)
        debug_edge_4 = Edge(debug_vertex_4)
        debug_edge_5 = Edge(debug_vertex_5)

        debug_vertex_1.edges.append(debug_edge_2)
        debug_vertex_2.edges.append(debug_edge_1)

        debug_vertex_2.edges.append(debug_edge_3)
        debug_vertex_3.edges.append(debug_edge_2)

        debug_vertex_3.edges.append(debug_edge_4)
        debug_vertex_4.edges.append(debug_edge_3)

        debug_vertex_4.edges.append(debug_edge_5)
        debug_vertex_5.edges.append(debug_edge_4)

        self.vertexes.extend(
            [debug_vertex_1, debug_vertex_2, debug_vertex_3, debug_vertex_4, debug_vertex_5])

    def bfs(self, start):
        print('called BFS')
        random_color = "#" + \
            ''.join([random.choice('0123456789ABCDEF') for j in range(6)])

        queue = []
        found = []

        queue.append(start)
        found.append(start)

        start.color = random_color

        print('about to start while')
        while len(queue) > 0:
            v = queue[0]
            for edge in v.edges:
                if edge.destination not in found:
                    found.append(edge.destination)
                    queue.append(edge.destination)
                    edge.destination.color = random_color

            queue.pop(0)  # TODO: Look at collections.dequeue

        print('about to return')
        # return found

    def get_connected_components(self):
        searched = []

        for vertex in self.vertexes:
            if vertex not in searched:
                searched = searched.append(self.bfs(vertex))

        return searched

    def randomize(self, width, height, circle, probability):
        def connect_verts(v0, v1):
            v0.edges.append(Edge(v1))
            v1.edges.append(Edge(v0))
        count = 0
        ### BUILD A GRID OF VERTS ###
        grid = []
        for y in range(height):
            row = []
            for x in range(height):
                v = Vertex("", x=0, y=0)
                v.value = 'v' + str(count)
                row.append(v)
            grid.append(row)

        # Go through the grid randomly hooking up edges
        for y in range(height):
            for x in range(width):
                # connect down
                if y < height - 1:
                    if random.randint(0, 100) < probability:
                        connect_verts(grid[y][x], grid[y + 1][x])

                if x < width - 1:
                    if random.randint(0, 100) < probability:
                        connect_verts(grid[y][x], grid[y][x + 1])

        # Last pass, set the x and y coordinates for drawing
        boxBuffer = 0.8
        boxInner = circle * boxBuffer
        boxInnerOffset = (circle - boxInner) / 2

        for y in range(height):
            for x in range(width):
                grid[y][x].pos['x'] = x * circle + \
                    boxInnerOffset + random.randint(0, 100) * boxInner

                grid[y][x].pos['y'] = y * circle + \
                    boxInnerOffset + random.randint(0, 100) * boxInner

        for y in range(height):
            for x in range(width):
                self.vertexes.append(grid[y][x])
