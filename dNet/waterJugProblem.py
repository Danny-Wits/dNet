from dearpygui.dearpygui import *
# rules

jugSize = 150
bgColor = (255, 255, 255, 255)
y = 200
actions: list = []


def addToAction(action: str):
    actions.append(action)
    set_value("Actions", "Actions :\n"+"\n".join(actions))


def popAction():
    if (len(actions) == 0):
        return
    actions.pop()
    set_value("Actions", "Actions :\n"+"\n".join(actions))


class Jug:
    def __init__(self, name: str, water: int, capacity: int, drawList, x: int):
        self.name = name
        self.water = water
        self.capacity = capacity
        self.drawList = drawList
        self.pos = x
        self.lastText = None
        self.lastFill = None
        self.lastBorder = None

    def fill(self):
        addToAction(f"{self.name} filled")
        self.water = self.capacity
        self.draw()

    def empty(self):
        addToAction(f"{self.name} emptied")
        self.water = 0
        self.draw()

    def pour_to_other_until_full(self, otherJug):
        limit = otherJug.capacity - otherJug.water
        if (limit <= self.water):
            otherJug.water += limit
            self.water -= limit
            addToAction(f"{self.name} poured {limit} to {otherJug.name}")
        else:
            addToAction(f"{self.name} poured {self.water} to {otherJug.name}")
            otherJug.water += self.water
            self.water = 0
        self.draw()
        otherJug.draw()

    def draw(self):
        self.water = min(self.water, self.capacity)
        self.reset()
        self.lastBorder = draw_rectangle((self.pos, y), (self.pos+jugSize, y+jugSize), color=(
            0, 0, 0, 255), parent=self.drawList)
        draw_line(p1=(self.pos, y), p2=(self.pos+jugSize, y),
                  color=bgColor, thickness=10, parent=self.drawList)
        # filling the Jug
        self.lastFill = draw_rectangle((self.pos+1, y+jugSize-(jugSize*(self.water/self.capacity))),
                                       (self.pos+jugSize-1, y+jugSize-2), fill=(135, 206, 250, 255), parent=self.drawList)
        self.lastText = draw_text(text=f"{self.water}/{self.capacity}", size=20,
                                  pos=(self.pos, y-20), color=(0, 0, 0, 255), parent=self.drawList)

    def reset(self):
        delete_item(self.lastBorder)
        delete_item(self.lastText)
        delete_item(self.lastFill)


jug1 = Jug("Jug1", 0, 1, "drawList", x=50)
jug2 = Jug("Jug2", 0, 3, "drawList", x=80+jugSize)


def setJug1():
    jug1.capacity = get_value("jug1Capacity")
    jug1.draw()


def setJug2():
    jug2.capacity = get_value("jug2Capacity")
    jug2.draw()


# gui setup
create_context()

# Create a theme for window background color
with theme() as my_theme:
    with theme_component(mvWindowAppItem):
        add_theme_color(mvThemeCol_WindowBg, bgColor)

with window(label="Main", tag="Main"):
    add_text(default_value="Water Jug Problem",
             color=(0, 0, 0, 255), tag="Title")
    add_text(default_value="Actions :",
             color=(0, 0, 0, 255), tag="Actions")
    add_button(label="Pop Action", callback=popAction)
    with drawlist(width=400, height=400, tag="drawList"):
        pass
with window(label="Jug 1 Controls", pos=(550, 0), width=200, height=150, tag="Controls1"):
    add_slider_int(label="Capacity", min_value=1, max_value=10,
                   tag="jug1Capacity")
    add_button(label="Set Jug 1", callback=setJug1)
    add_button(label="Fill Jug 1", callback=jug1.fill)
    add_button(label="Empty Jug 1", callback=jug1.empty)
    add_button(label="Pour to Jug 2",
               callback=lambda: jug1.pour_to_other_until_full(jug2))
with window(label="Jug 2 Controls", pos=(550, 200), width=200, height=150, tag="Controls2"):
    add_slider_int(label="Capacity", min_value=1, max_value=10,
                   tag="jug2Capacity")
    add_button(label="Set Jug 2", callback=setJug2)
    add_button(label="Fill Jug 2", callback=jug2.fill)
    add_button(label="Empty Jug 2", callback=jug2.empty)
    add_button(label="Pour to Jug 1",
               callback=lambda: jug2.pour_to_other_until_full(jug1))

bind_item_theme("Main", my_theme)


# starting the GUI
create_viewport(title='2 Jug Problem', width=800, height=600)
setup_dearpygui()
show_viewport()
set_primary_window("Main", True)

start_dearpygui()

print(get_item_width("Main"))
configure_item("drawList", width=get_item_width("Main"),
               height=get_item_height("Main"))
jug1.draw()
jug2.draw()
destroy_context()
