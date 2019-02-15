import sys

import MapReduce


mr = MapReduce.MapReduce()


def mapper(record):
    order_id = record[1]

    mr.emit_intermediate(order_id, record)


def reducer(key, list_of_values):
    order_id, records = key, list_of_values

    order_record = None
    line_item_records = []
    for record in records:
        record_type = record[0]
        if record_type == "order":
            if order_record:
                raise RuntimeError("More than 1 order record for order_id: " + str(order_id))
            order_record = record
        elif record_type == "line_item":
            line_item_records.append(record)
        else:
            raise RuntimeError("Unexpected record type: " + record_type)

    for line_item_record in line_item_records:
        mr.emit(order_record + line_item_record)


if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
