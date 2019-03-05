import csv

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
        
#[x[n], x[n-1], ... , x[0]]
def get_solution_vector(matrix, values):
    n = len(matrix)
    new_matrix = matrix

    #gaussian elimination
    for i in range(0, n):
        for j in range(0, n):
            if i != j and new_matrix[i][i] != 0:
                ratio = (-1.0 * new_matrix[j][i])/new_matrix[i][i]
                for k in range(0, n):
                    value =  (ratio * new_matrix[i][k]) + new_matrix[j][k]
                    new_matrix[j][k] = value
