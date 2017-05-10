import codecs

STOPWORDS_FILENAME = 'data/stopwords.txt'

stoplist = set([line.strip() for line in codecs.open(STOPWORDS_FILENAME, encoding='utf-8').readlines()])
