from file_reader import FileReader
from itertools import chain, islice, repeat, imap
from collections import defaultdict
from os import linesep
import string

queries = FileReader('./qrys.txt').all()
documents = list(FileReader('./docs.txt', True).all())

class DocsScorer:
  def __init__(self, queries, documents, filename):
    self.filename = filename
    self.posting = defaultdict(set)
    self.queries, self.documents = queries, documents

  def build_matching_vectors(self):
    self.posting = defaultdict(list)
    for (doc_id, content) in self.documents:
      for word in content: self.posting[word].append(doc_id)
    return self

  def output_scores(self):
    def recent_matches(terms, documents, num_matches):

      def do_linear_merge(postings):
        documents = []
        pointers = [0] * len(postings)
        ends = map(lambda l: len(l) - 1, postings)

        def find_highest_document_id(_postings, _pointers):
          return max(_postings[index][_pointers[index]] for index in xrange(len(pointers)))

        while True:
          document = find_highest_document_id(postings, pointers)
          matching_i = set([])
          for index in xrange(len(pointers)):
            this_document = postings[index][pointers[index]]
            if this_document == document: matching_i.add(index)

          def increment_and_check_end(matches):
            for index in matching_i:
              if pointers[index] == ends[index]:
                return True
              else:
                pointers[index] += 1
            return False

          if len(matching_i) == len(pointers):
            documents.append(str(document))

          if len(documents) == 5 or increment_and_check_end(matching_i):
            return documents

      matches = do_linear_merge(map(lambda q: self.posting[q], q))
      return matches

    with open(self.filename, 'w') as docs_top:
      for (q_n, q) in queries:
        docs_top.write(str(q_n) + ' ' + string.join(recent_matches(q, self.documents, 5), ' ') + linesep)

DocsScorer(queries, documents, './docs.top').build_matching_vectors().output_scores()
