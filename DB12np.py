#!/usr/bin/python

########################################################################
# File :    DIRACbenchmark.py
# Author :  Andrew McNab 
########################################################################

""" DIRAC Benchmark 2012 by Ricardo Graciani, and wrapper functions to
    run multiple copies in parallel by Andrew McNab.
    
    This file (DIRACbenchmark.py) is intended to be the ultimate upstream
    shared by different users of the DIRAC Benchmark 2012 (DB12). The
    canonical version can be found at https://github.com/DIRACGrid/DB12
    
    This script can either be imported or run from the command line:
    
    ./DIRACbenchmark.py NUMBER
    
    where NUMBER gives the number of benchmark processes to run in parallel.
    
    Run  ./DIRACbenchmark.py help  to see more options.
"""

import os
import sys
import random
import urllib
import multiprocessing
import numpy as np

version = '00.03 DB12'

def singleDiracBenchmark( iterations = 1, extraIteration = False ):
  """ Get Normalized Power of one CPU in DIRAC Benchmark 2012 units (DB12)
  """

  # This number of iterations corresponds to 1kHS2k.seconds, i.e. 250 HS06 seconds
  # modified to normalize to HS06 on Intel(R) Xeon(R) CPU E5-2630 v4
  # running 10 threads on a single node

  n = int(1000 * 12.5 )
  calib = 19.11

  m = 0. 
  m2 = 0.
  p = 0.
  p2 = 0.
  # Do one iteration extra to allow CPUs with variable speed (we ignore zeroth iteration)
  # Possibly do one extra iteration to avoid tail effects when copies run in parallel
  for i in range( iterations + 1 + (2 if extraIteration else 0)):
    if i == 1:
      start = os.times()

    # Now the iterations
    for _j in xrange( n ):
      t = np.random.normal(10, 1, 1000)
      m += np.sum(t)
      m2 += np.sum(t * t)
      p += np.sum(t)
      p2 += np.sum(t * t)

    if i == iterations:
      end = os.times()

  cput = sum( end[:4] ) - sum( start[:4] )
  wall = end[4] - start[4]

  if not cput:
    return None
  
  # Return DIRAC-compatible values
  return { 'CPU' : cput, 'WALL' : wall, 'NORM' : calib * iterations / cput, 'UNIT' : 'DB12' }

def singleDiracBenchmarkProcess( resultObject, iterations = 1, extraIteration = False ):

  """ Run singleDiracBenchmark() in a multiprocessing friendly way
  """

  benchmarkResult = singleDiracBenchmark( iterations = iterations, extraIteration = extraIteration )
  
  if not benchmarkResult or 'NORM' not in benchmarkResult:
    return None
    
  # This makes it easy to use with multiprocessing.Process
  resultObject.value = benchmarkResult['NORM']

def multipleDiracBenchmark( copies = 1, iterations = 1, extraIteration = False ):

  """ Run multiple copies of the DIRAC Benchmark in parallel  
  """

  processes = []
  results = []

  # Set up all the subprocesses
  for i in range( copies ):
    results.append( multiprocessing.Value('d', 0.0) )
    processes.append( multiprocessing.Process( target = singleDiracBenchmarkProcess, args = ( results[i], iterations, extraIteration) ) )
 
  # Start them all off at the same time 
  for p in processes:  
    p.start()
    
  # Wait for them all to finish
  for p in processes:
    p.join()

  raw     = []
  product = 1.0

  for result in results:
    raw.append( result.value )
    product *= result.value

  raw.sort()
  
  # Return the list of raw results and various averages
  return { 'raw'             : raw,
           'copies'          : copies,
           'sum'             : sum(raw),
           'arithmetic_mean' : sum(raw)/copies,
           'geometric_mean'  : product ** (1.0 / copies),
           'median'          : raw[(copies-1) / 2] }
  
def wholenodeDiracBenchmark( copies = None, iterations = 1, extraIteration = False ): 

  """ Run as many copies as needed to occupy the whole machine
  """
  
  # Try $MACHINEFEATURES first if not given by caller
  if not copies and 'MACHINEFEATURES' in os.environ:
    try:
      copies = int( urllib.urlopen( os.environ['MACHINEFEATURES'] + '/total_cpu' ).read() )
    except:
      pass

  # If not given by caller or $MACHINEFEATURES/total_cpu then just count CPUs
  if not copies:
    try:
      copies = multiprocessing.cpu_count()
    except:
      copies = 1
  
  return multipleDiracBenchmark( copies = copies, iterations = iterations, extraIteration = extraIteration )
  
def jobslotDiracBenchmark( copies = None, iterations = 1, extraIteration = False ):

  """ Run as many copies as needed to occupy the job slot
  """

  # Try $JOBFEATURES first if not given by caller
  if not copies and 'JOBFEATURES' in os.environ:
    try:
      copies = int( urllib.urlopen( os.environ['JOBFEATURES'] + '/allocated_cpu' ).read() )
    except:
      pass

  # If not given by caller or $JOBFEATURES/allocated_cpu then just run one copy
  if not copies:
    copies = 1
  
  return multipleDiracBenchmark( copies = copies, iterations = iterations, extraIteration = extraIteration )

#
# If we run as a command
#   
if __name__ == "__main__":

  helpString = """DIRACbenchmark.py [--iterations ITERATIONS] [--extra-iteration]
                  [COPIES|single|wholenode|jobslot|version|help] 
Uses the functions within DIRACbenchmark.py to run the DB12 benchmark from the 
command line.
By default one benchmarking iteration is run, in addition to the initial 
iteration which DB12 runs and ignores to avoid ramp-up effects at the start.
The number of benchmarking iterations can be increased using the --iterations
option. An additional final iteration which is also ignored can be added with
the --extra-iteration option, to avoid tail effects.
The COPIES (ie an integer) argument causes multiple copies of the benchmark to
be run in parallel. The tokens "wholenode", "jobslot" and "single" can be 
given instead to use $MACHINEFEATURES/total_cpu, $JOBFEATURES/allocated_cpu, 
or 1 as the number of copies respectively. If $MACHINEFEATURES/total_cpu is
not available, then the number of (logical) processors visible to the 
operating system is used.
Unless the token "single" is used, the script prints the following results to
two lines on stdout:
COPIES SUM ARITHMETIC-MEAN GEOMETRIC-MEAN MEDIAN
RAW-RESULTS
The tokens "version" and "help" print information about the script.
The source code of DIRACbenchmark.py provides examples of how the functions
within DIRACbenchmark.py can be used by other Python programs.
DIRACbenchmark.py is distributed from  https://github.com/DIRACGrid/DB12
"""

  copies         = None
  iterations     = 1
  extraIteration = False

  for arg in sys.argv[1:]:
    if arg.startswith('--iterations='):
      iterations = int(arg[13:])
    elif arg == '--extra-iteration':
      extraIteration = True
    elif arg == '--help' or arg == 'help':
      print helpString
      sys.exit(0)
    elif not arg.startswith('--'):
      copies = arg

  # print iterations, copies

  if copies == 'version':
    print version
    sys.exit(0)

  if copies is None or copies == 'single':
     print singleDiracBenchmark()['NORM']
     sys.exit(0)

  if copies == 'wholenode':
    result = wholenodeDiracBenchmark( iterations = iterations, extraIteration = extraIteration )
    print result['copies'],result['sum'],result['arithmetic_mean'],result['geometric_mean'],result['median']
    print ' '.join([str(i) for i in result['raw']])
    sys.exit(0)

  if copies == 'jobslot':
    result = jobslotDiracBenchmark( iterations = iterations, extraIteration = extraIteration )
    print result['copies'],result['sum'],result['arithmetic_mean'],result['geometric_mean'],result['median']
    print ' '.join([str(i) for i in result['raw']])
    sys.exit(0)

  result = multipleDiracBenchmark( copies = int(copies), iterations = iterations, extraIteration = extraIteration )
  print result['copies'],result['sum'],result['arithmetic_mean'],result['geometric_mean'],result['median']
  print ' '.join([str(i) for i in result['raw']])
  sys.exit(0)

