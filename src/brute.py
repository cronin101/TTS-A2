import string
from itertools import islice
from file_reader import FileReader
from os import linesep
import gc
import sys

class BruteScorer:
  def __init__(self, query_file='./../data/qrys.txt', n_docs=None, doc_file='./../data/docs.txt', filename='./../rankings/brute.top'):
    self.filename = filename
    self.queries = FileReader(query_file).all()
    self.documents = list(islice(FileReader(doc_file, True).all(), n_docs))

  def output_scores(self):
    with open(self.filename, 'w') as brute:
      _join = string.join

      def recent_docs(take_n, query):
        return islice((str(d_n) for (d_n, d) in self.documents if query <= d), take_n)

      def match_line(query):
        query_number, terms = query
        return str(query_number) + ' ' + _join(recent_docs(5, terms), ' ') + linesep

      brute.write(_join((match_line(query) for query in self.queries), ''))

if __name__ == "__main__":
  gc.disable()
  num_documents = None
  if len(sys.argv) >= 2:
    num_documents   = int(sys.argv[1])


  BruteScorer(n_docs=num_documents).output_scores()
