import string
from itertools import islice
from file_reader import FileReader
from os import linesep

queries = FileReader('./qrys.txt').all()
documents = FileReader('./docs.txt').all()

with open('./brute.top', 'w') as brute:
  _join = string.join
  d_list = list(documents)
  d_list.reverse()

  def recent_docs(take_n, query):
    return islice((d_n for (d_n, d) in d_list if query.issubset(d)), take_n)

  def match_line(query):
    query_number, terms = query
    return query_number + ' ' + _join(recent_docs(5, terms), ' ') + linesep

  brute.write(_join((match_line(query) for query in queries), ''))
