import dearpygui.dearpygui as dpg

class Node:
    equalityIndexes = [0, 1]

    def __init__(self, value, parent=None, children=None, ):
        self.value = value
        self.parent = parent
        self.children = children if children else []

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def add_children(self, children):
        for child in children:
            child.parent = self
            self.children.append(child)

    def print_children(self):
        print(self.children)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __eq__(self, node):
        if node == None:
            return False
        result = True
        for i in self.equalityIndexes:
            result = result and self.value[i] == node.value[i]
        return result

    def __hash__(self):
        return hash((self.value[0], self.value[1]))


class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_nodes(self, nodes):
        self.nodes.extend(nodes)

    def BFS(self, start, end):
        queue = [start]
        parents = {start: None}
        while queue:
            node = queue.pop(0)
            if node.__eq__(end):
                end = node
                print(f"Found : {node.value}")
                break
            for child in possible_states(node):
                if child in parents:
                    continue
                queue.append(child)
                parents[child] = node
                print(f"Visited : {child}")
        path = [end]
        while parents[end] != None:
            path.append(parents[end])
            end = parents[end]
        path.reverse()
        print(path)
        return path


def possible_states(node):
    water1 = node.value[0]
    water2 = node.value[1]
    capacity1 = node.value[2]
    capacity2 = node.value[3]
    states = []
    if (water1 != capacity1):
        states.append(
            Node([capacity1, water2, capacity1, capacity2]))
    if (water2 != capacity2):
        states.append(
            Node([water1, capacity2, capacity1, capacity2]))
    if (water1 != 0):
        states.append(Node([0, water2, capacity1, capacity2]))
    if (water2 != 0):
        states.append(Node([water1, 0, capacity1, capacity2]))
    if (water1 + water2 <= capacity1):
        states.append(
            Node([water1 + water2, 0, capacity1, capacity2]))
    if (water1 + water2 <= capacity2):
        states.append(
            Node([0, water1 + water2, capacity1, capacity2]))
    if (water1 + water2 > capacity1):
        states.append(
            Node([capacity1, water1 + water2 - capacity1, capacity1, capacity2]))
    if (water1 + water2 > capacity2):
        states.append(
            Node([water1 + water2 - capacity2, capacity2, capacity1, capacity2]))
    return states
