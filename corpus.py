import codecs

import re

from basic_form import basic_form
from preprocessor import clean

CORPUS_FILENAME = 'data/pap.txt'
DOCUMENT_SEP = '#\d+'


class Corpus(object):
    def __init__(self):
        self.__documents = None

    def __load_documents(self):
        with codecs.open(CORPUS_FILENAME, encoding='utf-8') as corpus_file:
            documents = re.split(DOCUMENT_SEP, corpus_file.read())
            self.__documents = documents

    def get(self, key):
        if self.__documents is None:
            self.__load_documents()
            return self.__documents[key]

    def all_ids(self):
        if self.__documents is None:
            self.__load_documents()
        return range(0, len(self.__documents))

    def __iter__(self):
        with codecs.open(CORPUS_FILENAME, encoding='utf-8') as corpus_file:
            text = ''
            for line in corpus_file:
                if re.match(DOCUMENT_SEP, line):
                    yield self.transform_text(text), text
                    text = ''
                else:
                    text = text + line

            yield self.transform_text(text), text

    def transform_text(self, doc):
        return [basic_form(word) for word in clean(doc)]


if __name__ == '__main__':
    for text in Corpus():
        print text

