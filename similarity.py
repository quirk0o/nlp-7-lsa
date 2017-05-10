# coding=utf-8
import logging
import os

from gensim import corpora, models, similarities

from preprocessor import clean
from stoplist import stoplist

from corpus import Corpus

CORPUS_CACHE_FILENAME = 'cache/corpus.mm'
DICTIONARY_CACHE_FILENAME = 'cache/pap.dict'
TFIDF_CACHE_FILENAME = 'cache/model.tfidf'
LSI_CACHE_FILENAME = 'cache/model_{}.lsi'
INDEX_CACHE_FILENAME = 'cache/pap_{}.index'

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Similarity(object):
    def __init__(self, k):
        self.k = k
        self.load_dictionary()
        self.load_mmcorpus()
        self.load_tfidf()
        self.load_lsi()
        self.load_index()

    def load_index(self):
        index_cache_filename = INDEX_CACHE_FILENAME.format(k)

        if os.path.isfile(index_cache_filename):
            self.index = similarities.MatrixSimilarity.load(index_cache_filename)
        else:
            index = similarities.MatrixSimilarity(self.corpus_lsi, num_features=self.k)
            index.save(index_cache_filename)
            self.index = index

    def load_lsi(self):
        lsi_cache_filename = LSI_CACHE_FILENAME.format(k)
        if os.path.isfile(lsi_cache_filename):
            lsi = models.LsiModel.load(lsi_cache_filename)
            corpus_lsi = lsi[self.corpus_tfidf]
        else:
            lsi = models.LsiModel(self.corpus_tfidf, id2word=self.dictionary, num_topics=self.k)
            corpus_lsi = lsi[self.corpus_tfidf]
            lsi.save(lsi_cache_filename)

        self.lsi = lsi
        self.corpus_lsi = corpus_lsi

    def load_tfidf(self):
        if os.path.isfile(TFIDF_CACHE_FILENAME):
            tfidf = models.TfidfModel.load(TFIDF_CACHE_FILENAME)
            corpus_tfidf = tfidf[self.corpus]
        else:
            tfidf = models.TfidfModel(self.corpus)
            corpus_tfidf = tfidf[self.corpus]
            tfidf.save(TFIDF_CACHE_FILENAME)
        self.tfidf = tfidf
        self.corpus_tfidf = corpus_tfidf

    def load_mmcorpus(self):
        if os.path.isfile(CORPUS_CACHE_FILENAME):
            corpus = corpora.MmCorpus(CORPUS_CACHE_FILENAME)
        else:
            corpus = [self.dictionary.doc2bow(doc) for doc in Corpus()]
            corpora.MmCorpus.serialize(CORPUS_CACHE_FILENAME, corpus)
        self.corpus = corpus

    def load_dictionary(self):
        if os.path.isfile(DICTIONARY_CACHE_FILENAME):
            dictionary = corpora.Dictionary.load(DICTIONARY_CACHE_FILENAME)
        else:
            dictionary = corpora.Dictionary(doc for doc in Corpus())
            stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
            dictionary.filter_tokens(stop_ids)
            dictionary.filter_extremes(no_below=2, no_above=0.7)
            dictionary.compactify()
        self.dictionary = dictionary

    def similarity(self, doc):
        vec_bow = self.dictionary.doc2bow(clean(doc))
        vec_tfidf = self.tfidf[vec_bow]
        vec_lsi = self.lsi[vec_tfidf]

        sims = self.index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        return sims


if __name__ == '__main__':

    k = 200

    sim = Similarity(k)

    doc = Corpus().get(1403)

    print doc

    sims = sim.similarity(doc)

    for id, sim in sims[:20]:
        print sim
        print Corpus().get(id)
