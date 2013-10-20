from file_reader import FileReader
from itertools import chain, islice, repeat, imap
from collections import defaultdict
from os import linesep
from bisect import bisect_left, bisect_right
import string
from heapq import heappush, heappop
import sys

class BestScorer:
  def __init__(self, queries, documents, filename):
    self.filename                = filename
    self.posting                 = defaultdict(list)
    self.queries, self.documents = queries, documents

  def build_matching_vectors(self):
    for (doc_id, content) in self.documents:
      for word in content: self.posting[word].append(doc_id)
    return self

  def output_scores(self):
    def recent_matches(terms, num_matches):
      num_terms = len(terms)
      def do_linear_merge(queries):
        if min(len(self.posting[query]) for query in queries) == 0:
          return

        min_max  = min((self.posting[query][-1] for query in queries))
        max_min  = max((self.posting[query][0] for query in queries))

        def set_in_range(posting):
          left = bisect_left(posting, max_min)
          right = bisect_right(posting, min_max)
          return set(posting[left:right])

        h = []
        for posting in ((len(p), p) for p in (set_in_range(self.posting[query]) for query in queries)):
          heappush(h, posting)

        popheap = (heappop(h)[1] for i in xrange(num_terms))

        documents = sorted(reduce(lambda x,y: x&y, popheap), reverse=True)
        for doc in documents:
          yield str(doc)
        return

      return islice(do_linear_merge(terms), num_matches)

    with open(self.filename, 'w') as docs_top:
      _join = string.join
      docs_top.write(_join((str(q_n) + ' ' + _join(recent_matches(q, 5), ' ') + linesep for (q_n, q) in queries), ''))


num_documents = None

if len(sys.argv) >= 2:
  num_documents   = int(sys.argv[1])

queries = FileReader('./qrys.txt').all()
documents = islice(FileReader('./docs.txt').all(), num_documents)

BestScorer(queries, documents, './best.top').build_matching_vectors().output_scores()
