from Game import Game
from NN import NeuralNetwork

def main():
    # game = Game()
    # game.run()
    n = NeuralNetwork.Network("FeedForward", 3, 4)
    n.addLayer(3)
    stop=1


if __name__ == "__main__":
    main()
