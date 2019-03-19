import csv

#bharat kumar

def parser_csv(filename):
    data = []
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            data.append(row)

    return data

def get_curve(data_points, degree):
    n = degree

    matrix = [[0 for i in range(0, n + 1)] for  j in range(0, n + 1)]

    coefficients = []

    range_n = 2 * n

    i = len(data_points)

    for k in range(0, range_n):
        sum = 0
        for l in range(0, i):
            sum += pow(data_points[l][0], range_n - k)
        coefficients.append(sum)

    for i in range(0, n):
        for j in range(0, n):
            matrix[i][j] = coefficients[i + j]

    values = []

    for i in range(0, n):
        values.append(matrix[i][n - 1])

    return get_solution_vector(matrix, values)

#[x[0], x[1], ... , x[n]]
def get_solution_vector(matrix, values):
    n = len(matrix)

    new_matrix = matrix
    new_values = values
    #gaussian elimination

    pivot = 0;

    for i in range(0, n):
        for j in range(0, n):
            if i != j and new_matrix[i][i] != 0:
                ratio = (-1.0 * new_matrix[j][i])/new_matrix[i][i]
                for k in range(0, n):
                    value =  (ratio * new_matrix[i][k]) + new_matrix[j][k]
                    new_matrix[j][k] = value

                value = (ratio * new_values[i]) + new_values[j]
                new_values[j] = value

    coefficients = [0 for i in range(0, n)]

    for i in range(0, n):
        coefficients[i] = new_values[i] / new_matrix[i][i]

    return coefficients

def f(x, model):
    n = len(model)
    x_powered = [0 for i in range(0, n)]

    x_powered[0] = 1

    for i in range(1, n):
        x_powered[i] = x * x_powered[i - 1]


    value = 0

    for i in range(0, n):
        v = model[i] * x_powered
        value += v

    return value

def sort_key(val):
    return val[1]

def get_curves(points):
    n = len(points)
    degree = n - 1
    model = get_curve(points, degree)

    error = [(0, 0) for i in range(0, n)]

    for i in range(0, n):
        x = points[i][0]
        y = points[i][1]
        estimate = f(x, model)
        e = estimate - y
        if e < 0:
            e = -1 * e
        e = e / estimate
        error[i] = (i, e)

    sorted_error = error
    sorted_error.sort(key = sort_key)

    p = int((n + 1) / 2)
    median = error[p]

    split = [False for i in range(0, n)]

    for i in range(0, p):
        split[sorted_error[0]] = True
