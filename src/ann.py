import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class ANN:
    def __init__(self, input_vector, weights1, weights2):
        self.input_vector = input_vector
        self.weights1 = weights1
        self.weights2 = weights2
        self.output_vector = np.random.rand(2, 1)

    def feed_forward(self):
        middle_layer = sigmoid(np.dot(self.input_vector.T, self.weights1))
        self.output_vector = sigmoid(np.dot(middle_layer, self.weights2))

    def get_output(self):
        return self.output_vector


if __name__ == '__main__':
    # Generate random input vector simulating our sensors
    input_vector = np.random.rand(12, 1)

    # Generate random weights for layer 1-2 and 2-3
    weights1 = np.random.rand(input_vector.shape[0], 5)
    weights2 = np.random.rand(5, 2)

    # Initiate Neural Network
    ann = ANN(input_vector=input_vector, weights1=weights1, weights2=weights2)
    ann.feed_forward()

    print(ann.get_output())
