import numpy as np


class Perceptron:
    def __init__(self, inputsize=2, b=0, weights=None, learnRate=0.5):
        if (weights == None):
            self.w = np.random.rand(inputsize+1)
            self.w[-1] = b
        else:
            if (len(weights) != inputsize):
                raise Exception("len(weights) != inputsize")
            self.w = np.append(weights, b)
        self.learnRate = learnRate

    def predict(self, inputs):
        inputs = np.append(inputs, 1)
        inputs = np.array(inputs)
        x = np.transpose(inputs)
        result = Perceptron.activationFunction(np.dot(self.w, x))
        # print(f"Inputs: {inputs} =>Result: {result}")
        return result

    def train(self, x, y):
        expected = y
        predicted = self.predict(x)
        error = expected - predicted
        print(f"Expected: {expected} Predicted: {predicted} Error: {error}")
        avgWeight = np.average(self.w)
        if (avgWeight == 0):
            avgWeight = 1
        # print(f"Average Weight: {avgWeight}")
        fixes = [float(error * (w / avgWeight)) for w in self.w]
        # print(f"Fixes: {fixes}")
        self.fix(np.multiply(fixes, self.learnRate))

    def fix(self, fixes):
        # print(f"old: {self.w} new: {np.add(self.w, fixes)}")
        self.w = np.add(self.w, fixes)

    @staticmethod
    def activationFunction(input: float | int):
        return 1 if input >= 1 else 0
