from file_reader import FileReader
from itertools import chain, islice, repeat, imap
from collections import defaultdict
from os import linesep
from bisect import bisect_left, bisect_right
import string
import sys
import gc

class DocScorerPlus:
  def __init__(self, query_file='./qrys.txt', n_docs=None, doc_file='./docs.txt', filename='./docs+.top'):
    self.filename  = filename
    self.posting   = defaultdict(list)
    self.queries   = FileReader(query_file).all()
    self.documents = islice(FileReader(doc_file).all(), n_docs)

  def build_matching_vectors(self):
    for (doc_id, content) in self.documents:
      for word in content: self.posting[word].append(doc_id)
    return self

  def output_scores(self):
    _posting = self.posting
    _bl, _br = bisect_left, bisect_right
    _l, _z, _mi, _ma, _en, _s = len, zip, min, max, enumerate, str
    def recent_matches(terms, num_matches):
      def do_linear_merge():
        n_terms  = _l(terms)
        postings = [_posting[term] for term in terms]
        pointers = repeat(-1, n_terms)
        ends     = repeat(0, n_terms)

        while True:
          if _mi(len(posting) for posting in postings) == 0:
            return
          min_max  = _mi(posting[pointer] for (posting, pointer) in _z(postings, pointers))
          max_min  = _ma(posting[end] for (posting, end) in _z(postings, ends))
          pointers = [_br(posting, min_max) - 1 for posting in postings]
          if _mi(pointers) == (-1): return

          ends     = [_bl(posting, max_min) for posting in postings]
          frontier = [posting[pointer] for (posting, pointer) in _z(postings, pointers)]
          document = _ma(frontier)
          matches  = [index for (index, this_document) in _en(frontier) if this_document == document]

          if _l(matches) == n_terms:
            yield _s(document)

          for index in matches:
            reached_end = pointers[index] == ends[index]
            if reached_end: return
            else:           pointers[index] -= 1

      return islice(do_linear_merge(), num_matches)

    with open(self.filename, 'w') as docs_top:
      for (q_n, q) in self.queries:
        docs_top.write(str(q_n) + ' ' + string.join(recent_matches(q, 5), ' ') + linesep)

if __name__ == "__main__":
  if len(sys.argv) > 1:
    num_d = int(sys.argv[1])
  else:
    num_d = None

  gc.disable()
  DocScorerPlus(n_docs=num_d).build_matching_vectors().output_scores()
