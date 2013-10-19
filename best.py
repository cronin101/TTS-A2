from file_reader import FileReader
from itertools import chain, islice, repeat, imap
from collections import defaultdict
from os import linesep
from bisect import bisect_left, bisect_right
import string
from heapq import heappush, heappop
import gc

queries = FileReader('./qrys.txt').all()
documents = FileReader('./docs.txt').all()

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
        min_max  = min((self.posting[query][-1] for query in queries))
        max_min  = max((self.posting[query][0] for query in queries))

        def set_in_range(posting):
          left = bisect_left(posting, max_min)
          right = bisect_right(posting, min_max)
          return set(posting[left:right])

        postings = ((len(p), p) for p in (set_in_range(self.posting[query]) for query in queries))

        h = []
        for p in postings: heappush(h, p)

        def gen_heap(h):
          return (heappop(h)[1] for i in xrange(num_terms))

        documents = sorted(reduce(lambda x,y: x&y, gen_heap(h)), reverse=True)
        for doc in documents:
          yield str(doc)
        return

      return islice(do_linear_merge(terms), num_matches)

    with open(self.filename, 'w') as docs_top:
      _join = string.join
      docs_top.write(_join((str(q_n) + ' ' + _join(recent_matches(q, 5), ' ') + linesep for (q_n, q) in queries), ''))

gc.disable()
BestScorer(queries, documents, './best.top').build_matching_vectors().output_scores()
