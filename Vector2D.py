import math


class Vector2:
    '''
    class used for store the coordinates as a vector
    '''

    '''
    initialization of the vector
    '''

    def __init__(self, x, y):
        self.x, self.y = x, y

    '''
    function used to normalize the vector
    '''

    def normalize(self):
        magnitude = math.sqrt(self.x * self.x + self.y * self.y)
        self.x = self.x / magnitude
        self.y = self.y / magnitude

    '''
    function used to change the magnitude of the vector
    '''

    def set_magnitude(self, new_magnitude):
        self.normalize()
        x = self.x * new_magnitude
        y = self.y * new_magnitude

        return Vector2(x, y)

    '''
    function used to calculate the euclidean distance from 2 vectors
    '''

    def distance_to(self, b):
        return math.sqrt((self.x - b.x) ** 2 + (self.y - b.y) ** 2)
