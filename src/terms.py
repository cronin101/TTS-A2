from file_reader import FileReader
from itertools import chain, islice, repeat
from collections import defaultdict
from os import linesep
import string
import sys
import gc

class TermScorer:
  def __init__(self, query_file='./../data/qrys.txt', n_docs=None, doc_file='./../data/docs.txt', filename='./../rankings/terms.top'):
    self.filename = filename
    self.posting = defaultdict(list)
    self.queries = FileReader(query_file).all()
    self.documents = list(islice(FileReader(doc_file).all(), n_docs))

  def build_index(self):
    documents = self.documents
    for (doc_id, words) in documents:
      for word in words:
        self.posting[word].append(doc_id)
    return self


  def output_scores(self):
    num_docs = len(self.documents)
    def recent_matches(terms, num_matches):
      num_terms = len(terms)
      partial_score = list(repeat(0, num_docs + 1))
      for term in terms:
        for doc_id in self.posting[term]: partial_score[doc_id] += 1
      matches = (str(doc_id) for doc_id in xrange(num_docs, 0, -1) if partial_score[doc_id] == num_terms)
      return islice(matches, num_matches)

    with open(self.filename, 'w') as terms_top:
      for (q_n, q) in self.queries:
        terms_top.write(str(q_n) + ' ' + string.join(recent_matches(q, 5), ' ') + linesep)

if __name__ == '__main__':
  n_docs = None
  if len(sys.argv) > 1:
    n_docs = int(sys.argv[1])
  gc.disable()
  TermScorer(n_docs=n_docs).build_index().output_scores()
