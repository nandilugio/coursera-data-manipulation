import collections
import sys

import MapReduce


mr = MapReduce.MapReduce()

# Calculating C = A x B

# A has dimensions L,M
# B has dimensions M,N

# These weren't provided in the problem, but where easily found
# by inspecting the data. Changing the data will require to update
# this numbers! Finding out this numbers dynamically requires
# another processing step that can't be done in this assignment.
#
# See the discussion in the forum:
# https://www.coursera.org/learn/data-manipulation/discussions/all/threads/YXazUeLnEeWAzxJelNFrFw
L = 5
M = 5
N = 5


def mapper(record):
    matrix_id, row, col, value = record

    if matrix_id == "a":
        i, j = row, col
        for k in range(0, N):
            mr.emit_intermediate((i, k), (matrix_id, j, value))
    elif matrix_id == "b":
        j, k = row, col
        for i in range(0, L):
            mr.emit_intermediate((i, k), (matrix_id, j, value))


def reducer(key, list_of_values):
    i, k = key

    operand_values = {
        "a": collections.defaultdict(lambda: 0),
        "b": collections.defaultdict(lambda: 0),
    }
    for triplet in list_of_values:
        matrix_id, j, value = triplet
        operand_values[matrix_id][j] = value

    result_cell_value = 0
    for j in range(0, M):
        result_cell_value += operand_values["a"][j] * operand_values["b"][j]

    if result_cell_value > 0:
        mr.emit((i, k, result_cell_value))


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
