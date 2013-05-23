#!/usr/bin/env python

from math import log
from tempfile import NamedTemporaryFile
from operator import itemgetter

from ConfigParser import SafeConfigParser
import sys, getopt

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import numpy

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pylab

from bwa import BWA

#global variables
speciesID={} # just for as convenient reference
speciesCount={} # count to evaluate each round which species is the most likely
bigArray=[] # for testing purposes only
bigArray1=[]

#TODO:
# Upload-ProgressBar
# Process-ProgressBar
# display them on the website
# make them downloadable
# add readme and python modules to lib

def create_fasta_records(D):
  c = 1
  for seq, n in sorted(D.iteritems(), key=itemgetter(1), reverse=True):
    if n > 1:
      yield SeqRecord(Seq(seq), id="%d_%d" % (n, c), description='')
      c += 1

def entropy(seq):
  counts = [seq.count(n) for n in 'ACGT']
  total = float(sum(counts))
  entropy = 0
  if total:
    entropy -= sum(c / total * log(c / total, 2) for c in counts if c)
  return entropy

def seqfilter(seq, length, cutoff, complexity_cutoff):
  return len (seq) >= length \
      and seq.count('N') <= cutoff \
      and entropy(seq) >= complexity_cutoff

def sam_reader(fh):
  for line in fh:
    if line.startswith('@'):
      continue
    fields = line.split('\t')
    if fields[2] != '*':
      mms = {fields[2].split('|')[-1]: int(fields[12].split(':')[-1])}
      for s in fields[-1][5:].split(';')[:-1]:
        sfields = s.split(',')
        species = sfields[0].split('|')[-1]
        if not species in mms:
          mms[species] = int(sfields[-1])
      yield fields[0], mms

def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]
     
def process_Sites(sp_dict, templateList):
    tempList = []
    tempList.extend(templateList)
    for speciesName in sp_dict:
        specPos = speciesID[speciesName]
        tempList[specPos] = sp_dict[speciesName]
        speciesCount[speciesName] = speciesCount[speciesName] + 1
        # TODO: correct this way?
        #   because for example in sp_dict = {'Ursus_spelaeus': 5}, ...
        #   where does the '5' here actually have an effect? Only the Graph?
    return tempList

#TODO: takes two arguments: uploaded file path and session-ID to generate (temporary) files
def main(inputFile="data/cavebear.txt", output='defaultOut'):
  outputFile="static/" + output
  config = SafeConfigParser()
  config.read(['speciesd.cfg'])
  bwa_bin = config.get("files", "bwa_bin")
  bwa = BWA(bwa_bin)
  tmpdir = config.get("files", "tmpdir")
  all_genomes = config.get("files", "all_genomes")
  species_ref = config.get("files", "species_ref")
  listBackToServer=[]

  db = {}

  with open(inputFile, 'r') as ifh:
    print('file read')    
  # -------------can this section be optimised? kinda slow at the moment
    for record in SeqIO.parse(ifh, "fastq"):
      s = str(record.seq)
      db[s] = db.get(s, 0) + 1
  # ---------------------------------------------------------------------  
      
  for s in db.keys():
    if not seqfilter(s, length=35, cutoff=2, complexity_cutoff=1.2):
      del(db[s])
  
  tmpfiles = [NamedTemporaryFile(dir=tmpdir, prefix="tmp{}_".format(n))
              for n in range(3)]
                  
  SeqIO.write(create_fasta_records(db), tmpfiles[0], "fasta")

  #index was still necessary: the "is"-algorithm should be fine; bwtsw would be the other option but seems to only work with humans

  bwa_index = \
      '"{bwa}" index -a is "{ref}" "{}"'.format(
        bwa=bwa_bin, ref=all_genomes, *[tmpfiles[n].name for n in [2, 1, 0]]) # TODO: only [1,0] ? seems to make no difference but still...
  bwa_aln_cmd = \
      '"{bwa}" aln -n 0.04 -t 8 -f "{}" "{ref}" "{}"'.format(
        bwa=bwa_bin, ref=all_genomes, *[tmpfiles[n].name for n in [1, 0]])
  bwa_samse_cmd = \
      '"{bwa}" samse -n 242 -f "{}" "{ref}" "{}" "{}"'.format(
        bwa=bwa_bin, ref=all_genomes, *[tmpfiles[n].name for n in [2, 1, 0]])

  return_code = bwa.run(bwa_index)
  return_code = bwa.run(bwa_aln_cmd)
  return_code = bwa.run(bwa_samse_cmd)

  [t.close() for t in tmpfiles[:2]]
  tmpfiles[2].seek(0) #TODO: ok, but how do we know it's file #2? Perhaps only valid for test example?

  ref_species = [s.rstrip() for s in open(species_ref, 'r').xreadlines()]
  total=[0,0,0,0] # to store the sites
  winner=[]     # to store the most likely species
  resSp_dict={} # to not have to use the tmpfiles[2] for the second and third graph, more convenient that way
  counter=0
  
  # to have a template array (a bunch of zeros) which fills up the array (the one for the graph)
  #     in those places where the species dont have any hits
  templateList = [0 for s in ref_species]
  # one array for each image
#  bigArray = []
#  bigArray1 = []
  bigArray2 = []
  
  i=0
  for s in ref_species:
      speciesID[s] = i
      speciesCount[s] = 0
      i=i+1 
  
  #the last initialisation
  for id, sp_dict in sam_reader(tmpfiles[2]):   
    resSp_dict[id]=sp_dict
  tmpfiles[2].close()
      
  while counter <= 3:
      resSp_dictTemp = resSp_dict.copy() # otherwise one runs into problems of a changing dict size        
      for id in resSp_dict:
        sp_dict = resSp_dict[id]        
        tempList = process_Sites(sp_dict, templateList)
        if counter==0:
            bigArray.append(tempList)
        if counter==1:
            bigArray1.append(tempList)
        if counter==2:
            bigArray2.append(tempList)
        #add together first number of e.g. '2_20585' (id) -> 2 (& convert it from string to int); 29341 entries
        total[counter] = total[counter] + int(id[:id.find('_')])
      winner.append(keywithmaxval(speciesCount))
      for id in resSp_dictTemp: #take away all cites of the 'winner' from last round
      #TODO: '0' in cites (from winner) are also taken out? Where is the difference between NA and 0?
          if resSp_dictTemp[id].has_key(keywithmaxval(speciesCount)):
              del resSp_dict[id]
              # resSp_dict.pop(id, None) # alternative method, but displays every time, not desired
      for s in ref_species:
          speciesCount[s] = 0
      counter = counter + 1

  # convert arrays to numpy.arrays
  arr = numpy.array(bigArray, dtype=numpy.int16)
  arr2 = numpy.array(bigArray1, dtype=numpy.int16)
  arr3 = numpy.array(bigArray2, dtype=numpy.int16)
  
  # plot and show the figures
  fig = plt.figure(1, figsize=(8.27, 11.69), dpi=100)
  img = plt.imshow(arr, interpolation='nearest', extent=(0, 242, 0, 250))
  i=0
  plt.xlabel('Species (of the 242 possibilities): {} has a likelihood of {:.3f}%.'.format(winner[i], (float(total[i]-total[i+1])) / total[0] * 100))
  plt.ylabel('sites (ratio: approx. 1:120; total match: {}, not match: {})'.format(total[i]-total[i+1], total[i+1]))
  plt.title('Species Likelihood Analysis:')
  plt.savefig(outputFile+'.png', bbox_inches='tight', pad_inches=0.2)
  listBackToServer.append(outputFile+'.png')
  fig2 = plt.figure(2, figsize=(8.27, 11.69), dpi=100)
  plt.subplot(211)
  i=1
  img2 = plt.imshow(arr2, interpolation='nearest', extent=(0, 242, 0, 250))
  plt.xlabel('Species: {} has a likelihood of {:.3f}%.'.format(winner[i], (float(total[i]-total[i+1])) / total[0] * 100))
  plt.ylabel('sites (total match: {}, not match: {})'.format(total[i]-total[i+1], total[i+1]))
  plt.subplot(212)
  img3 = plt.imshow(arr3, interpolation='nearest', extent=(0, 242, 0, 250))
  i=2
  plt.xlabel('Species: {} has a likelihood of {:.3f}%.'.format(winner[i], (float(total[i]-total[i+1])) / total[0] * 100))
  plt.ylabel('sites (total match: {}, not match: {})'.format(total[i]-total[i+1], total[i+1]))
  plt.savefig(outputFile+'2.png', bbox_inches='tight', pad_inches=0.2)
  listBackToServer.append(outputFile+'2.png')
  #pylab.show()
  
#  save files as pdf 
  pp = PdfPages('static/'+ output +'.pdf')
  listBackToServer.append('static/'+ output +'.pdf')
  pp.savefig(fig)
  pp.savefig(fig2)
  pp.close()

  # what you need at the end: the three arrays (see above), the 4 totals, the three species
  # the results
  print('The species with the most likelihood are:')
  for i in range(3):
      print('{}.: {}'.format(i+1, winner[i]))
      print('\t total match: {}'.format(total[i]-total[i+1]))
      # TODO: is this correct? How would the percentage likelihood be calculated? just 
      print('\t not match: {}'.format(total[i+1]))
      print("\t percentage match: {:.3f}%".format((float(total[i]-total[i+1])) / total[0] * 100)) # TODO: is this correct?
      # TODO: perhaps a vertical column chart for the percentages on the website?
  return listBackToServer
      
# takes now approx. 30-35 sec, which seems ok...now suddenly 1.5mins...

if __name__ == '__main__':
    main()

# print(fields[0], mms):
# ('2_20585', {'Ursus_spelaeus': 5})
# ('2_20586', {'Ursus_spelaeus': 2})
# ('2_20587', {'Ursus_spelaeus': 2})
# ('2_20589', {'Homo_sapiens_neanderthalensis': 1, 'Homo_sapiens': 1})