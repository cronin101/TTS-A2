from file_reader import FileReader
from itertools import chain, islice, repeat, imap
from collections import defaultdict
from os import linesep
from bisect import bisect_left, bisect_right
import string
from heapq import heappush, heappop
from operator import and_
import gc
import sys

class SetScorer:
  def __init__(self, query_file='./../data/qrys.txt', n_docs=None, doc_file='./../data/docs.txt', filename='./../rankings/set.top'):
    self.filename  = filename
    self.posting   = defaultdict(set)
    self.queries   = FileReader(query_file).all()
    self.documents = islice(FileReader(doc_file).all(), n_docs)

  def build_matching_vectors(self):
    for (doc_id, content) in self.documents:
      for word in content: self.posting[word].add(doc_id)
    return self

  def output_scores(self):
    _l = len
    _posting = self.posting
    def recent_matches(terms, num_matches):
      num_terms = _l(terms)
      def do_linear_merge():
        h = []

        for posting in ((_l(p), p) for p in (_posting[term] for term in terms)):
          heappush(h, posting)
        popheap = (heappop(h)[1] for i in xrange(num_terms))

        for doc in sorted(reduce(and_, popheap), reverse=True):
          yield str(doc)
        return

      return islice(do_linear_merge(), num_matches)

    with open(self.filename, 'w') as docs_top:
      _join = string.join
      docs_top.write(_join((str(q_n) + ' ' + _join(recent_matches(q, 5), ' ') + linesep for (q_n, q) in self.queries), ''))

if __name__ == "__main__":
  gc.disable()
  num_documents = None
  if len(sys.argv) >= 2:
    num_documents   = int(sys.argv[1])


  SetScorer(n_docs=num_documents).build_matching_vectors().output_scores()
