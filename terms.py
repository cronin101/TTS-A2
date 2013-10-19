from file_reader import FileReader
from itertools import chain, islice, repeat
from collections import defaultdict
from os import linesep
import string

queries = FileReader('./qrys.txt').all()
documents = list(FileReader('./docs.txt', True).all())

class TermScorer:
  def __init__(self, queries, documents, filename):
    self.filename = filename
    self.posting = defaultdict(set)
    self.queries, self.documents = queries, documents

  def build_index(self):
    documents = self.documents
    for (doc_id, words) in documents:
      for word in words:
        self.posting[word].add(int(doc_id))

    return self


  def output_scores(self):
    def recent_matches(terms, documents, num_matches):
      partial_score = list(repeat(0, len(documents)))
      for term in q:
        for doc_id in self.posting[term]: partial_score[doc_id - 1] += 1
      matches = (str(doc_id) for doc_id in xrange(len(documents), 0, -1) if partial_score[doc_id - 1] == len(q))
      return islice(matches, num_matches)

    with open(self.filename, 'w') as terms_top:
      for (q_n, q) in queries:
        terms_top.write(str(q_n) + ' ' + string.join(recent_matches(q, self.documents, 5), ' ') + linesep)

TermScorer(queries, documents, './terms.top').build_index().output_scores()
