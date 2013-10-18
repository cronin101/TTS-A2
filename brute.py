import string
from itertools import islice
from file_reader import FileReader
from os import linesep

queries = FileReader('./qrys.txt').all()
documents = list(FileReader('./docs.txt', True).all())

with open('./brute.top', 'w') as brute:
  _join = string.join

  def recent_docs(take_n, query):
    return islice((d_n for (d_n, d) in documents if query <= d), take_n)

  def match_line(query):
    query_number, terms = query
    return query_number + ' ' + _join(recent_docs(5, terms), ' ') + linesep

  brute.write(_join((match_line(query) for query in queries), ''))
