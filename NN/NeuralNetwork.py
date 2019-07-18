import numpy as np

class Network:
    '''
    Simple Neural Network class
    '''
    def __init__(self, name, input, hidden):
        self.name = name
        self.weights = {0:np.random.uniform(0,1, (input, hidden))}


    def addLayer(self, neurons):
        '''
        Adds Layer to the network
        :param int neurons:
        '''
        layer = np.random.uniform(0,1, (self.weights[0].shape[1], neurons))
        self.weights[len(self.weights)] = layer
        self.weights = np.concatenate((self.weights,layer), axis=0)


    def feedForward(self, input):
        '''
        Passed input through the network
        :param input:
        '''
        pass


    def train(self, input, output, iterations):
        '''
        Trains the network for a choosen amount of iterations
        :param input: input data
        :param output: hypotheses is compared with output data
        :param iterations: iteration count
        '''
        pass
