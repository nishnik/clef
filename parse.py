from bs4 import BeautifulSoup
import gzip
# in the directory /net/data/cemi/CLEF-2015-eHealth/trec
path = 'very_6_small_2_n-con1376_12.trec.gz' # most of the data is same
data = ""
with gzip.open(path, 'r') as f:
    data = f.read()

source = BeautifulSoup(data, "html5lib")
docs = source.find('html').find('body').find('docs').findAll('doc')
refined_data = []
for a in docs:
    refined_data.append([a.docid.text, a.title.text, a.find('text').text])

count = 0
total = 0
for a in refined_data:
    if (a[2] == refined_data[0][2]):
        count +=1
    total += 1

# for path = 'very_4_small_0_mdbri3590_12.trec.gz' count = 207 total = 235
