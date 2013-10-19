from file_reader import FileReader
from itertools import chain, islice, repeat, imap
from collections import defaultdict
from os import linesep
from bisect import bisect_left, bisect_right
import string

queries = FileReader('./qrys.txt').all()
documents = list(FileReader('./docs.txt').all())

class BestScorer:
  def __init__(self, queries, documents, filename):
    self.filename                = filename
    self.posting                 = defaultdict(set)
    self.queries, self.documents = queries, documents

  def build_matching_vectors(self):
    self.posting = defaultdict(list)
    for (doc_id, content) in self.documents:
      for word in content: self.posting[word].append(doc_id)
    return self

  def output_scores(self):
    def recent_matches(terms, documents, num_matches):
      def do_linear_merge(queries):
        min_max  = min((self.posting[query][-1] for query in queries))
        max_min  = max((self.posting[query][0] for query in queries))

        def in_range(posting):
          left = bisect_left(posting, max_min)
          right = bisect_right(posting, min_max)
          return posting[left:right]

        postings = (in_range(self.posting[query]) for query in queries)
        documents = sorted(reduce(lambda x,y: x&y, sorted(imap(lambda p: set(p), postings), key=len)), reverse=True)
        for doc in documents:
          yield str(doc)
        return

      return islice(do_linear_merge(q), num_matches)

    with open(self.filename, 'w') as docs_top:
      for (q_n, q) in queries:
        docs_top.write(str(q_n) + ' ' + string.join(recent_matches(q, self.documents, 5), ' ') + linesep)

BestScorer(queries, documents, './best.top').build_matching_vectors().output_scores()
