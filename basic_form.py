# coding=utf-8
from plp import PLP

p = PLP()


def basic_form(word):
    ids = p.rec(word)
    return p.bform(ids[0]) if len(ids) > 0 else word


if __name__ == '__main__':
    print basic_form(u'żółwiem')
    print basic_form(u'bóle')
    print basic_form('abc')
