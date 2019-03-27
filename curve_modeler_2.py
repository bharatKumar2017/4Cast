import csv
import numpy
import math

def parser_csv(filename):
    data = []
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            data.append(row)

    return data

def get_points(data, row):
    n = len(data[row])

    points = []
    for i in range(0, n):
        x = data[i][i]
        y = data[row][j]
        tuple = (float(x), float(y))
        points.append(tuple)

    return points

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
        if e_percentage < 0:
            e_percentage = -1 * e_percentage
        error += e_percentage

    avg = (1.0 * error) / n

    value = math.sqrt(avg)

    return avg

def get_error(x, model, data_points):
    n = len(data_points)
    y = 0
    for i in range(0, n):
        if x == data_points[i][0]:
            y = data_points[i][1]

    y_expected = f(x, model)

    error = (y_expected - y) / (1.0 * y)

    if error < 0:
        error = -1 * error

    return error

def boolean_function(error, tolerance):
    if error > tolerance:
        return 1
    elif error < tolerance:
        return -1

    return 0

def get_curves(data_points, tolerance):
    upper_bound = len(data_points) - 1
    lower_bound = 1

    model = []

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

    if model == None:
        model = get_curve(data_points, len(data_points) - 1)
        return model

    if len(model) == 0:
        model = get_curve(data_points, len(data_points) - 1)
        return model

    return model

def get_max_error(model, data_points):
    n = len(data_points)
    max_error = 0
    for i in range(0, n):
        e_percentage = (data_points[i][1] - f(data_points[i][0], model)) / (1.0 * data_points[i][1])
        error = e_percentage
        if error < 0:
            error = -1 * error

        if max_error < error:
            max_error = error

    return max_error

def get_curves_max(data_points, tolerance):
    upper_bound = len(data_points) - 1
    lower_bound = 0
    while upper_bound > lower_bound + 1:
        mid = (upper_bound + lower_bound) / 2
        degree = mid
        model = get_curve(data_points, degree)
        error = get_max_error(model, data_points)

        c = boolean_function(error, tolerance)

        if c == 0:
            return model
        elif c > 0:
            lower_bound = mid
        elif c < 0:
            upper_bound = mid

def f(x, model):
    n = len(model)
    x_powered = [0 for i in range(0, n)]

    x_powered[0] = 1.0

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

def test_model(model, data_points):
    model_points = []
    n = len(data_points)
    for i in range(0, n):
        x = data_points[i][0]
        y = f(x, model)
        tuple = (x, y)
        model_points.append(tuple)

    return model_points

def get_all_points_interval(data_points, intervals):
    points = []

    for i in range(0, len(data_points)):
        point = data_points[i]
        if point[0] >= intervals[0] and point[0] <= intervals[1]:
            points.append(point)

    return points

def split_function(data_points, tolerance):
    n = len(data_points)
    model = get_curves(data_points, tolerance)

    split = [False for i in range(0, n)]

    for i in range(0, n):
        y_expected = 1.0 * f(data_points[i][0], model)
        error = (y_expected - data_points[i][1]) / (data_points[i][1])
        if error > tolerance:
            split[i] = True

    points = []
    models = []

    points.append(data_points[0])

    intervals = []

    for i in range(1, n):
        if split[i] == split[i - 1]:
            points.append(data_points[i])
        elif split[i] != split[i - 1]:
            if len(points) == 1:
                points.append(data_points[i])

            tuple = (points[0][0], data_points[i][0])
            intervals.append(tuple)
            points = []
            points.append(data_points[i])


    if len(points) > 0:
        tuple = (points[0][0], data_points[n - 1][0])
        intervals.append(tuple)

    models = []

    v = len(intervals)

    for i in range(0, v):
        points = get_all_points_interval(data_points, intervals[i])
        model = get_curves(points, tolerance)
        print("POINTS at position " + str(i))
        print(points)
        print("MODEL at position " + str(i))
        print(model)
        models.append(model)

    models_and_intervals = (models, intervals)
    return models_and_intervals

def f_split(x, function):
    models = function[0]
    intervals = function[1]

    n = len(intervals)

    index = 0

    for i in range(0, n):
        if x >= intervals[i][0] and x <= intervals[i][1]:
             index = i
             break

    model = models[index]

    value = f(x, model)

    return value

def test_model_split(model, data_points):
    model_points = []
    n = len(data_points)
    for i in range(0, n):
        x = data_points[i][0]
        y = f_split(x, model)
        tuple = (x, y)
        model_points.append(tuple)

    return model_points

def test1():
    #data = parser_csv("Lite_MC_Attrition.csv")
    #data_points = get_points(data, 1)

    data_points = [(1, 1.25), (2, 0.94), (3, 0.65), (4, 0.62), (5, 0.87), (6, 0.94), (7, 1.14), (8, 1.72), (9, 1.83), (10, 2.12), (11, 1.91), (12, 1.80), (13, 2.25), (14, 2.08), (15, 1.73)]

    print("DATA POINTS")
    print(data_points)
    print("\n")

    print("TOlERANCE = ?")

    tolerance = float(raw_input())

    model = get_curves(data_points, (tolerance / 100))

    print("Average Error = " + str(tolerance) + "%\n")

    model_string = convert_model_to_string(model)

    print("MODEL (equation form)")
    print(model_string)

    print("\n")
    print("EXAMPLES")

    test_data = test_model(model, data_points)

    print(test_data)

    while True:
        print("x = ?")
        string = raw_input()
        if string == 'quit':
            return 0
        x = float(string)
        y = f(x, model)
        print((x, y))
        print("\n")

def test2():
    data_points = [(1, 1.25), (2, 0.94), (3, 0.65), (4, 0.62), (5, 0.87), (6, 0.94), (7, 1.14), (8, 1.72), (9, 1.83), (10, 2.12), (11, 1.91), (12, 1.80), (13, 2.25), (14, 2.08), (15, 1.73)]

    print("DATA POINTS")
    print(data_points)
    print("\n")

    print("TOlERANCE = ?")

    tolerance = float(raw_input())

    model = split_function(data_points, (tolerance / 100))

    print("Average Error = " + str(tolerance) + "%\n")

    #model_string = convert_model_to_string(model)

    #print("MODEL (equation form)")
    #print(model_string)

    print("\n")
    print("EXAMPLES")

    test_data = test_model_split(model, data_points)

    print(test_data)

    while True:
        print("x = ?")
        string = raw_input()
        if string == 'quit':
            return 0
        x = float(string)
        y = f_split(x, model)
        print((x, y))
        print("\n")

test2()
