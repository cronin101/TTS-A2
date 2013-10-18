from file_reader import FileReader
from itertools import chain, islice
from collections import defaultdict
from os import linesep
import string

queries = list(FileReader('./qrys.txt').all())
documents = list(FileReader('./docs.txt').all())
documents.reverse

posting = defaultdict(set)

for (doc_id, words) in documents:
  for word in words:
    posting[word].add(doc_id)

with open('terms.top', 'w') as terms_top:
  _join = string.join
  for (q_n, q) in queries:
    partial_score = {}
    q_terms = frozenset(q)
    for term in q_terms:
      for doc_id in posting[term]:
        partial_score[doc_id] = partial_score.get(doc_id, 0) + 1

    matches = (doc_id for doc_id in partial_score.keys() if partial_score[doc_id] == len(q_terms))
    line = q_n + ' ' + _join(islice(matches, 5), ' ') + linesep
    terms_top.write(line)
