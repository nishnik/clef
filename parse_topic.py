import re
import gzip
# in the directory /net/work/people/saleh/clir_experiments/resources/new_data_split/
path = '/net/work/people/saleh/clir_experiments/resources/new_data_split/en.dev_train'
data = ""
with open(path, 'r') as f:
    data = f.read()

pat = re.compile("<topic>(.*?)</topic>",re.DOTALL|re.M)
topics=pat.findall(data)
pat_topicid = re.compile("<id>(.*?)</id>",re.DOTALL|re.M)
pat_topictitle = re.compile("<title>(.*?)</title>",re.DOTALL|re.M)
import string
topic_dict = {}
for a in topics:
    temp = pat_topictitle.findall(a)[0].lower()
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    temp = regex.sub(' ', temp)    
    topic_dict[pat_topicid.findall(a)[0]] = temp.split()

from gensim.models.keyedvectors import KeyedVectors
word_vectors = KeyedVectors.load_word2vec_format('/net/data/cemi/saleh/embeddings/pubmed_s100w10_min.bin', binary=True) 


count = 0
tot = 0

for a in topic_dict:
    for b in topic_dict[a]:
        if b .lower()not in word_vectors.vocab:
            print (b, a)
            count += 1
        tot += 1


"""
We have following topic ids:
qtest2013.1
qtest2013.2
qtest2013.4
qtest2013.5
qtest2013.6
qtest2013.9
qtest2013.10
qtest2013.13
qtest2013.14
qtest2013.15
qtest2013.16
qtest2013.18
qtest2013.20
qtest2013.22
qtest2013.23
qtest2013.24
qtest2013.25
qtest2013.26
qtest2013.27
qtest2013.28
qtest2013.31
qtest2013.33
qtest2013.34
qtest2013.35
qtest2013.36
qtest2013.37
qtest2013.39
qtest2013.40
qtest2013.42
qtest2013.43
qtest2013.44
qtest2013.46
qtest2013.49
qtest2014.2
qtest2014.3
qtest2014.4
qtest2014.5
qtest2014.7
qtest2014.8
qtest2014.10
qtest2014.11
qtest2014.12
qtest2014.14
qtest2014.15
qtest2014.17
qtest2014.22
qtest2014.23
qtest2014.26
qtest2014.27
qtest2014.28
qtest2014.29
qtest2014.33
qtest2014.34
qtest2014.35
qtest2014.36
qtest2014.37
qtest2014.38
qtest2014.39
qtest2014.40
qtest2014.44
qtest2014.45
qtest2014.46
qtest2014.47
qtest2014.48
qtest2014.49
clef2015.test.1
clef2015.test.2
clef2015.test.4
clef2015.test.5
clef2015.test.6
clef2015.test.7
clef2015.test.8
clef2015.test.13
clef2015.test.14
clef2015.test.15
clef2015.test.19
clef2015.test.22
clef2015.test.25
clef2015.test.27
clef2015.test.28
clef2015.test.30
clef2015.test.31
clef2015.test.36
clef2015.test.38
clef2015.test.39
clef2015.test.42
clef2015.test.44
clef2015.test.46
clef2015.test.47
clef2015.test.48
clef2015.test.49
clef2015.test.51
clef2015.test.53
clef2015.test.54
clef2015.test.56
clef2015.test.58
clef2015.test.59
clef2015.test.64
clef2015.test.66
clef2015.test.67
"""