import csv
import numpy

def get_curve(data_points, degree):
    x_data = []
    y_data = []

    for i in range(0, len(data_points)):
        x_data.append(data_points[i][0])
        y_data.append(data_points[i][1])

    equation = numpy.polyfit(x_data, y_data, degree, None, False, None, False)

    return equation

def get_average_error(model, data_points):
    n = len(data_points)
    error = 0
    for i in range(0, n):
        e_percentage = (data_points[i][1] - f(data_points[i][0], model)) / (1.0 * data_points[i][1])
        error += (e_percentage * e_percentage)

    avg = (1.0 * error) / n

    return avg

def boolean_function(error, tolerance):
    if error > tolerance:
        return 1
    elif error < tolerance:
        return -1

    return 0

def get_curves(data_points, tolerance):
    upper_bound = len(data_points) - 1
    lower_bound = 0
    while upper_bound > lower_bound + 1:
        mid = (upper_bound + lower_bound) / 2
        degree = mid
        model = get_curve(data_points, degree)
        error = get_average_error(model, data_points)

        c = boolean_function(error, tolerance)

        if c == 0:
            return model
        elif c > 0:
            lower_bound = mid
        elif c < 0:
            upper_bound = mid

    return model


def f(x, model):
    n = len(model)
    x_powered = [0 for i in range(0, n)]

    x_powered[0] = 1

    for i in range(1, n):
        x_powered[i] = x * x_powered[i - 1]

    value = 0

    for i in range(0, n):
        v = model[i] * x_powered[n - 1 - i]
        value += v

    return value

def convert_model_to_string(model):
    model_string = "y = "

    n = len(model)

    model_string += str(model[0]) + "(x^" + str(n - 1) + ")"
    for i in range(1, n):
        if i < n - 2:
            if model[i] < 0:
                model_string += " - " + str((-1 * model[i])) + "(x^" + str(n - i - 1) + ")"
            else:
                model_string += " + " + str(model[i]) + "(x^" + str(n - i - 1) + ")"
        else:
            if i == n - 2:
                if model[i] < 0:
                    model_string += " - " + str((-1 * model[i])) + "x"
                else:
                    model_string += " + " + str(model[i]) + "x"
            else:
                if model[i] < 0:
                    model_string += " - " + str((-1 * model[n - 1]))
                else:
                    model_string += " + " + str(model[i])
    return model_string

def test():
    data_points = [(1, 1.25), (2, 0.94), (3, 0.65), (4, 0.62), (5, 0.87), (6, 0.94), (7, 1.14), (8, 1.72), (9, 1.83), (10, 2.12), (11, 1.91), (12, 1.80), (13, 2.25), (14, 2.08), (15, 1.73)]
    #

    print("DATA POINTS")
    print(data_points)
    print("\n")

    model = get_curves(data_points, 0.005)

    model_string = convert_model_to_string(model)

    print("MODEL (equation form)")
    print(model_string)

    print("\n")
    print("EXAMPLES")

    print("x = ?")
    x = int(input())

    y = f(x, model)
    print((x, y))

test()
