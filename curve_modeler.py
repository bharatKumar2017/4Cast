import csv

def parser_csv(filename):
    data = []
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            data.append(row)

    return data

def get_curve(data_points):
    n = len(data_points) - 1

    matrix = [[0 for i in range(0, n + 1)] for  j in range(0, n + 1)]

    coefficients = []

    range_n = (2 * n) + 1

    i = n + 1

    for k in range(0, range_n):
        sum = 0
        for l in range(0, i):
            sum += pow(data_points[l][0], range_n - k)
        coefficients.append(sum)

    i = 0
    for i in range(0, n):
        for j in range(0, n):
            matrix[i][j] = coefficients[i + j]

    values = []

    for i in range(0, n + 1):
        values.append(matrix[i][n - 1])

    return get_solution_vector(matrix, values)

def update_row(matrix, row_index, ratio, pivot_row_index, n):
    row = []
    for i in range(0, n):
        v = (ratio * matrix[pivot_row_index][i]) + matrix[row_index][i]
        row.append(v)

    return row

def update_all_rows(matrix, pivot_row_index, pivot_position, n):
    new_matrix = matrix
    for i in range(0, n):
        if i != pivot_row_index:
            ratio = get_ratio(new_matrix, i, pivot_row_index, pivot_position, n)
            row = update_row(new_matrix, i, ratio, pivot_row_index, n)
            new_matrix[i] = row

    return new_matrix

def update_all_values(values, matrix, pivot_row_index, pivot_position, n):
    new_values = values
    for i in range(0, n):
        if i != pivot_row_index:
            ratio = get_ratio(matrix, i, pivot_row_index, pivot_position, n)
            value = (ratio * values[pivot_row_index]) + values[i]
            new_values[i] = value

    return new_values

def get_pivot_position(matrix, pivot_row_index, n):
    pivot_value = matrix[pivot_row_index][0]
    index = 0
    while pivot_value == 0 and index < n:
        index = index + 1

        if index < n:
            pivot_value = matrix[pivot_row_index][index]

    return index

def get_ratio(matrix, row_index, pivot_row_index, pivot_row_position, n):
    ratio = (-1.0 * matrix[row_index][pivot_row_position]) / matrix[pivot_row_index][pivot_row_position]
    return ratio

#[x[0], x[1], ... , x[n]]
def get_solution_vector(matrix, values):
    n = len(matrix)

    x = len(values)

    print(n)


    new_matrix = [[0 for i in range(0, n)] for j in range(0, n)]
    new_values = [0 for i in range(0, n)]

    for i in range(0, n):
        for j in range(0, n):
            new_matrix[i][j] = matrix[i][j]
        new_values[i] = values[i]

    for i in range(0, n):
        pivot_position = get_pivot_position(new_matrix, i, n)
        new_values = update_all_values(new_values, new_matrix, i, pivot_position, n)
        new_matrix = update_all_rows(new_matrix, i, pivot_position, n)

    coefficients = [0 for i in range(0, n)]

    for i in range(0, n):
        pivot_position = get_pivot_position(new_matrix, i, n)
        matrix_value = new_matrix[i][pivot_position]
        coefficient = (1.0 * new_values[i]) / matrix_value
        coefficients[pivot_position] = coefficient

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

    split = [False for i in range(0, n)]

    tolerance = 0.2
    for i in range(0, n):
        if error[i][1] > tolerance:
            split[error[i][0]] = True

    split_intervals = []
    start_index = 0;
    end_index = 0;
    for i in range(1, n):
        if split[i] == split[i - 1]:
            end_index = end_index + 1
        else:
            new_tuple = (start_index, end_index)
            split_intervals.append(new_tuple)
            start_index = end_index
            end_index = start_index

    if end_index != start_index:
        new_tuple = (start_index, end_index)
        split_intervals.append(new_tuple)

    number_of_functions = len(split_intervals)
    functions = [[0 for i in range(0, n)] for j in range(0, number_of_functions)]

    for i in range(0, number_of_functions):
        list_points = []
        start_index = split_intervals[i][0]
        end_index = split_intervals[i][1]

        for j in range(start_index, end_index + 1):
            list_points.append(points[j])

        degree = n
        curve = get_curve(list_points, degree)
        functions[i]  = curve

def print_matrix(matrix):
    string = ""

    for i in range(0, len(matrix)):
        for j in range(0, len(matrix)):
            string += str(matrix[i][j]) + "\t"
        string += "\n"

    print(string)

def test():
    data_points = [(1, 1.25), (2, 0.94), (3, 0.65), (4, 0.62), (5, 0.87), (6, 0.94)]
    model = get_curve(data_points)

    print(model)

test()
