import gc
import sys
from sets import SetScorer
from doc2 import DocScorerPlus

class BestScorer:
  def __init__(self, query_file='./qrys.txt', n_docs=None, doc_file='./docs.txt', filename='./best.top'):
    if n_docs and n_docs < 900:
      DocScorerPlus(query_file, n_docs, doc_file, filename).build_matching_vectors().output_scores()
    else:
      SetScorer(query_file, n_docs, doc_file, filename).build_matching_vectors().output_scores()

if __name__ == "__main__":
  if len(sys.argv) > 1:
    num_d = int(sys.argv[1])
  else:
    num_d = None

  gc.disable()
  BestScorer(n_docs=num_d)
