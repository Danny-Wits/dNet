from dRender.window import Surface
from dRender.Tile import Tile
from dNet.aStar import *


class MapRunner:
    t: Tile = None
    t1: Tile = None
    t2: Tile = None

    TEXTAREA = [10, 700, 700, 700]
    PreviousText = 0
    GRID_SIZE = 10

    def __init__(self):
        self.Tiles = []
        self.g = Surface(800, 800, title="A Star Practice")
        self.g.setOnClick(self.onClick)
        self.g.setKeyPress(self.onKeyPress)
        self.g.setRightClick(self.onRightClick)
        self.mode = "path"
        self.writeTitle("Using Best First Search aka Greedy BFS", 14)

    def start(self):
        self.setMap()
        self.g.run()

    def setMap(self):

        size = MapRunner.GRID_SIZE
        Tile.GRID_SIZE = size
        for i in range(size):
            for j in range(size):
                self.Tiles.append(
                    Tile(self.g, j * Tile.SIZE, i * Tile.SIZE, size=600//size, id=size * i + j).draw())
        self.g.update_idletasks()

    def getTile(self, x, y):
        row = y // Tile.SIZE
        col = x // Tile.SIZE
        return self.Tiles[row * Tile.GRID_SIZE + col]

    def writeTitle(self, text, fontSize=12):
        self.g.create_text(
            10, 610, text=text, font=("DIGIFACE", fontSize), justify="left", fill="black", anchor="nw"
        )

    def writeText(self, text, fontSize=12):
        self.PreviousText = self.g.create_text(
            self.TEXTAREA[0], self.TEXTAREA[1], text=text, font=("Monospace", fontSize), justify="left", fill="black", anchor="nw")

    def clearText(self):
        self.g.delete(self.PreviousText)

    def onClick(self, event):
        if (event.x < 0 or event.x > 600 or event.y < 0 or event.y > 600):
            return
        if self.mode == "distance":
            self.distanceTest(event=event)
        elif self.mode == "neighbors":
            self.neighborsTest(event=event)
        elif self.mode == "path":
            self.pathTest(event=event)
        print(f"Clicked at {event.x}, {event.y}")

    def onKeyPress(self, event):
        if (event.keysym == "d"):
            self.mode = "distance"
            print("Distance Mode")
        elif (event.keysym == "n"):
            self.mode = "neighbors"
            print("Neighbors Mode")
        elif (event.keysym == "p"):
            self.mode = "path"
            print("Path Mode")
        elif (event.keysym == "c"):
            self.clearText()
        elif (event.keysym == "r"):
            self.reset()

    def onRightClick(self, event):
        if (event.x < 0 or event.x > 600 or event.y < 0 or event.y > 600):
            return
        tile = self.getTile(event.x, event.y)
        tile.setObstacle(not tile.isObstacle)
        tile.finish()

    def reset(self):
        self.t = None
        self.t1 = None
        self.t2 = None
        for tile in self.Tiles:
            tile.unselect()
            tile.finish()
        self.g.update_idletasks()

    # Interactions

    def distanceTest(self, event):
        self.clearText()
        if (self.t1 == None):
            self.t1 = self.getTile(event.x, event.y)
            self.t1.select()
            self.writeText(f"Selected: {self.t1.id} ")
            self.g.update_idletasks()
            return
        elif (self.t2 == None):
            self.t2 = self.getTile(event.x, event.y)
            self.t2.select()
            self.g.update_idletasks()
            self.writeText(
                f"Selected:{self.t1.id} =>{self.t2.id} Distance: {distance(self.t1, self.t2)}")
        else:
            self.reset()

    def neighborsTest(self, event):
        self.clearText()
        if (self.t == None):
            self.t = self.getTile(event.x, event.y)
            self.t.select()
            neighbors = findNeighbors(self.t, self.Tiles)
            for neighbor in neighbors:
                neighbor.select("N")
            message = [f"{t.id}: {distance(self.t, t)}" for t in neighbors]
            self.writeText(f"Neighbors: {message}", fontSize=10)
        else:
            neighbors = findNeighbors(self.t, self.Tiles)
            for neighbor in neighbors:
                neighbor.unselect()
            self.t.unselect()
            self.t = self.getTile(event.x, event.y)
            self.t.select()
            neighbors = findNeighbors(self.t, self.Tiles)
            for neighbor in neighbors:
                neighbor.select("N")
            message = [f"{t.id}: {distance(self.t, t)}" for t in neighbors]
            self.writeText(f"Neighbors: {message}", fontSize=10)

    def pathTest(self, event=None):
        self.clearText()

        if (self.t1 == None):
            self.t1 = self.getTile(event.x, event.y)
            self.t1.start()
            self.writeText(f"Selected: {self.t1.id} ")
            return
        elif (self.t2 == None):
            self.t2 = self.getTile(event.x, event.y)
            self.t2.end()
            path = findPath(self.t1, self.t2, self.Tiles)
            self.writeText(
                f"Selected:{self.t1.id} =>{self.t2.id} Path: {[t.id for t in path]}")
            for tile in path:
                tile.select("P")
        else:
            self.reset()
