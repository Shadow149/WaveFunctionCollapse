import math
import numpy as np

class Square():
    def __init__(self, tile_types, observed_state = None):
        self.possible_tile_types = tile_types
        self.observed = False
        self.observed_state = observed_state
        self.propogate_visited = False

    def calculate_available_weights(self, weights: dict):
        self.weights_of_allowed_tile_type = []

        for tile_type in self.possible_tile_types:
            tile_type_weights = weights[tile_type]
            self.weights_of_allowed_tile_type += [tile_type_weights]
        return np.array(self.weights_of_allowed_tile_type)

    def calculate_entropy(self, weights: dict):
        weights = self.calculate_available_weights(weights)

        if len(weights) == 0:
            return 0
        
        shannon_entropy = np.log(sum(weights)) - (sum(weights * np.log(weights)) / sum(weights))
        #print(shannon_entropy)
        return shannon_entropy

    def collapse(self, weights: dict):
        weights = self.calculate_available_weights(weights)

        weights = np.array(weights)
        weights = weights / sum(weights)

        #print('asas',self.possible_tile_types,weights)

        if len(self.possible_tile_types) == 0:
            return self.observed_state

        collapsed_state = np.random.choice(self.possible_tile_types, p=weights)
        return collapsed_state

    def __repr__(self):
        if not self.observed:
            return '?'
        return self.observed_state


# Sums are over the weights of each remaining
# allowed tile type for the square whose
# entropy we are calculating.
#shannon_entropy_for_square = log(sum(weight)) - (sum(weight * log(weight)) / sum(weight))

# EXAMPLE
if __name__ == '__main__':
    weights = {'S': 4, 'C': 3, 'L': 2}
    tile_types = ['S','C','L']
    s1 = Square(tile_types)
    s1.calculate_entropy(weights)
    s1.collapse(weights)