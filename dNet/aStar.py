from dRender.Tile import Tile
import numpy as np
import time


def distance(t1: Tile, t2: Tile):
    return np.round(np.hypot(t1.x - t2.x, t1.y - t2.y)/Tile.SIZE, 2)


def findNeighbors(t1: Tile, Map: list[Tile], diag=True):

    if t1 is None:
        return {}
    t1.select("NS")
    neighbors = set()
    row = t1.getRow()
    col = t1.getCol()
    limit = Tile.GRID_SIZE-1

    rowUp = row - 1 if row > 0 else 0
    rowDown = row + 1 if row < limit else limit
    colLeft = col - 1 if col > 0 else 0
    colRight = col + 1 if col < limit else limit
    limit = limit + 1
    neighborsId = {row * limit + colLeft, row * limit + colRight,
                   rowUp * limit + col, rowDown * limit + col,
                   rowUp * limit + colLeft, rowUp * limit + colRight,
                   rowDown * limit + colLeft, rowDown * limit + colRight
                   } if diag else {row * limit + colLeft, row * limit + colRight,
                                   rowUp * limit + col, rowDown * limit + col
                                   }
    for id in neighborsId:
        if id != t1.id and Map[id].isObstacle == False:
            neighbors.add(Map[id])
    for n in neighbors:
        n.select("N")
    return neighbors


def findPath(t1: Tile, t2: Tile, Map: list[Tile], visited=None):
    if visited == None:
        visited = set()
    if t1.id == t2.id:
        return [t1]
    visited.add(t1)

    #!GETTING THE NEIGHBORS
    neighbors = findNeighbors(t1, Map, diag=False)

    #! SORTING BASED ON DISTANCE
    sortedNeighbors = sorted(
        neighbors, key=lambda n: distance(n, t2))

    #! SEARCH THE CLOSEST NEIGHBOR TO THE GOAL
    for neighbor in sortedNeighbors:
        if neighbor not in visited:
            path = findPath(neighbor, t2, Map, visited)
            if path != None:
                return [t1] + path
    return None


def aStar(t1: Tile, t2: Tile, Map: list[Tile]):
    #!Evaluating source
    t1.h_cost = distance(t1, t2)
    open = {t1}  # adding t1 to open
    closed = set()  # set of evaluated nodes

    while True:

        #!Selecting Best Node
        current = min(open, key=lambda t: t.get_f_cost())

        #!Setting current to be processed
        open.remove(current)
        closed.add(current)

        #!Adding neighbors to open
        if current.id == t2.id:
            return current

        neighbor = findNeighbors(current, Map, diag=True)

        for n in neighbor:
            if n in closed:
                continue
            new_g_cost = current.g_cost+distance(current, n)
            if n not in open or new_g_cost < n.g_cost:

                #!Setting F cost
                n.g_cost = new_g_cost
                n.h_cost = distance(n, t2)

                # Setting Best parent
                n.parent = current
                if n not in open:
                    open.add(n)


def useAStar(t1: Tile, t2: Tile, Map: list[Tile]):
    target = aStar(t1, t2, Map)
    path = []
    while target.parent.id != t1.id:
        path.append(target)
        target = target.parent
    path.append(target)
    return path
