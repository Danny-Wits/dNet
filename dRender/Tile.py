from dRender.window import Surface


class Tile:
    SIZE = 60
    COLOR = "#CAF1DE"
    COLORS = {"D": "red", "N": "#9FC3B2", "S": "#E6E6E6"}

    def __init__(self, surface: Surface, x, y, id=0, isObstacle=False, width=SIZE, height=SIZE, color=COLOR):
        self.surface = surface
        self.id = id
        self.x = x
        self.y = y
        self.isObstacle = isObstacle
        self.width = width
        self.height = height
        self.color = "gray" if isObstacle else color

    def select(self, mode="D"):
        self.color = self.COLORS[mode]
        self.draw()

    def unselect(self):
        self.color = "gray" if self.isObstacle else self.COLOR
        self.draw()

    def getRow(self):
        return self.id // 10

    def getCol(self):
        return self.id % 10

    def draw(self):
        self.surface.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height, fill=self.color)
        self.surface.create_text(
            self.x + self.width / 2, self.y + self.height / 2, text=str(self.id), fill="black"
        )
        self.surface.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height, outline="white", width=2)
        return self
