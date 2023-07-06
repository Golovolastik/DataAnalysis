import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
import random

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
         
def choose_distance(size1, size2, intersection=True):
    if intersection:
        return size1 + size2*0.8
    else:
        return size1 + size2 + 0.15
    

def find_circle_intersection_center(x1, y1, r1, x2, y2, r2):
    # Вычисляем расстояние между центрами окружностей
    d = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    # Проверяем случаи, когда окружности не пересекаются или совпадают
    if d > r1 + r2 or d < abs(r1 - r2):
        return None
    
    # Вычисляем разность радиусов
    r_diff = abs(r1 - r2)
    r_diff = r1 - r2

    
    # Вычисляем отношение
    a = r_diff / d
    a = r_diff / 2
    # Вычисляем координаты центра пересечения
    x_intersect = x1 + (d**2 - r2**2 + r1**2)/(2*d)
    #y_intersect = y1 + a * (y2 - y1)
    y_intersect = y1
    
    return x_intersect, y_intersect

def choose_venn(number, ax, set_list, dict):
        function_dictionary = {
            2: venn2,
            3: venn3,
            4: venn4
        }
        if number in function_dictionary:
            selected_func = function_dictionary[number]
            selected_func(ax, set_list, dict)

# def place_dots(ax, set, center_x, center_y, radius, intersection=False):
#     if intersection:
#         number = 3
#     else:
#         number_of_dots = {
#             0.5: 8,
#             0.35: 6,
#             0.25: 4,
#             0.15: 3
#         }
#         number = number_of_dots.get(radius)
#     if len(set) < number:
#         number = len(set)
#     random_set = random.sample(set, number)
#     point_value_dict = {}
#     for point in random_set:
#         dist = random.random() * radius
#         theta = random.random() * 2 * np.pi
#         x = center_x + dist * np.cos(theta) 
#         y = center_y + dist * np.sin(theta)
#         dot = ax.plot(x, y, 'ro')[0]
#         dot.set_picker(5)  # Радиус "зоны попадания" для нажатия
#         dot.set_pickradius(5)  # Радиус точки
#         point_value_dict[dot] = point
    
#     return point_value_dict

def venn2(ax, set_list, dict=[1,2]):
    if len(set_list) != 2:
        return
    temp_dict = list(dict)
    # Intersection True
    size_list = size_of_circle(set_list)
    big_x, big_y = 0.5, 1
    if set_list[0] & set_list[1]:
        circle0 = plt.Circle((big_x, big_y), size_list[0], color='blue', alpha=0.5)
        #place_dots(ax, set_list[0], big_x, big_y, size_list[0])
        ax.add_artist(circle0)
        ax.text(big_x, big_y, temp_dict[0], ha='center')
        x_adder = choose_distance(size_list[0], size_list[1])
        circle1 = plt.Circle((big_x + x_adder, big_y), size_list[1], color='yellow', alpha=0.5)
        #place_dots(ax, set_list[1], big_x + x_adder, big_y, size_list[1])
        ax.add_artist(circle1)
        ax.text(big_x + x_adder, big_y, temp_dict[1], ha='center')
        intersection = set_list[0].intersection(set_list[1])
        intersection = [str(x) for x in intersection]
        text = '\n'.join(intersection)
        intersection_center = find_circle_intersection_center(big_x, big_y, size_list[0], big_x + x_adder, big_y, size_list[1])
        #ax.text(intersection_center[0], intersection_center[1], text, ha='center')
    else:
        circle0 = plt.Circle((big_x, big_y), size_list[0], color='blue', alpha=0.5)
        #place_dots(ax, set_list[0], big_x, big_y, size_list[0])
        ax.add_artist(circle0)
        ax.text(big_x, big_y, temp_dict[0], ha='center')
        adder = choose_distance(size_list[0], size_list[1], intersection=False)
        circle1 = plt.Circle((big_x + adder, big_y), size_list[1], color='yellow', alpha=0.5)
        #place_dots(ax, set_list[1], big_x + x_adder, big_y, size_list[1])
        ax.add_artist(circle1)
        ax.text(big_x + adder, big_y, temp_dict[1], ha='center')

def venn3(ax, set_list, dict=[1,2,3]):
    if len(set_list) != 3:
        return
    temp_dict = list(dict)
    size_list = size_of_circle(set_list)
    center0 = (0, 0)
    x_adder = choose_distance(size_list[0], size_list[1])
    if set_list[0] & set_list[1] & set_list[2]:
        print(f"Condition: set_list[0] & set_list[1] & set_list[2]")
        # Координаты центров окружностей
        circle0 = plt.Circle((center0), size_list[0], color='yellow', alpha=0.5)
        #place_dots(ax, set_list[1], 0, 0, size_list[1])
        ax.text(0, 0, temp_dict[0], ha='center')
        ax.add_artist(circle0)
        center1 = (size_list[0] + size_list[1]*0.6, 0)
        xy2 = find_circle_intersection_center(0, 0, size_list[0], size_list[0] + size_list[1]*0.6, 0, size_list[1])
        center2 = (xy2[0], xy2[1] + size_list[1] * np.sqrt(2))
        circle1 = plt.Circle(center1, size_list[1], color='blue', alpha=0.5)
        #place_dots(ax, set_list[1], size_list[0] + size_list[1]*0.6, 0, size_list[1])
        ax.text(size_list[0] + size_list[1]*0.6, 0, temp_dict[1], ha='center')
        ax.add_artist(circle1)
        circle2 = plt.Circle(center2, size_list[1], color='red', alpha=0.5)
        #place_dots(ax, set_list[2], xy2[0], xy2[1] + size_list[1] * np.sqrt(2), size_list[2])
        ax.text(xy2[0], xy2[1] + size_list[1] * np.sqrt(2), temp_dict[2], ha='center')
        ax.add_artist(circle2)
        ax.set_xlim(-0.8, 1.5)
        ax.set_ylim(-0.8, 1.15)
        return
    if set_list[0] & set_list[1] or set_list[0] & set_list[2] or set_list[1] & set_list[2]:
        condition_0_1 = set_list[0] & set_list[1]
        condition_0_2 = set_list[0] & set_list[2]
        condition_1_2 = set_list[1] & set_list[2]
        if condition_0_1:
            print(f"Condition: condition_0_1")
            venn2_list = [temp_dict[0], temp_dict[1]]
            venn2(ax, [set_list[0], set_list[1]], venn2_list)
            if condition_0_2:
                print(f"Condition: condition_0_2")
                circle2 = plt.Circle((0.35, 1+size_list[0]+size_list[2]*0.4), size_list[2], color='red', alpha=0.5)
                #place_dots(ax, set_list[0], 0.35, 1+size_list[0]+size_list[2]*0.4, size_list[0])
                ax.text(0.35, 1+size_list[0]+size_list[2]*0.8, temp_dict[2], ha='center')
            elif condition_1_2:
                print(f"Condition: condition_1_2")
                x_adder = choose_distance(size_list[0], size_list[1])
                circle2 = plt.Circle((0.35+x_adder, 1+size_list[0]+size_list[2]*0.8), size_list[2], color='red', alpha=0.5)
                #place_dots(ax, set_list[2], 0.35+x_adder, 1+size_list[0]+size_list[2]*0.8, size_list[2])
                ax.text(0.35+x_adder, 1+size_list[0]+size_list[2]*0.8, temp_dict[2], ha='center')
            else:
                circle2 = plt.Circle((0.35, 1+size_list[0]+size_list[2]+0.15), size_list[2], color='red', alpha=0.5)
                #place_dots(ax, set_list[2], 0.35, 1+size_list[0]+size_list[2]+0.15, size_list[2])
                ax.text(0.35, 1+size_list[0]+size_list[2]+0.15, temp_dict[2], ha='center')
            ax.add_artist(circle2)
            ax.set_xlim(-0.3, 2.1)
            ax.set_ylim(0.25, 2.2)
        elif condition_0_2:
            print(f"Condition: condition_0_2")
            venn2_list = [temp_dict[0], temp_dict[2]]
            venn2(ax, [set_list[0], set_list[2]], venn2_list)
            if condition_0_1:
                print(f"Condition: condition_0_1")
                circle2 = plt.Circle((0.35, 1+size_list[0]+size_list[1]*0.8), size_list[1], color='red', alpha=0.5)
                #place_dots(ax, set_list[1], 0.35, 1+size_list[0]+size_list[1]*0.8, size_list[1])
                ax.text(0.35, 1+size_list[0]+size_list[1]*0.8, temp_dict[1], ha='center')
            elif condition_1_2:
                print(f"Condition: condition_1_2")
                x_adder = choose_distance(size_list[0], size_list[2])
                circle2 = plt.Circle((0.75+size_list[0]+size_list[2], 1+size_list[2]+size_list[1]*0.8), size_list[1], color='red', alpha=0.5)
                #place_dots(ax, set_list[1], 0.75+size_list[0]+size_list[2], 1+size_list[2]+size_list[1]*0.8, size_list[1])
                ax.text(0.75+size_list[0]+size_list[2], 1+size_list[2]+size_list[1]*0.8, temp_dict[1], ha='center')
            else:
                circle2 = circle2 = plt.Circle((0.5, 1+size_list[0]+size_list[1]+0.15), size_list[1], color='red', alpha=0.5)
                #place_dots(ax, set_list[1], 0.5, 1+size_list[0]+size_list[1]+0.15, size_list[1])
                ax.text(0.5, 1+size_list[0]+size_list[1]+0.15, temp_dict[1], ha='center')
            ax.add_artist(circle2)
        elif condition_1_2:
            print(f"Condition: condition_1_2")
            venn2_list = [temp_dict[1], temp_dict[2]]
            venn2(ax, [set_list[1], set_list[2]], venn2_list)
            if condition_0_1:
                print(f"Condition: condition_0_1")
                circle2 = plt.Circle((0.35, 1+size_list[0]+size_list[1]*0.8), size_list[2], color='red', alpha=0.5)
                #place_dots(ax, set_list[2], 0.35, 1+size_list[0]+size_list[1]*0.8, size_list[2])
                ax.text(0.35, 1+size_list[0]+size_list[1]*0.8, temp_dict[0], ha='center')
            elif condition_0_2:
                print(f"Condition: condition_0_2")
                x_adder = choose_distance(size_list[1], size_list[2])
                circle2 = plt.Circle((0.35+x_adder, 1+size_list[0]+size_list[2]*0.8), size_list[2], color='red', alpha=0.5)
                #place_dots(ax, set_list[2], 0.35+x_adder, 1+size_list[0]+size_list[2]*0.8, size_list[2])
                ax.text(0.35+x_adder, 1+size_list[0]+size_list[2]*0.8, temp_dict[0], ha='center')
            else:
                circle2 = circle2 = plt.Circle((0.5, 1+size_list[1]+size_list[0]+0.15), size_list[0], color='red', alpha=0.5)
                #place_dots(ax, set_list[0], 0.5, 1+size_list[1]+size_list[0]+0.15, size_list[0])
                ax.text(0.5, 1+size_list[1]+size_list[0]+0.15, temp_dict[0], ha='center')
            ax.add_artist(circle2)
            ax.set_xlim(-0.7, 2)
            ax.set_ylim(-0.7, 1.6)
        return
    print(f"Condition: no intersections")
    circle0 = plt.Circle((center0), size_list[0], color='yellow', alpha=0.5)
    #place_dots(ax, set_list[0], 0, 0, size_list[0])
    ax.text(center0[0], center0[1], temp_dict[0], ha='center')
    ax.add_artist(circle0)
    center1 = (size_list[0] + size_list[1]+0.2, center0[1])
    center2 = ((center0[0] + center1[0])/2, center1[1] + size_list[2] + max(size_list[0], size_list[1])+0.15)
    circle1 = plt.Circle(center1, size_list[1], color='blue', alpha=0.5)
    #place_dots(ax, set_list[1], size_list[0] + size_list[1]+0.2, center0[1], size_list[1])
    ax.text(center1[0], center1[1], temp_dict[1], ha='center')
    ax.add_artist(circle1)
    circle2 = plt.Circle(center2, size_list[2], color='red', alpha=0.5)
    #place_dots(ax, set_list[2], (center0[0] + center1[0])/2, center1[1] + size_list[2] + max(size_list[0], size_list[1])+0.15, size_list[2])
    ax.text(center2[0], center2[1], temp_dict[2], ha='center')
    ax.add_artist(circle2)
    ax.set_xlim(-0.7, 2)
    ax.set_ylim(-0.7, 1.6)

    return

def venn4(ax, set_list, dict=[1,2,3,4]):
    # if len(set_list) != 3:
    #     return
    temp_dict = list(dict)
    size_list = size_of_circle(set_list)
    r = 0.5
    center0 = (0,0)
    center1 = (r/2, r*0.8)
    center2 = (r, 0)
    center3 = (r/2, 0-r*0.8)

    circle0 = plt.Circle(center0, r, color='blue', alpha=0.5)
    circle1 = plt.Circle(center1, r, color='red', alpha=0.5)
    circle2 = plt.Circle(center2, r, color='yellow', alpha=0.5)
    circle3 = plt.Circle(center3, r, color='green', alpha=0.5)

    ax.add_artist(circle0)
    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.add_artist(circle3)