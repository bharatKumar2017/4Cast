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

    
