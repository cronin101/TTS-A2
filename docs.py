from file_reader import FileReader
from itertools import chain, islice, repeat, imap
from collections import defaultdict
from os import linesep
import string

queries = FileReader('./qrys.txt').all()
documents = list(FileReader('./docs.txt', True).all())

class DocsScorer:
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
        postings = [self.posting[query] for query in queries]
        pointers = [0 for posting in postings]
        ends     = [len(posting) - 1 for posting in postings]
        frontier = [posting[0] for posting in postings]

        def increment_and_check_end(matches):
          for index in matches:
            if pointers[index] == ends[index]:
              return True
            else:
              pointers[index] += 1
              frontier[index] = postings[index][pointers[index]]
          return False

        while True:
          document = max(frontier)
          matches = [index for (index, this_document) in enumerate(frontier) if this_document == document]

          if len(matches) == len(pointers):
            yield str(document)

          if increment_and_check_end(matches):
            return

      return islice(do_linear_merge(q), num_matches)

    with open(self.filename, 'w') as docs_top:
      for (q_n, q) in queries:
        docs_top.write(str(q_n) + ' ' + string.join(recent_matches(q, self.documents, 5), ' ') + linesep)

DocsScorer(queries, documents, './docs.top').build_matching_vectors().output_scores()
