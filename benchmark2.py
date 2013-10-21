import time
from pylab import *
from best import BestScorer
from brute import BruteScorer
from docs import DocsScorer
from doc2 import DocScorerPlus
from terms import TermScorer
from operator import add

# Original testing set
sizes = [100000,200000,500000,1000000,2000000,5000000]

def time_it(scoring_lambda):
  print '-'
  started = time.time()
  scoring_lambda()
  taken = time.time() - started
  print '.'
  return taken

def average_it(scoring_lambda):
  num_trials = 1
  return reduce(add, (time_it(scoring_lambda) for i in xrange(num_trials))) / float(num_trials)

bests = map(lambda s: average_it(lambda: BestScorer(query_file='./qrys.txt.1', n_docs=s, doc_file='./full.txt')),sizes)
print 'Best done.'

doc2s = map(lambda s: average_it(lambda: DocScorerPlus(query_file='./qrys.txt.1', n_docs=s, doc_file='./full.txt').build_matching_vectors().output_scores()),sizes)
print 'Best done.'

plot(sizes, bests, ':b')
plot(sizes, bests, 'bo', label='Best algorithm (best.py)')
plot(sizes, doc2s, ':r')
plot(sizes, doc2s, 'ro', label='Improved doc-at-a-time algorithm (doc2.py)')
xscale('log')
xlabel('Document count')
yscale('log')
ylabel('Runtime in seconds')
legend(loc='upper left')
show()
