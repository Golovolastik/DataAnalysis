import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

def find_center(ax):
    x_y_coordinates = []
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()

    # Вычисление центра графика
    x_center = (x_min + x_max) / 2
    x_y_coordinates.append(x_center)
    y_center = (y_min + y_max) / 2
    x_y_coordinates.append(y_center)
    return x_y_coordinates    

def size_of_circle(set_list):
    lengths = [len(s) for s in set_list]
    max_length = max(lengths)
    coefficients = []

    for length in lengths:
        if length == max_length:
            coefficients.append(0.5)
        else:
            factor = length / max_length
            if factor >= 0.8:
                coefficients.append(0.5)
            elif factor >= 0.6:
                coefficients.append(0.35)
            elif factor >= 0.4:
                coefficients.append(0.25)
            else:
                coefficients.append(0.15)

    return coefficients
         
def choose_distance(size_list, intersection=True):
    if intersection:
        return size_list[0] + size_list[1]*0.2
    else:
        return size_list[0] + size_list[1] + 0.15

def venn2(ax, set_list):
    if len(set_list) != 2:
        return
    # Intersection True
    size_list = size_of_circle(set_list)
    big_x, big_y = 0.5, 1
    if set_list[0] & set_list[1]:
        circle0 = plt.Circle((big_x, big_y), size_list[0], color='blue', alpha=0.5)
        ax.add_artist(circle0)
        x_adder = choose_distance(size_list)
        circle1 = plt.Circle((big_x + x_adder, big_y), size_list[1], color='yellow', alpha=0.5)
        ax.add_artist(circle1)
        intersection = set_list[0].intersection(set_list[1])
        #print(intersection)
        intersection = [str(x) for x in intersection]
        text = '\n'.join(intersection)
        d = sqrt((big_x + x_adder - big_x)**2 + (big_y - big_y)**2)
        x = (size_list[0]**2 - size_list[1]**2 + d**2) / (2 * d)
        ax.text(big_x+x, big_y, text)
    else:
        circle0 = plt.Circle((big_x, big_y), size_list[0], color='blue', alpha=0.5)
        ax.add_artist(circle0)
        circle1 = plt.Circle((big_x + choose_distance(size_list, intersection=False), big_y), size_list[1], color='yellow', alpha=0.5)
        ax.add_artist(circle1)

def venn3(ax, set_list):
    if len(set_list) != 3:
        return
    size_list = size_of_circle(set_list)
    big_x, big_y = 0.7, 0.7
    