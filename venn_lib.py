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

def choose_size(factor):
    if factor < 0.25:
        return 0.15
    elif factor < 0.5:
        return 0.25
    elif factor < 0.75:
        return 0.35
    else:
        return 0.5

def size_of_circle(set_list):
    """
    Всего 4 варианта размеров:
    r1 = 0.5
    r2 = 0.35
    r3 = 0.25
    r4 = 0.15
    если разница в количестве значений больше 25% то радиус становится меньше на один шаг
    """
    r1 = 0.5
    r2 = 0.35
    r3 = 0.25
    r4 = 0.15
    size_list = []
    if len(set_list) <= 1:
        return
    max_idx = 0
    for i, set in enumerate(set_list):
        if set:
            if len(set) > len(set_list[max_idx]):
                max_idx = i
    if len(set_list) == 2:
        size_list = [ r4, r4]
        factor = len(set_list[0]) / len(set_list[1])
        if factor > 1:
            size_list[0] = r1
            factor = 1 / factor
            size_list[1] = choose_size(factor)
        else:
            size_list[1] = r1
            size_list[0] = choose_size(factor)
        return size_list
         
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
    