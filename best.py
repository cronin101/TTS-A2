from file_reader import FileReader
from itertools import chain, islice, repeat, imap
from collections import defaultdict
from os import linesep
from bisect import bisect_left, bisect_right
import string
import sys
import gc

class BestScorer:
  def __init__(self, query_file='./qrys.txt', n_queries=None, documents='./docs.txt', filename='./best.top'):
    self.filename  = filename
    self.posting   = defaultdict(list)
    self.queries   = islice(FileReader(query_file).all(), n_queries)
    self.documents = list(FileReader(documents).all())

  def build_matching_vectors(self):
    for (doc_id, content) in self.documents:
      for word in content: self.posting[word].append(doc_id)
    return self

  def output_scores(self):
    def recent_matches(terms, documents, num_matches):
      def do_linear_merge(queries):
        def decrement_and_check_end(matches):
          for index in matches:
            reached_end = pointers[index] == ends[index]
            if reached_end: return True
            else:           pointers[index] -= 1
          return False

        n_terms  = len(terms)
        postings = [self.posting[query] for query in queries]
        pointers = repeat(-1, n_terms)
        ends     = repeat(0, n_terms)

        while True:
          min_max  = min(posting[pointer] for (posting, pointer) in zip(postings, pointers))
          max_min  = max(posting[end] for (posting, end) in zip(postings, ends))
          pointers = [bisect_right(posting, min_max) - 1 for posting in postings]
          if min(pointers) == (-1): return

          ends     = [bisect_left(posting, max_min) for posting in postings]
          frontier = [posting[pointer] for (posting, pointer) in zip(postings, pointers)]
          document = max(frontier)
          matches  = [index for (index, this_document) in enumerate(frontier) if this_document == document]

          if len(matches) == n_terms:          yield str(document)
          if decrement_and_check_end(matches): return
      return islice(do_linear_merge(q), num_matches)

    with open(self.filename, 'w') as docs_top:
      for (q_n, q) in self.queries:
        docs_top.write(str(q_n) + ' ' + string.join(recent_matches(q, self.documents, 5), ' ') + linesep)

gc.disable()
BestScorer().build_matching_vectors().output_scores()
