import numpy as np
import json
from keras import backend
from keras.layers import Input, merge
from keras.layers.core import Dense, Lambda, Reshape
from keras.layers.convolutional import Convolution1D
from keras.models import Model
import string
import re
import random
import operator
from itertools import izip
from gensim.models.keyedvectors import KeyedVectors

## Here connection is a dict which gives positively related documents id
## {'12' : ['13', '14'], '13' : ['14', '15']}
##
## Pubmed_fetch contains the abstract and tite for a given id i.e
## {'12' : {'title' : 'title of 12', 'abstract' : 'abstract of 12'}}



WINDOW_SIZE = 3 # this is to decide window for words in a sentence (sliding window) See section 3.2
TOTAL_LETTER_GRAMS = 100 # Word Vector Dimension
WORD_DEPTH = WINDOW_SIZE * TOTAL_LETTER_GRAMS # See equation (1).
K = 300 # Dimensionality of the max-pooling layer. See section 3.4.
L = 128 # Dimensionality of latent semantic space. See section 3.5.
J = 4 # Number of Negative Documents
FILTER_LENGTH = 1 # We only consider one time step for convolutions.

# loading the qrels
qrel_path = '/net/work/people/saleh/clir_experiments/resources/new_data_split/data/qrels_dev_train.txt'
with open(qrel_path, 'r') as f:
    data = f.readlines()

for i in range(len(data)):
    data[i] = data[i].strip().split(' ')

connection = {}

for a in data:
    if a[0] in topic_wise.keys():
        connection[a[0]][a[3]].append(a[2])
    else:
        connection[a[0]] = {}
        connection[a[0]]['0'] = []
        connection[a[0]]['1'] = []

to_del = ""
# because there is one file with no +ve
for a in connection:
    if (len(connection[a]['1']) == 0):
        to_del = a

del connection[to_del]

connection_list = []

for a in connection:
    connection_list.append(connection[a])

connection = connection_list

# pubmed_fetch = json.load(open('pubmed_fetch_gens.json'))
# all_keys = list(pubmed_fetch.keys())

# Loading the word embeddings 
def load_emb():
    word_vectors = KeyedVectors.load_word2vec_format('/net/data/cemi/saleh/embeddings/pubmed_s100w10_min.bin', binary=True) 
    return word_vectors

emb = load_emb()

# count = 0
# corpus = set()
# for a in list(pubmed_fetch.keys()):
#     count += 1
#     print count
#     for b in pubmed_fetch[a]['abstract'].lower().split():
#         corpus.add(b)


# for a in corpus:
#     if not a in emb:
#         print (a)

# We keep word vectors for only those words which are in corpus

# emb_keys = emb.keys()
# for a in emb_keys:
#     if not a in corpus:
#         del emb[a]


# So we have emb['word'] equal to vector representation of 'word'


## gives you a numpy.ndarray that is the vector for given sentence
def get_vector(words):
    ## get words in the sentence
    # words = sentence.split()
    output_vec = [] # size will len(words) - 2, and each element will have size of WORD_DEPTH
    sliding_window = [] # size will be WINDOW_SIZE, and each element will have size of TOTAL_LETTER_GRAMS
    for ind in range(len(words)):
        word = words[ind]
        if not word in emb:
            continue
        word_vec = emb[word]
        if (len(sliding_window) < WINDOW_SIZE):
            sliding_window.append(word_vec)
        else:
            sliding_window.append(word_vec)
            temp = sliding_window[0]
            for s in sliding_window[1:]:
                temp = np.concatenate((temp, s))
            output_vec.append(temp)
            del temp
            del sliding_window[0]
    del sliding_window
    return np.array(output_vec)


train_till = 80
## Get random negative doc ids for given pmid
def get_negatives(id):
    output_ids = []
    while (len(output_ids) < J):
        ind = random.randrange(0, train_till)
        if not all_keys[ind] in connection[pmid]:
            output_ids.append(all_keys[ind])
    return output_ids


def R(vects):
    """
    Calculates the cosine similarity of two vectors.
    :param vects: a list of two vectors.
    :return: the cosine similarity of two vectors.
    """
    (x, y) = vects
    return backend.dot(x, backend.transpose(y)) / (x.norm(2) * y.norm(2)) # See equation (4)


query = Input(shape = (None, WORD_DEPTH))
pos_doc = Input(shape = (None, WORD_DEPTH))
neg_docs = [Input(shape = (None, WORD_DEPTH)) for j in range(J)]


doc_conv = Convolution1D(K, FILTER_LENGTH, border_mode = "same", input_shape = (None, WORD_DEPTH), activation = "tanh")
doc_max = Lambda(lambda x: x.max(axis = 1), output_shape = (K, ))
doc_sem = Dense(L, activation = "tanh", input_dim = K)


query_conv = doc_conv(query) # See equation (2).
query_max = doc_max(query_conv) # See section 3.4.
query_sem = doc_sem(query_max) # See section 3.5.

pos_doc_conv = doc_conv(pos_doc)
pos_doc_max = doc_max(pos_doc_conv)
pos_doc_sem = doc_sem(pos_doc_max)

neg_doc_convs = [doc_conv(neg_doc) for neg_doc in neg_docs]
neg_doc_maxes = [doc_max(neg_doc_conv) for neg_doc_conv in neg_doc_convs]
neg_doc_sems = [doc_sem(neg_doc_max) for neg_doc_max in neg_doc_maxes]


# This layer calculates the cosine similarity between the semantic representations of
# a query and a document.
R_layer = Lambda(R, output_shape = (1, )) # See equation (4).

# Returns the final 128 Dimensional vector
def return_repr(vects):
    return vects[0]

repr = Lambda(return_repr, output_shape = (1, 128))
repr_vect = repr([query_sem])

R_Q_D_p = R_layer([query_sem, pos_doc_sem]) # See equation (4).
R_Q_D_ns = [R_layer([query_sem, neg_doc_sem]) for neg_doc_sem in neg_doc_sems] # See equation (4).

concat_Rs = merge([R_Q_D_p] + R_Q_D_ns, mode = "concat")
concat_Rs = Reshape((J + 1, 1))(concat_Rs)

weight = np.array([1]).reshape(1, 1, 1, 1)
with_gamma = Convolution1D(1, 1, border_mode = "same", input_shape = (J + 1, 1), activation = "linear", bias = False, weights = [weight])(concat_Rs) # See equation (5).

exponentiated = Lambda(lambda x: backend.exp(x), output_shape = (J + 1, ))(with_gamma) # See equation (5).
exponentiated = Reshape((J + 1, ))(exponentiated)

prob = Lambda(lambda x: x[0][0] / backend.sum(x[0]), output_shape = (1, ))(exponentiated) # See equation (5).

model = Model(input = [query, pos_doc] + neg_docs, output = prob)
model.compile(optimizer = "adadelta", loss = "binary_crossentropy")

y = np.ones(1)

for ind in range(train_till):
    try:
        print (ind+1, "/", train_till)
        i = all_keys[ind]
        l_Qs = get_vector(pubmed_fetch[i]['abstract'].lower())
        ## For making it compatible with model, we reshape it
        l_Qs = l_Qs.reshape(1, l_Qs.shape[0], l_Qs.shape[1])
        for jind in range(min(len(connection[i]), 6)):
            j = connection[i][jind]
            pos_l_Ds = get_vector(pubmed_fetch[j]['abstract'].lower())
            pos_l_Ds = pos_l_Ds.reshape(1, pos_l_Ds.shape[0], pos_l_Ds.shape[1])
            neg_l_Ds = []
            for a in get_negatives(i):
                temp = get_vector(pubmed_fetch[a]['abstract'].lower())
                neg_l_Ds.append(temp.reshape(1, temp.shape[0], temp.shape[1]))   
            history = model.fit([l_Qs, pos_l_Ds] + neg_l_Ds, y, nb_epoch = 1, verbose = 1)
        ## save evry 1000 iterations
        if (ind % 1000 == 0):
            model.save_weights("model_gens.h5")
            print ("saved")
    except Exception as e:
        print (ind, all_keys[ind], e)
        continue


### TESTING ###


# get_repr = backend.function([query], repr_vect)
# # 128-D representation of the abstracts
# dict_repr = {}

# count = 0
# model.load_weights("model_final.h5")
# for a in pubmed_fetch.keys():
#     count += 1
#     print (count)
#     l_Qs = get_vector(pubmed_fetch[a]['abstract'].lower())
#     l_Qs = l_Qs.reshape(1, l_Qs.shape[0], l_Qs.shape[1])
#     dict_repr[a] = get_repr([l_Qs])

# count = 0
# # Top similar documents
# dict_top = {}
# # Top 100
# dict_top[100] = {}
# for a in all_keys[train_till:]:
#     count += 1
#     print (count)
#     vec1 = dict_repr[a]
#     top_100 = {}
#     for b in dict_repr:
#         if not b == a:
#             val = np.dot(vec1, dict_repr[b])
#             if len(top_100) < 100:
#                 top_100[b] = val
#             else:
#                 m = min(top_100, key=top_100.get)
#                 if (val > top_100[m]):
#                     del top_100[m]
#                     top_100[b] = val
#     dict_top[100][a] = top_100

# count = 0

# for a in [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90]:
#     dict_top[a]= {}

# for a in dict_top[100]:
#     count += 1
#     print (count)
#     for num in [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90]:
#         tmp = sorted(dict_top[100][a].iteritems(), key = operator.itemgetter(1), reverse = True)
#         dict_top[num][a] = dict(tmp[:num])


# for ORDER in [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
#     p_f, p_t, t_f = 0, 0, 0
#     for a in all_keys[train_till:]:
#         count_real = 0
#         for aa in dict_top[ORDER][a]:
#              if aa in connection[a]:
#                 count_real += 1
#         p_f += count_real
#         p_t += min(len(connection[a]), ORDER)
#         t_f += ORDER
#     recall = float(p_f)/p_t
#     precision = float(p_f)/t_f
#     f1 = 2*precision*recall/(precision + recall)
#     print ("ORDER: ", ORDER, recall, precision, f1)