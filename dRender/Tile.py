from dRender.window import Surface


class Tile:
    SIZE = 30
    COLOR = "#E6E6E6"
    COLORS = {"D": "red", "N": "#9FC3B2",
              "S": "#E6E6E6", "P": "blue", "NS": "green"}
    GRID_SIZE = 0

    def __init__(self, surface: Surface, x, y, size=SIZE, id=0, isObstacle=False, color=COLOR):
        self.surface = surface
        self.id = id
        self.x = x
        self.y = y
        self.isObstacle = isObstacle
        self.isStart = False
        self.isEnd = False
        Tile.SIZE = size
        self.color = "gray" if isObstacle else color
        self.g_cost = 0
        self.h_cost = 0
        self.parent = None

    def get_f_cost(self):
        return self.g_cost+self.h_cost

    def select(self, mode="D"):
        self.color = self.COLORS[mode]
        self.draw()
        self.surface.update_idletasks()

    def unselect(self):
        self.color = "gray" if self.isObstacle else self.COLOR
        self.draw()

    def setObstacle(self, value=True):
        self.isObstacle = value
        self.draw()
        self.surface.update_idletasks()

    def start(self):
        self.isStart = True
        self.draw()
        self.surface.update_idletasks()

    def end(self):
        self.isEnd = True
        self.draw()
        self.surface.update_idletasks()

    def finish(self):
        self.isStart = False
        self.isEnd = False
        self.color = self.COLOR
        self.draw()

    def getRow(self):
        return self.id // Tile.GRID_SIZE

    def getCol(self):
        return self.id % Tile.GRID_SIZE

    def draw(self):
        if self.isStart:
            self.color = "orange"
        elif self.isEnd:
            self.color = "purple"

        self.surface.create_rectangle(
            self.x, self.y, self.x + self.SIZE, self.y + self.SIZE, fill=self.color if not self.isObstacle else "black")
        self.surface.create_text(
            self.x + self.SIZE / 2, self.y + self.SIZE / 2, font=("Arial", 10), text=str(round(self.g_cost, 0))+" | "+str(round(self.h_cost, 0))+"\n  "+str(round(self.get_f_cost(), 1)), fill="black"

        )
        self.surface.create_rectangle(
            self.x, self.y, self.x + self.SIZE, self.y + self.SIZE, outline="white", width=2)
        return self
