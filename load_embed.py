from gensim.models.keyedvectors import KeyedVectors
word_vectors = KeyedVectors.load_word2vec_format('/net/data/cemi/saleh/embeddings/pubmed_s100w10_min.bin', binary=True) 
print (len(word_vectors[list(word_vectors.vocab)[0]]))