import time
from pylab import *
from best import BestScorer
from brute import BruteScorer
from docs import DocsScorer
from doc2 import DocScorerPlus
from terms import TermScorer
from operator import add

# Original testing set
sizes = [100,200,500,1000,2000,5000,10000,20000]

def time_it(scoring_lambda):
  started = time.time()
  scoring_lambda()
  return time.time() - started

def average_it(scoring_lambda):
  num_trials = 3
  return reduce(add, (time_it(scoring_lambda) for i in xrange(num_trials))) / float(num_trials)

bests = map(lambda s: average_it(lambda: BestScorer(n_docs=s)),sizes)
print 'Best done.'
brutes = map(lambda s: average_it(lambda: BruteScorer(n_docs=s).output_scores()),sizes)
print 'Brutes done.'
docs = map(lambda s: average_it(lambda: DocsScorer(n_docs=s).build_matching_vectors().output_scores()),sizes)
print 'Docs done.'
doc2 = map(lambda s: average_it(lambda: DocScorerPlus(n_docs=s).build_matching_vectors().output_scores()),sizes)
print 'Doc2 done.'
terms = map(lambda s: average_it(lambda: TermScorer(n_docs=s).build_index().output_scores()),sizes)
print 'Terms done.'

print 'Done!'

plot(sizes, bests, ':b')
plot(sizes, bests, 'bo', label='Best algorithm (best.py)')
plot(sizes, brutes, ':r')
plot(sizes, brutes, 'ro', label='Brute force (brute.py)')
plot(sizes, docs, ':g')
plot(sizes, docs, 'go', label='Document-at-a-time (docs.py)')
plot(sizes, doc2, ':k')
plot(sizes, doc2, 'ko', label='Improved Doc-at-a-time (doc2.py)')
plot(sizes, terms, ':y')
plot(sizes, terms, 'yo', label='Term-at-a-time (terms.py)')
xscale('log')
xlabel('Document count')
yscale('log')
ylabel('Runtime in seconds')
legend(loc='upper left')
show()
