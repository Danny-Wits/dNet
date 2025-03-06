import dearpygui.dearpygui as dpg
from math import *
dpg.create_context()


# Define activation functions
activationFunctions = {
    "ReLU": lambda x: max(0, x),  # Rectified Linear Unit
    "Sigmoid": lambda x: 1 / (1 + exp(-x)),  # Sigmoid function
    "Tanh": lambda x: tanh(x),  # Hyperbolic Tangent
    # Exponential Linear Unit (ELU)
    "ELU": lambda x: x if x > 0 else 0.1 * (exp(x) - 1),
    "Swish": lambda x: x / (1 + exp(-x)),  # Swish activation
    "Softsign": lambda x: x / (1 + abs(x)),  # Softsign
}


x = [i/100 for i in range(-1000, 1000)]


with dpg.window(label="Activation Function Plot", tag="Plot"):
    # create plot
    with dpg.plot(label="Activation Functions", height=700, width=800):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")
        for func in activationFunctions:
            y = [activationFunctions[func](i) for i in x]
            dpg.add_line_series(x, y, label=func, tag=func, parent="y_axis")

dpg.create_viewport(title='Activation Function Plot', width=800, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Plot", True)

dpg.start_dearpygui()
dpg.destroy_context()
