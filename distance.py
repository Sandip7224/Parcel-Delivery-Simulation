# utils.py

import math

def calculate_distance(p1, p2):
    """
    Calculate Euclidean distance between two points
    p1 and p2 are lists like [x, y]
    """
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)