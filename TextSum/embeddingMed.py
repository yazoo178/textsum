import gensim
import re
# Load Google's pre-trained Word2Vec model.
model = gensim.models.KeyedVectors.load_word2vec_format('PubMed-and-PMC-w2v.bin', binary=True)
model.wv.most_similar(positive=['woman', 'king'], negative=['man'])

wordstoCounts = {}
for word, vocab_obj in model.vocab.items():
    wordstoCounts[word] = vocab_obj.count


file_content = open('stop_words_med', 'w')

for w in sorted(wordstoCounts, key=wordstoCounts.get, reverse=True):
    if re.match('[A-z]+', w):
        file_content.write(w + "\n")

print(wordstoCounts)