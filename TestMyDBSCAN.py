import logging
import pytest
import re

import dbscan


class LogEntry:
    def __init__(self, log_entry):
        self.original_entry = log_entry
        self.entry_set = set(re.compile("""\s+|{|}|\(|\)|\[|\]""").split(log_entry))

    def get_entry(self):
        return self.original_entry

    def get_entry_set(self):
        return self.entry_set


def dist(a, b):
    intersection_len = len(a.get_entry_set().intersection(b.get_entry_set()))
    union_len = len(a.get_entry_set().union(b.get_entry_set()))
    return 1.0 - float(intersection_len) / float(union_len)


dataset = [LogEntry(s) for s in ['a}b', 'b(c', 'b    c']]

assert dataset[0].get_entry() == "a}b"
assert dataset[0].get_entry_set() == {'a', 'b'}
assert dataset[1].get_entry() == 'b(c'
assert dataset[1].get_entry_set() == {'b', 'c'}
assert dataset[2].get_entry() == 'b    c'
assert dataset[2].get_entry_set() == {'b', 'c'}

assert dist(dataset[0], dataset[1]) == 1.0 - 1.0/3.0
assert dist(dataset[1], dataset[2]) == 0.0
assert dist(dataset[0], dataset[2]) == 1.0 - 1.0/3.0

cluster_ids = dbscan.MyDBSCAN(dataset, 0.7, 2, dist)

assert cluster_ids == [1, 1, 1]

cluster_ids = dbscan.MyDBSCAN(dataset, 0.5, 2, dist)

assert cluster_ids == [-1, 1, 1]

cluster_ids = dbscan.MyDBSCAN(dataset, 0.5, 1, dist)

assert cluster_ids == [1, 2, 2]
