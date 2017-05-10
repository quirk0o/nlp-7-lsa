import sys

from similarity import Similarity


class StatisticsService(object):
    def __init__(self, all_samples=None, classification=None, guesses=None):
        self.all_samples = all_samples
        self.classification = classification
        self.guesses = guesses

    def true_positives(self):
        return [x for x in self.guesses if x in self.classification]

    def true_negatives(self):
        return [x for x in self.all_samples if x not in self.guesses and x not in self.classification]

    def precision(self):
        all_positives = len(self.guesses)
        if all_positives == 0:
            return 0
        return float(len(self.true_positives())) / float(all_positives)

    def recall(self):
        return float(len(self.true_positives())) / len(self.classification)

    def f1(self):
        p = self.precision()
        r = self.recall()
        return 2 * p * r / (p + r)

    def accuracy(self):
        return float(len(self.true_positives() + self.true_negatives())) / len(self.all_samples)


if __name__ == '__main__':
    id = int(sys.argv[1])
    sample_filename = 'samples/{}'.format(id)
    classification = [int(id) for id in open(sample_filename).readlines()]

    k = 200

    sim = Similarity(k)
    corpus = sim.corpus
    doc = corpus.get(1403)

    print doc

    sims = sim.similarity(doc)

    for id, sim in sims[:20]:
        print sim
        print corpus.get(id)

    all_ids = corpus.all_ids()

    stats = StatisticsService(all_samples=all_ids, classification=classification, guesses=sims[:20])
    print 'Precision: {}'.format(stats.precision())
    print 'Recall: {}'.format(stats.recall())
    print 'F1: {}'.format(stats.f1())
    print 'Accuracy: {}'.format(stats.accuracy())

