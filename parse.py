import gzip
# in the directory /net/data/cemi/CLEF-2015-eHealth/trec

# mypath = '/net/data/cemi/CLEF-2015-eHealth/trec'
# from os import listdir
# from os.path import isfile, join
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# very_files = []

# for a in onlyfiles:
#     if "very_" == a[:len("very_")]:
#         very_files.append(a)

path = '/net/data/cemi/CLEF-2015-eHealth/trec/very_9_small_7_yourh5013_12.trec.gz'

data = ""
with gzip.open(path, 'r') as f:
    data = f.read()


import re
import string
pat = re.compile(b"<DOC>(.*?)</DOC>",re.DOTALL|re.M)
docs=pat.findall(data)
pat_docid = re.compile(b"<DOCID>(.*?)</DOCID>",re.DOTALL|re.M)
pat_doctitle = re.compile(b"<TITLE>(.*?)</TITLE>",re.DOTALL|re.M)
pat_doctext = re.compile(b"<TEXT>(.*?)</TEXT>",re.DOTALL|re.M)

refined_data = []
for a in docs:
    refined_data.append([pat_docid.findall(a)[0], pat_doctext.findall(a)[0], pat_doctitle.findall(a)[0]])

print (len(refined_data))

for i in range(len(refined_data)):
    to_parse = refined_data[i][1]
    to_parse = to_parse.decode('utf-8').lower()
    # Remove punctuation and remove special chars and lower it
    temp = to_parse
    temp = "".join([c for c in temp if c in string.ascii_lowercase or c in string.whitespace or c in string.digits or c in string.punctuation])
    temp = "".join([c for c in temp if not c == '\n'])
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    temp = regex.sub(' ', temp)
    temp = ' '.join(temp.split())
    no_integers = [x for x in temp.split(' ') if not x.isdigit()]
    no_one_letter = [x for x in no_integers if not len(x) == 1]
    refined_data[i][1] = no_one_letter

print (refined_data[0][1])

from gensim.models.keyedvectors import KeyedVectors
word_vectors = KeyedVectors.load_word2vec_format('/net/data/cemi/saleh/embeddings/pubmed_s100w10_min.bin', binary=True) 

sum_tot = 0
sum_not_pre = 0
for b in refined_data:
    c = b[1]
    total = len(c)
    not_pre = 0
    for a in c:
        if not a in word_vectors.vocab:
            print (a)
            not_pre += 1
    print (not_pre, "/", total)
    sum_tot += total
    sum_not_pre += not_pre

print ("----", sum_not_pre, "/", sum_tot)

#TODO : remove stopwords

# count = 0
# total = 0
# for a in refined_data:
#     if (a[2] == refined_data[0][2]):
#         count +=1
#     total += 1

# for path = 'very_4_small_0_mdbri3590_12.trec.gz' count = 207 total = 235
# So the file name contains info about the underlying content: 