from dRender.Tile import Tile
import numpy as np


def distance(t1: Tile, t2: Tile):
    return np.round(np.hypot(t1.x - t2.x, t1.y - t2.y)/Tile.SIZE, 2)


def findNeighbors(t1: Tile, Map: list[Tile]):

    if t1 is None:
        return {}
    neighbors = set()
    row = t1.getRow()
    col = t1.getCol()
    limit = int(np.sqrt(len(Map)))-1

    rowUp = row - 1 if row > 0 else 0
    rowDown = row + 1 if row < limit else limit
    colLeft = col - 1 if col > 0 else 0
    colRight = col + 1 if col < limit else limit

    neighborsId = {row * 10 + colLeft, row * 10 + colRight,
                   rowUp * 10 + col, rowDown * 10 + col,
                   rowUp * 10 + colLeft, rowUp * 10 + colRight,
                   rowDown * 10 + colLeft, rowDown * 10 + colRight
                   }
    for id in neighborsId:
        if id != t1.id and Map[id].isObstacle == False:
            neighbors.add(Map[id])
    return neighbors
