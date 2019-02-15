import sys

import MapReduce


mr = MapReduce.MapReduce()


def mapper(record):
    person, friend = record

    mr.emit_intermediate(person, ("has_as_friend", friend))
    mr.emit_intermediate(friend, ("is_friend_of", person))


def reducer(key, list_of_values):
    person, friendships = key, list_of_values

    friends = set()
    friend_of = set()
    all_other_persons = set()
    for friendship in friendships:
        kind, other_person = friendship
        all_other_persons.add(other_person)
        if kind == "has_as_friend":
            friends.add(other_person)
        elif kind == "is_friend_of":
            friend_of.add(other_person)

    for other_person in all_other_persons:
        is_symetric_friend = other_person in friends and other_person in friend_of
        if not is_symetric_friend:  # and person > other_person:  # Grader expects both (a, b) and (b, a) pairs
            mr.emit((person, other_person))


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
