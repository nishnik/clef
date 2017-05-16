from os import listdir
from os.path import isfile, join

######## for data dir
mypath = "data/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
import json
all_keys = []
for a in onlyfiles:
    with open("data/"+a) as data_file:    
        data = json.load(data_file)
        all_keys += list(data.keys())

all_keys = sorted(all_keys)
f = open("data_keys",'w')
f.write(str(all_keys))
f.close()

###### for clef dir
import gzip
import re
def parse_file(path):
    data = ""
    with gzip.open(path, 'r') as f:
        data = f.read()
    pat = re.compile(b"<DOC>(.*?)</DOC>",re.DOTALL|re.M)
    docs=pat.findall(data)
    pat_docid = re.compile(b"<DOCID>(.*?)</DOCID>",re.DOTALL|re.M)
    pat_doctitle = re.compile(b"<TITLE>(.*?)</TITLE>",re.DOTALL|re.M)
    pat_doctext = re.compile(b"<TEXT>(.*?)</TEXT>",re.DOTALL|re.M)
    refined_data = []
    for a in docs:
        refined_data.append(pat_docid.findall(a)[0].decode('utf-8'))
    return refined_data

mypath = '/net/data/cemi/CLEF-2015-eHealth/trec'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
clef_keys = []
for a in onlyfiles:
    try:
        clef_keys += parse_file(mypath+"/"+a)
    except Exception as e:
        print (e, a)
        continue

clef_keys = sorted(clef_keys)
f = open("clef_keys",'w')
f.write(str(clef_keys))
f.close()




# f = open("data_keys", 'r')
# str_Data = f.read()
# all_keys = eval(str_Data)
# # len(all_keys)
# # 1096879

# f = open("clef_keys", 'r')
# str_Data = f.read()
# got_keys = eval(str_Data)
# # len(got_keys)
# # 1096879

# all_keys = set(all_keys)
# got_keys = set(got_keys)
# all_keys - got_keys
# # set()
# got_keys - all_keys
# # set()

