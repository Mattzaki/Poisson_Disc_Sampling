import bpy
import math
import os
import random


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

def generate_new_samples(r, x_i):
    '''
    function that calculate a new possible sample
    :param r: the minimum distance between the samples
    :param x_i: initial position
    :return: the possible_sample
    '''
    angle = random.random() * math.pi * 2  # calculate a random angle
    possible_sample = Vector2(math.cos(angle), math.sin(angle))  # calculate a random vector with the previous angle
    # as angulation
    possible_sample.normalize()  # normalize the vector to change is length to 1
    new_mag = int(random.uniform(r, 2 * r))  # calculate a random new magnitude for the vector that
    # is between the r (minimum distance) and 2r
    possible_sample = possible_sample.set_magnitude(new_mag)

    # at this point the new vector has a length that is between r and 2r
    possible_sample.x += x_i.x  # add the x's vector with the x of the sample that we are examining
    possible_sample.y += x_i.y  # add the x's vector with the x of the sample that we are examining

    # now the vector has the origin in the x_i position and has the right length
    return possible_sample


def bridson(r, k, width, height):
    '''
    Bridson's Algorithm
    :param r: value of the minimum distance between two samples
    :param k: number of tries before decide to stop the generation of new possible samples
    :param width: width of the game screen used to visualize the spawn of the samples
    :param height: height of the game screen used to visualize the spawn of the samples
    '''

    '''
    STEP 0 of Bridson's paper:
        we pick the cell size to be bounded by r/sqrt(n) where n is the number of the dimensions, in our case n = 2
        now we can initialize the n-dimensional background grid, we will use this for store the sample and accelerate the searches
    '''
    w = r / math.sqrt(2)  # cellsize for the background grid that that ensures that only one sample is present
    rows, cols = math.floor(height / w), math.floor(width / w)  # number of rows and cols
    grid = [-1 for _ in range(cols * rows)]  # initialization of the background grid

    '''
    STEP 1 of Bridson's paper:
        we choose a random initial sample that is between our width and height 's screen
        we store it into our background grid
        and we initialize our active list with the sample's index
    '''
    x = math.floor(random.uniform(0, width))  # pick of a random x for the first sample
    y = math.floor(random.uniform(0, height))  # pick of a random y for the first sample
    i = math.floor(x / w)  # value of the i coordinate used to store the sample into the background grid
    j = math.floor(y / w)  # # value of the j coordinate used to store the sample into the background grid
    pos = Vector2(x, y)  # initialization of the position of the first sample
    grid[i + j * cols] = pos  # store the position coordinate into the background grid
    active = []  # initialization of the active list
    active.append(pos)  # addition of the first sample into the active list

    '''
            STEP 2 of Bridson's paper:
                While the active list is not empty, we choose a random index from it (randomIndex)
            '''
    while len(active) > 0:  # if the active list isn't empty
        randomIndex = math.floor(random.uniform(0, len(active) - 1))  # pick a random index between the
        # length of the active list
        x_i = active[randomIndex]  # store the coordinate of the sample
        found = False  # initialization of a boolean variable used to know if a new sample is found or not

        '''
        we generate up to k points
        '''
        for _ in range(k):  # for k tries
            '''
            we use this function to generate a new point that is chosen randomly from the
            spherical annulus between radius r and 2r around our x_i
            '''
            possible_sample = generate_new_samples(r, x_i)  # generation of a new sample
            '''
            Now we check if it is within r distance from existing samples
            and we use the background grid for testing the neighborhood
            '''
            # possible_sample's position into the grid
            col = math.floor(possible_sample.x / w)  # calculate the value of the column picking the integer value of
            # the possible_sample x divided by the cellsize w
            row = math.floor(possible_sample.y / w)  # calculate the value of the row picking the integer value of
            # the possible_sample x divided by the cellsize w

            '''
            if the point is not out of our range and it don't exist in the background grid
            '''
            if (0 < col < cols - 1) and (0 < row < rows - 1) and (grid[col + row * cols] == -1):
                valid = True  # initialization of a boolean variable used to know if the sample is valid
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        '''
                        We select the possible neighbor from the background grid
                        '''
                        index = (col + i) + (row + j) * cols  # calculate the index of the neighbor
                        neighbor = grid[index]  # pick the neighbor from the background list
                        '''
                        if it exists ( his value in the background grid isn't equal to -1)
                        we calculate the distance between the current point and this neighbor
                        if it is lesser than r, the point isn't valid because it is
                        too near to an existing sample
                        '''
                        if neighbor != -1:  # if there is a sample
                            d = possible_sample.distance_to(neighbor)  # initialization of the distance between
                            # the possible sample and his neighbor
                            if d < r:  # if the distance is lesser than d
                                valid = False  # the possible sample isn't valid
                    '''
                    if the point is valid, we add the point into the grid as a new possible_sample
                    and we store it into the active list as the next possible_sample
                    '''
                if valid:  # if a valid sample was found
                    found = True
                    grid[col + row * cols] = possible_sample  # store the new sample into the background grid
                    active.append(possible_sample)  # add the new sample into the active list
                    break
            '''
            if after k tries we don't find a valid point, we remove it from our active list
            '''
        if not found:  # if didn't find anything
            active.pop(randomIndex)  # remove the possible sample from the active list

    return grid


def generate_points(r, k, width, height):
    grid = bridson(r, k, width, height)  # initialize the grid that contains the samples' coordinates
    bpy.ops.mesh.primitive_plane_add(size=width, align='WORLD', enter_editmode=False,
                                     location=(width / 2, width / 2, 0))  # add the plane where we'll put the spheres

    for i in grid:  # for each sample in the background grid
        if i != -1:  # that exist
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(i.x, i.y, 0.5))  # add the spheres


def export():
    bpy.ops.object.select_all(action='SELECT')  # select all the elements in the scene
    bpy.ops.object.join()  # join all the elements in a single one
    blend_file_path = bpy.data.filepath  # take the path were the file .blend is stored
    directory = os.path.dirname(blend_file_path)  # store the directory of the path
    target_file = os.path.join(directory, 'PoissonDiscSampling.obj')  # add to the directory the name of our file
    bpy.ops.export_scene.obj(filepath=target_file)  # export the file as a .obj


if __name__ == '__main__':
    bpy.ops.object.select_all(action='SELECT')  # select all the elements in the scene
    bpy.ops.object.delete(use_global=False, confirm=False)  # delete all the selected objects
    generate_points(5, 30, 100, 100)  # run the algorithm
    export()  # export the scene
