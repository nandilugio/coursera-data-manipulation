import sys

import MapReduce


mr = MapReduce.MapReduce()


def mapper(record):
    doc_id, text = record

    words = text.split()

    for word in words:
        mr.emit_intermediate(word, doc_id)


def reducer(key, list_of_values):
    word, doc_ids = key, list_of_values

    deduplicated_doc_ids = list(set(list_of_values))

    mr.emit((word, deduplicated_doc_ids))


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
