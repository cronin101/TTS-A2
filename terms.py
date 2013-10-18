from file_reader import FileReader
from itertools import chain, islice, repeat
from collections import defaultdict
from os import linesep
import string

queries = FileReader('./qrys.txt').all()
documents = list(FileReader('./docs.txt').all())

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
    with open(self.filename, 'w') as terms_top:
      _join = string.join

      def increment(score, doc_id):
        score[doc_id - 1] += 1

      for (q_n, q) in queries:
        partial_score = list(repeat(0, len(documents)))
        for term in q:
          for doc_id in self.posting[term]: increment(partial_score, doc_id)

        matches = (str(doc_id) for doc_id in xrange(len(documents), 0, -1) if partial_score[doc_id - 1] == len(q))
        line = q_n + ' ' + _join(islice(matches, 5), ' ') + linesep
        terms_top.write(line)

TermScorer(queries, documents, './terms.top').build_index().output_scores()
