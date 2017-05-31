import gzip
import re
import string
import json
# in the directory /net/data/cemi/CLEF-2015-eHealth/trec

mypath = '/home/nikhil/data'
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

mini_very_files_small = []
small_files = []
for a in onlyfiles:
    if "mini_very" == a[:len("mini_very")]:
        mini_very_files_small.append(a)
    elif "small_" == a[:len("small_")]:
        small_files.append(a)

mini_very_files_small = sorted(mini_very_files_small)
small_very_files = sorted(small_files)


for a in mini_very_files_small:
    dict_1 = {}
    with open(a[-12:]) as data_file:    
        dict_1 = json.load(data_file)
    dict_2 = {}
    with open(a) as data_file:    
        dict_2 = json.load(data_file)
    z = dict_1.copy()
    z.update(dict_2)
    with open(a[-12:], 'w') as outfile:
         json.dump(z, outfile, sort_keys = True, indent = 4,
                   ensure_ascii = False)



for a in small_very_files:
    dict_1 = {}
    with open(a[-12:]) as data_file:    
        dict_1 = json.load(data_file)
    dict_2 = {}
    with open(a) as data_file:    
        dict_2 = json.load(data_file)
    z = dict_1.copy()
    z.update(dict_2)
    with open(a[-12:], 'w') as outfile:
         json.dump(z, outfile, sort_keys = True, indent = 4,
                   ensure_ascii = False)


# from gensim.models.keyedvectors import KeyedVectors
# word_vectors = KeyedVectors.load_word2vec_format('/net/data/cemi/saleh/embeddings/pubmed_s100w10_min.bin', binary=True) 

# sum_tot = 0
# sum_not_pre = 0
# for b in refined_data:
#     c = b[1]
#     total = len(c)
#     not_pre = 0
#     for a in c:
#         if not a in word_vectors.vocab:
#             print (a)
#             not_pre += 1
#     print (not_pre, "/", total)
#     sum_tot += total
#     sum_not_pre += not_pre

# print ("----", sum_not_pre, "/", sum_tot)

#TODO : remove stopwords

# count = 0
# total = 0
# for a in refined_data:
#     if (a[2] == refined_data[0][2]):
#         count +=1
#     total += 1

# for path = 'very_4_small_0_mdbri3590_12.trec.gz' count = 207 total = 235
# So the file name contains info about the underlying content: 