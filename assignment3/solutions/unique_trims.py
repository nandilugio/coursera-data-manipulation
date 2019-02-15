import sys

import MapReduce


mr = MapReduce.MapReduce()


def mapper(record):
    raw_nucleotides = record[1]

    trimmed_nucleotides = raw_nucleotides[:-10]

    mr.emit_intermediate(trimmed_nucleotides, None)


def reducer(key, list_of_values):
    trimmed_nucleotides = key

    mr.emit(trimmed_nucleotides)


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
