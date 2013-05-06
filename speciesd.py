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
import operator

from bwa import BWA

# never used, or is it?
# def items_sorted_by_value(dictionary, reverse=False):
#   for item in sorted(dictionary.iteritems(),
#                      itemgetter(1),
#                      reverse=reverse):
#     yield item

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

  #index was still necessary: the "is"-algorithm should be fine; bwtsw would be the other option but seems to only work with humans

  bwa_index = \
      '"{bwa}" index -a is "{ref}" "{}"'.format(
        bwa=bwa_bin, ref=all_genomes, *[tmpfiles[n].name for n in [1, 0]])
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
  tmpfiles[2].seek(0) #ok, but how do we know it's file #2? Perhaps only valid for test example?

  ref_species = [s.rstrip() for s in open(species_ref, 'r').xreadlines()]
  # arr=numpy.array([0,0,0,0])
  
  stats={}
  for id, sp_dict in sam_reader(tmpfiles[2]):
    for i in sp_dict:
      stats[i] = 0
  tmpfiles[2].seek(0)
  for id, sp_dict in sam_reader(tmpfiles[2]):
    for i in sp_dict:
      stats[i] = stats[i] + sp_dict[i]
  stats_sorted = sorted(stats.iteritems(), key=operator.itemgetter(1))
  # best: 
  # stats_sorted[-1:][0][0] # 'Ursus_spelaeus'
  print( stats_sorted)
        

  # for id, sp_dict in sam_reader(tmpfiles[2]):
  #   try:
  #     # arrayTest.append(s in sp_dict and sp_dict[s] or -1 for s in ref_species)
  #     numpy.vstack((arr, [s in sp_dict and sp_dict[s] or -1 for s in ref_species])) #all and last
  #     # print("Array 1: ")
  #     # print(arr)
  #   except NameError:
  #     print("NameError")
  #     arr = numpy.array([s in sp_dict and sp_dict[s] or -1 for s in ref_species], dtype=numpy.int16) #one line
  #     # print("Array 2: ")
  #     # print(arr)

  # img = matplotlib.pyplot.imshow(arr, interpolation='nearest', extent=(0, 1, 0, 1))
  # pylab.show()

# example Array
# Array 1: 
# [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
#  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
#  -1, -1, -1, -1, -1, -1, -1, -1,  1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
#  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  1,  1, -1, -1, -1, -1, -1, -1, -1, -1,
#  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  1,  1, -1,  1, -1,
#  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
#  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  1, -1, -1, -1,  1, -1, -1, -1, -1,
#  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
#  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
#  -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

# print(fields[0], mms):
# ('2_20585', {'Ursus_spelaeus': 5})
# ('2_20586', {'Ursus_spelaeus': 2})
# ('2_20587', {'Ursus_spelaeus': 2})
# ('2_20589', {'Homo_sapiens_neanderthalensis': 1, 'Homo_sapiens': 1})
# ('2_20591', {'Ursus_spelaeus': 2})
# ('2_20592', {'Ursus_spelaeus': 3})
# ('2_20593', {'Ursus_spelaeus': 1})
# ('2_20594', {'Naemorhedus_swinhoei': 1, 'Pantholops_hodgsonii': 1, 'Ovis_aries': 1, 'Bos_indicus': 1, 'Melursus_ursinus': 1, 'Elaphodus_cephalophus': 1, 'Lama_guanicoe': 1, 'Muntiacus_reevesi_micrurus': 1, 'Episoriculus_fumidus': 1, 'Lama_pacos': 1, 'Giraffa_camelopardalis_angolensis': 1, 'Phoca_fasciata': 1, 'Canis_lupus': 1, 'Antilope_cervicapra': 1, 'Cervus_nippon_taiouanus': 1, 'Rangifer_tarandus': 1, 'Ursus_spelaeus': 1, 'Lama_glama': 1, 'Muntiacus_muntjak': 1, 'Capra_hircus': 1, 'Mirounga_leonina': 1, 'Bos_taurus': 1, 'Canis_lupus_lupus': 1, 'Cervus_unicolor_swinhoei': 1, 'Canis_lupus_chanco': 1, 'Monachus_schauinslandi': 1, 'Canis_lupus_laniger': 1, 'Camelus_dromedarius': 1, 'Bubalus_bubalis': 1, 'Cervus_elaphus': 1, 'Canis_lupus_familiaris': 1, 'Capricornis_crispus': 1, 'Bison_bison': 1})
# ('2_20595', {'Ursus_maritimus': 2, 'Ursus_spelaeus': 1})
# ('2_20596', {'Arctodus_simus': 3, 'Ursus_maritimus': 3, 'Ursus_spelaeus': 2})
# ('2_20597', {'Ursus_spelaeus': 2})
# ('2_20600', {'Ursus_maritimus': 2, 'Ailurus_fulgens': 2, 'Panthera_tigris': 3, 'Helarctos_malayanus': 3, 'Arctodus_simus': 2, 'Ursus_americanus': 2, 'Ursus_thibetanus_ussuricus': 3, 'Ursus_thibetanus_mupinensis': 3, 'Ursus_thibetanus_thibetanus': 3, 'Ailurus_fulgens_styani': 2, 'Ursus_spelaeus': 2, 'Ursus_thibetanus': 3, 'Ursus_arctos': 3, 'Spilogale_putorius': 2, 'Tremarctos_ornatus': 3, 'Acinonyx_jubatus': 3, 'Ursus_thibetanus_formosanus': 3})
# ('2_20601', {'Ursus_spelaeus': 3})
# ('2_20602', {'Ursus_thibetanus_mupinensis': 3, 'Helarctos_malayanus': 3, 'Ursus_maritimus': 2, 'Ursus_spelaeus': 2, 'Ursus_arctos': 3})
# ('2_20603', {'Homo_sapiens_neanderthalensis': 2, 'Homo_sapiens': 1})
# ('2_20605', {'Ursus_spelaeus': 1})
# ('2_20606', {'Ursus_spelaeus': 2})
# ('2_20607', {'Ursus_spelaeus': 4})
# ('2_20609', {'Phoca_vitulina': 1, 'Arctodus_simus': 1, 'Phoca_fasciata': 1, 'Ursus_thibetanus_mupinensis': 1, 'Vulpes_vulpes': 1, 'Melursus_ursinus': 1, 'Phoca_groenlandica': 1, 'Phoca_caspica': 1, 'Ursus_maritimus': 1, 'Ursus_thibetanus_formosanus': 1, 'Phoca_hispida': 1, 'Arctocephalus_forsteri': 1, 'Ursus_thibetanus_thibetanus': 1, 'Ursus_spelaeus': 0, 'Erignathus_barbatus': 1, 'Callorhinus_ursinus': 1, 'Spilogale_putorius': 1, 'Canis_lupus_chanco': 1, 'Ailurus_fulgens_styani': 1, 'Neophoca_cinerea': 1, 'Arctocephalus_townsendi': 1, 'Helarctos_malayanus': 1, 'Ursus_americanus': 1, 'Zalophus_californianus': 1, 'Ailuropoda_melanoleuca': 1, 'Canis_latrans': 1, 'Ursus_arctos': 1, 'Ailurus_fulgens': 1, 'Arctocephalus_pusillus': 1, 'Eumetopias_jubatus': 1, 'Phoca_largha': 1, 'Canis_lupus_lupus': 1, 'Pongo_pygmaeus': 1, 'Canis_lupus': 1, 'Phoca_sibirica': 1, 'Canis_lupus_laniger': 1, 'Halichoerus_grypus': 1, 'Hyperoodon_ampullatus': 1, 'Canis_lupus_familiaris': 1, 'Phocarctos_hookeri': 1, 'Ursus_thibetanus': 1, 'Berardius_bairdii': 1})

# [('Dasypus_novemcinctus', 1), ('Hylomys_suillus', 2), ('Mammut_americanum', 2), ('Tamandua_tetradactyla', 4), ('Dendrohyrax_dorsalis', 5), ('Cervus_nippon_centralis', 5), ('Cervus_nippon_yesoensis', 8), ('Jaculus_jaculus', 9), ('Muntiacus_reevesi', 9), ('Cynocephalus_variegatus', 10), ('Orycteropus_afer', 10), ('Pipistrellus_abramus', 11), ('Cebus_albifrons', 12), ('Bradypus_tridactylus', 13), ('Muntiacus_crinifrons', 13), ('Nannospalax_ehrenbergi', 14), ('Eulemur_mongoz', 14), ('Echinosorex_gymnura', 15), ('Cervus_nippon_yakushimae', 15), ('Lemur_catta', 16), ('Papio_hamadryas', 16), ('Mus_musculus', 16), ('Mus_musculus_domesticus', 16), ('Pecari_tajacu', 17), ('Sus_scrofa_domestica', 18), ('Sus_scrofa', 18), ('Lipotes_vexillifer', 21), ('Microtus_kikuchii', 23), ('Mus_musculus_castaneus', 24), ('Hemiechinus_auritus', 25), ('Rattus_exulans', 27), ('Rattus_norvegicus_strain_BN/SsNHsdMCW', 28), ('Nasalis_larvatus', 28), ('Phacochoerus_africanus', 28), ('Rattus_praetor', 29), ('Microtus_rossiaemeridionalis', 30), ('Balaenoptera_omurai', 32), ('Hydropotes_inermis', 33), ('Crocidura_russula', 37), ('Diceros_bicornis', 37), ('Thryonomys_swinderianus', 37), ('Sciurus_vulgaris', 37), ('Ceratotherium_simum', 37), ('Daubentonia_madagascariensis', 38), ('Choloepus_didactylus', 38), ('Balaenoptera_borealis', 39), ('Equus_asinus', 39), ('Mus_musculus_molossinus', 42), ('Mus_musculus_musculus', 42), ('Phocoena_phocoena', 43), ('Mus_terricolor', 44), ('Rhinolophus_pumilus', 47), ('Rhinolophus_monoceros', 47), ('Equus_caballus', 48), ('Balaenoptera_edeni', 49), ('Elephantulus_sp._VB001', 51), ('Tarsius_bancanus', 53), ('Ochotona_princeps', 54), ('Anomalurus_sp._GP-2005', 56), ('Rhinoceros_sondaicus', 56), ('Chlorocebus_sabaeus', 57), ('Chlorocebus_tantalus', 59), ('Chlorocebus_pygerythrus', 59), ('Chlorocebus_aethiops', 59), ('Rhinoceros_unicornis', 61), ('Hippopotamus_amphibius', 62), ('Echinops_telfairi', 64), ('Rattus_rattus', 66), ('Myoxus_glis', 67), ('Cricetulus_griseus', 68), ('Trachypithecus_obscurus', 70), ('Pygathrix_roxellana', 71), ('Trichechus_manatus', 72), ('Dugong_dugon', 72), ('Oryctolagus_cuniculus', 73), ('Macroscelides_proboscideus', 73), ('Eremitalpa_granti', 73), ('Procavia_capensis', 76), ('Propithecus_coquereli', 77), ('Inia_geoffrensis', 77), ('Pygathrix_nemaeus', 78), ('Semnopithecus_entellus', 78), ('Megaptera_novaeangliae', 79), ('Presbytis_melalophos', 79), ('Cavia_porcellus', 79), ('Macaca_sylvanus', 80), ('Manis_tetradactyla', 82), ('Tupaia_belangeri', 82), ('Eschrichtius_robustus', 83), ('Nycticebus_coucang', 84), ('Rhinolophus_formosae', 88), ('Hylobates_lar', 95), ('Chrysochloris_asiatica', 96), ('Rattus_tanezumi', 98), ('Ammotragus_lervia', 99), ('Chalinolobus_tuberculatus', 102), ('Camelus_bactrianus_ferus', 103), ('Camelus_bactrianus', 103), ('Lepus_europaeus', 105), ('Sorex_unguiculatus', 111), ('Pteropus_scapulatus', 113), ('Mystacina_tuberculata', 114), ('Rousettus_aegyptiacus', 116), ('Ochotona_collaris', 121), ('Ochotona_curzoniae', 142), ('Macaca_fascicularis', 142), ('Bos_grunniens', 151), ('Macaca_thibetana', 152), ('Urotrichus_talpoides', 154), ('Macaca_mulatta', 160), ('Meles_meles_anakuma', 174), ('Pteropus_dasymallus', 185), ('Mogera_wogura', 187), ('Stenella_coeruleoalba', 197), ('Delphinus_capensis', 197), ('Stenella_attenuata', 197), ('Phoca_sibirica', 198), ('Caperea_marginata', 199), ('Monodon_monoceros', 200), ('Sousa_chinensis', 200), ('Dicerorhinus_sumatrensis', 201), ('Physeter_catodon', 206), ('Kogia_breviceps', 209), ('Colobus_guereza', 210), ('Lagenorhynchus_albirostris', 213), ('Tursiops_truncatus', 216), ('Balaenoptera_musculus', 217), ('Grampus_griseus', 218), ('Panthera_pardus', 220), ('Eubalaena_australis', 221), ('Balaenoptera_brydei', 221), ('Cervus_unicolor_swinhoei', 222), ('Eubalaena_japonica', 224), ('Pongo_pygmaeus', 224), ('Berardius_bairdii', 224), ('Cervus_nippon_taiouanus', 224), ('Cervus_elaphus', 224), ('Muntiacus_reevesi_micrurus', 226), ('Elaphodus_cephalophus', 227), ('Balaenoptera_physalus', 228), ('Pantholops_hodgsonii', 231), ('Naemorhedus_swinhoei', 232), ('Coelodonta_antiquitatis', 234), ('Antilope_cervicapra', 247), ('Vulpes_vulpes', 248), ('Bubalus_bubalis', 248), ('Herpestes_javanicus', 249), ('Pontoporia_blainvillei', 254), ('Neofelis_nebulosa', 255), ('Platanista_minor', 257), ('Felis_catus', 257), ('Phoca_groenlandica', 260), ('Giraffa_camelopardalis_angolensis', 265), ('Rangifer_tarandus', 267), ('Balaena_mysticetus', 269), ('Hyperoodon_ampullatus', 269), ('Procolobus_badius', 273), ('Uncia_uncia', 277), ('Tursiops_aduncus', 278), ('Canis_latrans', 290), ('Galemys_pyrenaicus', 306), ('Ovis_aries', 306), ('Camelus_dromedarius', 307), ('Gorilla_gorilla_gorilla', 309), ('Artibeus_jamaicensis', 345), ('Erinaceus_europaeus', 357), ('Odobenus_rosmarus_rosmarus', 363), ('Phoca_hispida', 370), ('Muntiacus_muntjak', 391), ('Talpa_europaea', 402), ('Bos_indicus', 412), ('Eumetopias_jubatus', 412), ('Bos_taurus', 412), ('Capricornis_crispus', 416), ('Bison_bison', 422), ('Balaenoptera_acutorostrata', 422), ('Balaenoptera_bonaerensis', 423), ('Pongo_abelii', 426), ('Lutra_lutra', 431), ('Gulo_gulo', 435), ('Phoca_caspica', 437), ('Gorilla_gorilla', 455), ('Lama_pacos', 467), ('Callorhinus_ursinus', 470), ('Lama_guanicoe', 476), ('Lama_glama', 478), ('Capra_hircus', 483), ('Pan_troglodytes', 488), ('Enhydra_lutris', 504), ('Meles_meles', 505), ('Episoriculus_fumidus', 536), ('Martes_melampus', 562), ('Pan_paniscus', 575), ('Halichoerus_grypus', 587), ('Arctocephalus_pusillus', 590), ('Erignathus_barbatus', 625), ('Martes_flavigula', 627), ('Canis_lupus_laniger', 630), ('Panthera_tigris', 631), ('Cystophora_cristata', 632), ('Canis_lupus', 633), ('Canis_lupus_familiaris', 633), ('Canis_lupus_lupus', 633), ('Canis_lupus_chanco', 634), ('Acinonyx_jubatus', 674), ('Arctocephalus_forsteri', 739), ('Phoca_fasciata', 803), ('Arctocephalus_townsendi', 854), ('Neophoca_cinerea', 906), ('Phoca_vitulina', 970), ('Phoca_largha', 993), ('Ailurus_fulgens', 1001), ('Ailurus_fulgens_styani', 1002), ('Martes_zibellina', 1028), ('Mirounga_leonina', 1089), ('Monachus_schauinslandi', 1123), ('Procyon_lotor', 1166), ('Zalophus_californianus', 1178), ('Leptonychotes_weddellii', 1205), ('Hydrurga_leptonyx', 1325), ('Phocarctos_hookeri', 1380), ('Homo_sapiens', 1587), ('Spilogale_putorius', 1596), ('Lobodon_carcinophaga', 1623), ('Ailuropoda_melanoleuca', 1764), ('Melursus_ursinus', 1794), ('Homo_sapiens_neanderthalensis', 1890), ('Tremarctos_ornatus', 2175), ('Ursus_thibetanus_thibetanus', 3990), ('Arctodus_simus', 4678), ('Ursus_thibetanus_formosanus', 4679), ('Ursus_americanus', 5190), ('Helarctos_malayanus', 6247), ('Ursus_thibetanus_ussuricus', 7374), ('Ursus_arctos', 7395), ('Ursus_thibetanus', 7843), ('Ursus_maritimus', 8266), ('Ursus_thibetanus_mupinensis', 8850), ('Ursus_spelaeus', 29779)]
