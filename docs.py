from file_reader import FileReader
from itertools import chain, islice, repeat, imap
from collections import defaultdict
from os import linesep
from bisect import bisect_left, bisect_right
import string
import sys
import gc

documents = list(FileReader('./docs.txt').all())

class DocsScorer:
  def __init__(self, query_file='./qrys.txt', n_docs=None, doc_file='./docs.txt', filename='./docs.top'):
    self.filename                = filename
    self.posting                 = defaultdict(list)
    self.queries = FileReader(query_file).all()
    self.documents = islice(FileReader(doc_file).all(), n_docs)

  def build_matching_vectors(self):
    for (doc_id, content) in self.documents:
      for word in content: self.posting[word].append(doc_id)
    return self

  def output_scores(self):
    def recent_matches(terms, num_matches):
      def do_linear_merge(queries):
        postings = [self.posting[query] for query in queries]
        pointers = [len(posting) - 1 for posting in postings]
        if min(pointers) == -1:
          return
        frontier = [posting[-1] for posting in postings]

        while True:
          document = max(frontier)
          matches = [index for (index, this_document) in enumerate(frontier) if this_document == document]
          if len(matches) == len(pointers):
            yield str(document)

          for index in matches:
            if pointers[index] == 0:
              return
            else:
              pointers[index] -= 1
              frontier[index] = postings[index][pointers[index]]

      return islice(do_linear_merge(q), num_matches)

    with open(self.filename, 'w') as docs_top:
      for (q_n, q) in self.queries:
        docs_top.write(str(q_n) + ' ' + string.join(recent_matches(q, 5), ' ') + linesep)

if __name__ == '__main__':
  gc.disable()
  num_docs = None
  if len(sys.argv) > 1:
    num_docs = int(sys.argv[1])
  DocsScorer(n_docs = num_docs).build_matching_vectors().output_scores()
