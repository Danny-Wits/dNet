import matplotlib.pyplot as plt
from dNet.perceptron import Perceptron
import matplotlib.animation as animation
import numpy as np


def test(inputs):
    return 1 if inputs[0] * 2 + inputs[1] >= 1 else 0


# Initialize perceptron
p = Perceptron(2, 0, [0.1, 0.1])
limit = 1000
# Create figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Generate data points
inputs = np.random.rand(limit, 2)
# Add OR gate points
inputs = np.vstack((inputs, [0, 0], [0, 1], [1, 0], [1, 1]))
l = len(inputs)
outputs = np.array([test(i) for i in inputs])

# Initialize scatter plot
colors = np.array(["red" if p.predict(i) == 0 else "blue" for i in inputs])
scatter = ax.scatter(inputs[:, 1], inputs[:, 0], c=colors, marker="o")


def update(frame):
    global scatter
    global inputs
    global outputs
    global l
    global limit
    if (frame == 0):
        # Check if perceptron has already learned
        if (outputs == np.array([p.predict(i) for i in inputs])).all():
            print("Model Trained")
            # Generate data points
            inputs = np.random.rand(limit, 2)
            # Add OR gate points
            inputs = np.vstack((inputs, [0, 0], [0, 1], [1, 0], [1, 1]))
            l = len(inputs)
            outputs = np.array([test(i) for i in inputs])
            ani.event_source.stop()  # Stop animation
            scatter.set_offsets(inputs)
            return scatter,

        # Train perceptron
        for i in range(l):
            p.train(inputs[i], outputs[i])

        # Update colors based on predictions
        new_colors = np.array(
            ["red" if p.predict(i) == 0 else "blue" for i in inputs])
        scatter.set_facecolors(new_colors)
        return scatter,
    else:
        return scatter,


# Run animation
ani = animation.FuncAnimation(fig, update, frames=range(1), interval=100)
plt.title("Perceptron Training Visualization")
plt.show()
