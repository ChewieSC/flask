#!/usr/bin/env python

from math import log
from operator import itemgetter
from tempfile import NamedTemporaryFile

from ConfigParser import SafeConfigParser

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import numpy

import matplotlib.pyplot
import pylab
import pdb

from bwa import BWA


def items_sorted_by_value(dictionary, reverse=False):
  for item in sorted(dictionary.iteritems(),
                     itemgetter(1),
                     reverse=reverse):
    yield item

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


if __name__ == '__main__':

  config = SafeConfigParser()
  config.read(['speciesd.cfg'])

  bwa_bin = config.get("files", "bwa_bin")
  bwa = BWA(bwa_bin)
  tmpdir = config.get("files", "tmpdir")
  all_genomes = config.get("files", "all_genomes")
  species_ref = config.get("files", "species_ref")

  db = {}

  with open("data/cavebear.txt", 'r') as ifh:
    for record in SeqIO.parse(ifh, "fastq"):
      s = str(record.seq)
      db[s] = db.get(s, 0) + 1

  for s in db.keys():
    if not seqfilter(s, length=35, cutoff=2, complexity_cutoff=1.2):
      del(db[s])

  tmpfiles = [NamedTemporaryFile(dir=tmpdir, prefix="tmp{}_".format(n))
              for n in range(3)]

  SeqIO.write(create_fasta_records(db), tmpfiles[0], "fasta")

  bwa_aln_cmd = \
      '"{bwa}" aln -n 0.04 -t 8 -f "{}" "{ref}" "{}"'.format(
        bwa=bwa_bin, ref=all_genomes, *[tmpfiles[n].name for n in [1, 0]])
  bwa_samse_cmd = \
      '"{bwa}" samse -n 242 -f "{}" "{ref}" "{}" "{}"'.format(
        bwa=bwa_bin, ref=all_genomes, *[tmpfiles[n].name for n in [2, 1, 0]])

  return_code = bwa.run(bwa_aln_cmd)
  return_code = bwa.run(bwa_samse_cmd)

  [t.close() for t in tmpfiles[:2]]
  tmpfiles[2].seek(0)

  ref_species = [s.rstrip() for s in open(species_ref, 'r').xreadlines()]
  arr=numpy.array([])

  for id, sp_dict in sam_reader(tmpfiles[2]):
    try:
      # arrayTest.append(s in sp_dict and sp_dict[s] or -1 for s in ref_species)
      numpy.vstack((arr, [s in sp_dict and sp_dict[s] or -1 for s in ref_species])) #all and last
      print(arr)
    except NameError:
      print("NameError")
      arr = numpy.array([s in sp_dict and sp_dict[s] or -1 for s in ref_species], dtype=numpy.int16) #one line
      print(arr)

  img = matplotlib.pyplot.imshow(arr, interpolation='nearest', extent=(0, 1, 0, 1))
  pylab.show()

