import gensim

# Load Google's pre-trained Word2Vec model.
model = gensim.models.KeyedVectors.load_word2vec_format('PubMed-and-PMC-w2v.bin', binary=True)
model.wv.most_similar(positive=['woman', 'king'], negative=['man'])

print(model)
