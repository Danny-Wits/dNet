from dRender.window import Surface
from dRender.Tile import Tile
from dNet.aStar import *


class MapRunner:
    t: Tile = None
    t1: Tile = None
    t2: Tile = None

    TEXTAREA = [100, 650, 700, 700]
    PreviousText = 0

    def __init__(self):
        self.Tiles = []
        self.g = Surface(600, 700, title="A Star Practice")
        self.g.setOnClick(self.onClick)
        self.g.setKeyPress(self.onKeyPress)
        self.mode = "distance"

    def start(self):
        self.setMap()
        self.g.run()

    def setMap(self):
        for i in range(10):
            for j in range(10):
                self.Tiles.append(
                    Tile(self.g, j * 60, i * 60, id=i*10 + j).draw())
        self.g.update_idletasks()

    def getTile(self, x, y):
        row = y // Tile.SIZE
        col = x // Tile.SIZE
        return self.Tiles[row * 10 + col]

    def writeText(self, text, fontSize=16):
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
        print(f"Clicked at {event.x}, {event.y}")

    def onKeyPress(self, event):
        print(event.keysym)
        if (event.keysym == "d"):
            self.mode = "distance"
            print("Distance Mode")
        elif (event.keysym == "n"):
            self.mode = "neighbors"
            print("Neighbors Mode")
        elif (event.keysym == "r"):
            self.reset()

    def reset(self):
        if (self.t != None):
            neighbors = findNeighbors(self.t, self.Tiles)
            for neighbor in neighbors:
                neighbor.unselect()
            self.t.unselect()
            self.t = None
        if (self.t1 != None):
            self.t1.unselect()
            self.t1 = None
        if (self.t2 != None):
            self.t2.unselect()
            self.t2 = None

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
            self.t1.unselect()
            self.t2.unselect()
            self.g.update_idletasks()
            self.t1 = None
            self.t2 = None

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
