#!/usr/bin/python
# encoding:utf8
import sys
import re
import os
import psutil # if this makes an error, you need to install the psutil package on your system
import time

maxmem = 0
def showMemTime(when='Resources'):
  global maxmem
  # memory and time measurement
  process = psutil.Process(os.getpid())
  mem = process.memory_info()[0] / float(2 ** 20)
  maxmem = max(maxmem, mem)
  ts = process.cpu_times()
  sys.stderr.write("{when:<20}: {mb:4.0f} MB (max {maxmb:4.0f} MB), {user:4.1f} s user, {system:4.1f} s system\n".format(
    when=when, mb=mem, maxmb=maxmem, user=ts.user, system=ts.system))

def  displayKMostFrequentNGramsInFile(k, n, filename):
  #read input
  print "reading the file" +filename
  inputdata = open(filename,'r')

  #ngramcounter
  nc=NGramCounter(k,n)

  print ("splitting words")
  for line in inputdata:
    #split on all spaces
    inputwords = re.split(r' |\n',line)
    #remove empty strings
    inputwords = filter(lambda x: x!= '', inputwords)

    for idx, token in enumerate(inputwords):
      # let's show resources after all 50 K words
      #if idx % 50000 == 49999:
        #showMemTime('counting {} of {}'.format(idx+1, len(inputwords)))
      nc.count(token)
  del inputdata
  del k
  del n
  del filename

  showMemTime('after counting')
  print("ngrams:")
  nc.display()

  del nc

class NGramCounter:
  def __init__(self, k, n):
  # initialize storage dictionary (datatype of {} is 'dict')
    self.ngrams = {}
    self.n = n
    self.k = k
  def count(self, word):
  # make bigram (datatype of (,) is 'tuple')

    #for idx in range(n,len(word)):
    for idx in range(self.n-1 ,len(word)):
      self.registerNgram(word[idx-(self.n-1):idx+1])

  def registerNgram(self, ngram):
    #delete unused ngram variable from memory
    # increase count for this sequence by one
    if ngram not in self.ngrams:
      # if it was not yet in the dictionary
      self.ngrams[ngram] = 1
    else:
      # if it was already in the dictionary
      self.ngrams[ngram] += 1
    del ngram

  def display(self):
    showMemTime('begin display')

    # build list of all frequencies and bigrams
    ngram_freq = list(self.ngrams.items())
    showMemTime('after items')

    # sort that list by frequencies (i.e., second field), descending
    print("sorting ...")
    ngram_freq.sort(key = lambda x:x[1], reverse = True)
    showMemTime('after sorting')

    # iterate over the first five (or less) elements
    print("creating output ...")
    print("printing the {} most frequent {}-grams".format(self.k, self.n))


    for ngram, occurred in ngram_freq[0:self.k]:
      try:
        # python 2
        ngram = unicode.encode(ngram, 'utf8')
      except:
        pass
      print("ngram '{}' occured {:>5} times".format(ngram, occurred))
    
    del ngram_freq
    del self.n
    del self.k

# this is our main function
def main():
  # make sure the user gave us a file to read
  if len(sys.argv) != 2:
    print("need one argument! (file to read from)")
    sys.exit(-1)
  filename = sys.argv[1]

  showMemTime('begin') # let's observe where we use our memory and time

  #Show the 30 most frequent 2-grams
  displayKMostFrequentNGramsInFile(30, 2, filename)
  #Show the 20 most frequent 3-grams
  displayKMostFrequentNGramsInFile(20, 3, filename)
  #Show the 15 most frequent 4-grams
  displayKMostFrequentNGramsInFile(15, 4, filename)
  #Show the 15 most frequent 5-grams
  displayKMostFrequentNGramsInFile(15, 5, filename)
  #Show the 15 most frequent 6-grams.
  displayKMostFrequentNGramsInFile(15, 6, filename)

main()
showMemTime('at the end')