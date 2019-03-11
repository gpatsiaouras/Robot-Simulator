import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class ANN:
    def __init__(self, input_neurons=12, weights1=None, weights2=None, hidden_neurons=5, output_neurons=2):
        self.input_vector = input_neurons
        # initialize previous activations to zero, so that at first initialization of the network it just concatenetes zeros
        self.prev_activation = np.zeros((1, hidden_neurons))
        self.weights1 = weights1
        self.weights2 = weights2
        self.output_vector = np.random.rand(2, 1)

    def feed_forward(self, input):

        # in first step take as input sensors values + (that stands for concatenates being vectors) + activations of previous iteration
        middle_layer = sigmoid(np.matmul(np.append(input.T, self.prev_activation.T), self.weights1))
        # after computing new activations store them for next iterations
        self.prev_activation = middle_layer
        self.output_vector = sigmoid(np.dot(middle_layer, self.weights2))

    # TODO: This get_ouput could easily be a return in the feedforward method
    def get_output(self):
        return self.output_vector


if __name__ == '__main__':
    # Generate random input vector simulating our sensors
    input_vector = np.random.rand(12)

    # Generate random weights for layer 1-2 and 2-3
    weights1 = np.random.rand(17, 5)
    weights2 = np.random.rand(5, 2)

    # Initiate Neural Network
    ann = ANN( weights1=weights1, weights2=weights2)
    ann.feed_forward(input_vector)

    print(ann.get_output())
