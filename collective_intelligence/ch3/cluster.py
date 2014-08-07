# coding=utf-8


class Bicluster(object):
    """
    Bicluster represents a link between two objets, forming a cluster
    :param vec: vector of values to calculate distance between the 2 clusters
    :param left:
    :param right:
    :param distance:
    :param id:
    """

    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance


