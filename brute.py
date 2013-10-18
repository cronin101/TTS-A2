import string
from itertools import islice
from file_reader import FileReader
from os import linesep

queries = FileReader('./qrys.txt').all()
documents = FileReader('./docs.txt').all()

with open('./brute.top', 'w') as brute:
  _join = string.join
  document_list = list(documents)
  document_list.reverse()
  for (q_n, q) in queries:
    matches = islice((str(d_n) for (d_n, d) in document_list if q.issubset(d)), 5)
    brute.write(str(q_n) + ' ' + _join(matches, ' ') + linesep)
