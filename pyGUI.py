from dearpygui.dearpygui import *

create_context()
x = 0


def increment():
    global x
    x += 1
    print(get_value("Count"))
    set_value("Count", "Count : " + str(x))


with window(label="Tutorial", width=500, height=500, tag="Tutorial"):
    add_button(label="Click", callback=increment)
with window(label="Main", tag="Main"):
    add_text("Count : " + str(x), tag="Count")
    add_text("Count : " + str(x), tag="Count1")


# starting the GUI
create_viewport(title='DEARPYGUI', width=800, height=600)
setup_dearpygui()
show_viewport()
set_primary_window("Main", True)
start_dearpygui()
destroy_context()
