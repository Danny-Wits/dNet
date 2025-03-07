from dearpygui.dearpygui import *
from numpy import gcd
from Searches.Graphs import *
import time
jugSize = 150
bgColor = (255, 255, 255, 255)
y = 200
actions: list = []
solution: list = []


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


jug1 = Jug("Jug1", 0, 5, "drawList", x=50)
jug2 = Jug("Jug2", 0, 3, "drawList", x=80+jugSize)


def setJug1():
    jug1.capacity = get_value("jug1Capacity")
    jug1.draw()


def setJug2():
    jug2.capacity = get_value("jug2Capacity")
    jug2.draw()


def solve():
    if (jug1.capacity == 0 or jug2.capacity == 0):
        addToAction("Invalid Input")
        return
    target = get_value("Target") if get_value(
        "Target") != 0 else get_value("Target2")
    Node.equalityIndexes = [0] if get_value("Target") != 0 else [1]
    isFirstJug = get_value("Target") != 0
    hcf = gcd(jug1.capacity, jug2.capacity)
    print(f"Target: {target} jug: {Node.equalityIndexes[0]}")
    if (target % hcf != 0):
        addToAction("Can't Solve this state")
        return
    if (isFirstJug and target > jug1.capacity):
        addToAction("Target is greater than\n Jug1 capacity")
        return
    elif (not isFirstJug and target > jug2.capacity):
        addToAction("Target is greater than\n Jug2 capacity")
        return
    addToAction("Solving...")
    g = Graph()

    path = g.BFS(Node([jug1.water, jug2.water, jug1.capacity,
                       jug2.capacity]), Node([target if isFirstJug else 0, target if not isFirstJug else 0, jug1.capacity, jug2.capacity]))
    actionsToTake = []
    for i in range(len(path)-1):
        actionsToTake.append(get_action(path[i].value, path[i+1].value))
    resetSolution()
    for action in actionsToTake:
        addToSolution(action)
    addToAction("Solved")


def addToSolution(text):
    global solution
    solution.append(text)
    set_value("Solution", "Solution :\n"+"\n".join(solution))


def resetSolution():
    global solution
    solution = []
    set_value("Solution", "Solution :\n"+"\n".join(solution))


def performSolution():
    jug1.empty()
    jug2.empty()
    for action in solution:
        time.sleep(0.7)
        action = action[0]
        if (action == "1"):
            jug1.fill()
        elif (action == "2"):
            jug2.fill()
        elif (action == "3"):
            jug1.empty()
        elif (action == "4"):
            jug2.empty()
        elif (action == "5"):
            jug1.pour_to_other_until_full(jug2)
        elif (action == "6"):
            jug2.pour_to_other_until_full(jug1)


def get_action(state1: list, state2: list):
    initialWater1 = state1[0]
    finalWater1 = state2[0]
    capacity1 = state1[2]
    capacity2 = state1[3]
    initialWater2 = state1[1]
    finalWater2 = state2[1]
    # No Action
    if (initialWater1 == finalWater1 and initialWater2 == finalWater2):
        return "None"
    if (initialWater1 != finalWater1 and initialWater2 != finalWater2):
        if (initialWater1 > finalWater1):
            return "5 | Pour Jug 1 to Jug 2"
        else:
            return "6 | Pour Jug 2 to Jug 1"
    # Fill Jug 1
    if (finalWater1 == capacity1):
        return "1 | Fill Jug 1"
    # Fill Jug 2
    if (finalWater2 == capacity2):
        return "2 | Fill Jug 2"
    # Empty Jug 1
    if (finalWater1 == 0):
        return "3 |Empty Jug 1"
    # Empty Jug 2
    if (finalWater2 == 0):
        return "4 | Empty Jug 2"


# gui setup
create_context()

# Create a theme for window background color
with theme() as my_theme:
    with theme_component(mvWindowAppItem):
        add_theme_color(mvThemeCol_WindowBg, bgColor)
description = """This is a simple Water Jug Problem
Simulation and Solver.
It uses BFS to solve the problem.
Use the panels on the left to configure the problem.
Press Solve to solve the problem
Then Press Perform Solution to see the solution"""
with window(label="Tutorial", tag="Tutorial"):
    with drawlist(width=400, height=200, tag="drawList1"):
        draw_text(text="Water Jug Problem", pos=(10, 10), size=24,
                  color=(111, 45, 168, 255), tag="Title", parent="drawList1")
        draw_text(text=description, pos=(10, 40), size=14,
                  color=(0, 0, 0, 255), tag="Description", parent="drawList1")
with window(label="Main", tag="Main"):

    add_text(default_value="Actions :", pos=(760, 30),
             color=(0, 0, 0, 255), tag="Actions")
    add_text(default_value="Solution :",
             pos=(280, 30),
             color=(0, 0, 0, 255), tag="Solution")
    add_button(label="Perform Solution", pos=(
        280, 10), callback=performSolution)
    add_button(label="Pop Action", pos=(760, 10), callback=popAction)
    with drawlist(width=400, height=400, tag="drawList"):
        pass
with window(label="Jug 1 Controls", pos=(500, 0), width=250, height=150, tag="Controls1"):
    add_slider_int(label="Capacity", min_value=1, max_value=20, default_value=5,
                   tag="jug1Capacity", callback=setJug1)
    add_text(default_value="Actions")
    add_button(label="Fill Jug 1", callback=jug1.fill)
    add_button(label="Empty Jug 1", callback=jug1.empty)
    add_button(label="Pour to Jug 2",
               callback=lambda: jug1.pour_to_other_until_full(jug2))
with window(label="Jug 2 Controls", pos=(500, 200), width=250, height=150, tag="Controls2"):
    add_slider_int(label="Capacity", min_value=1, max_value=20, default_value=3,
                   tag="jug2Capacity", callback=setJug2)
    add_text(default_value="Actions")
    add_button(label="Fill Jug 2", callback=jug2.fill)
    add_button(label="Empty Jug 2", callback=jug2.empty)
    add_button(label="Pour to Jug 1",
               callback=lambda: jug2.pour_to_other_until_full(jug1))

bind_item_theme("Main", my_theme)
bind_item_theme("Tutorial", my_theme)
with window(label="Solver", pos=(500, 400), width=250, height=150, tag="Solver"):
    add_text(default_value="Set target value\nIf Target1 is 0\nthen Target2 is used",
             tag="TargetTitle")
    add_slider_int(label="Target1", min_value=0, max_value=19,
                   default_value=3, tag="Target")
    add_slider_int(label="Target2", min_value=1, max_value=19,
                   default_value=3, tag="Target2")
    add_button(label="Solve", callback=solve)

# starting the GUI


create_viewport(title='2 Jug Problem', width=1000, height=600)
setup_dearpygui()
bind_font(font)
show_viewport()
set_primary_window("Main", True)
jug1.draw()
jug2.draw()
start_dearpygui()


configure_item("drawList", width=get_item_width("Main"),
               height=get_item_height("Main"))
destroy_context()
