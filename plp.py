import codecs

from collections import defaultdict

FORMS_FILENAME = 'data/forms.txt'


class PLP(object):
    def __init__(self):
        self.basic_forms = None
        self.forms = None

    def load(self):
        self.basic_forms = []
        self.forms = defaultdict(list)

        with codecs.open(FORMS_FILENAME, encoding='utf-8') as forms_file:
            lines = forms_file.readlines()
            for line in lines:
                forms = line.split(', ')
                id = len(self.basic_forms)
                basic_form = forms[0]
                self.basic_forms.append(basic_form)

                for form in forms:
                    self.forms[form].append(id)

    def rec(self, word):
        if not self.forms:
            print 'Initializing PLP...'
            self.load()
        return self.forms[word]

    def bform(self, id):
        if not self.basic_forms:
            print 'Initializing PLP...'
            self.load()
        return self.basic_forms[id]
