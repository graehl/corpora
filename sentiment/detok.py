#!/usr/bin/env python

#import revtok
import sys
import nltk
import nltk.tokenize

from nltk.tokenize.treebank import TreebankWordTokenizer, TreebankWordDetokenizer

revtok = TreebankWordDetokenizer()

def detok(x):
    return revtok.detokenize(x)
#    return revtok.detokenize(x)


for l in sys.stdin:
    fields = l.split('\t')
    print('\t'.join(detok(x.split()) for x in fields))
