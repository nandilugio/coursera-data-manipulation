import sys

import MapReduce


mr = MapReduce.MapReduce()


def mapper(record):
    person, friend = record

    mr.emit_intermediate(person, friend)


def reducer(key, list_of_values):
    person, friends = key, list_of_values

    friend_count  = len(friends)

    mr.emit((person, friend_count))


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
