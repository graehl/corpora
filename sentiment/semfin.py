#!/usr/bin/env python

import sys
import plac
import json

def log(x):
    sys.stderr.write('INFO: %s\n' % str(x))

@plac.annotations(
    ntrain=("max training lines", "option", "t", int),
    ndev=("max dev lines if >0", "option", "d", int),
    pos=("threshold on [-1,1] at or above which we say positive (class 1)", "option", "p", float),
    neg=("threshold on [-1,1] below which we say negative (class 0)", "option", "n", float),
    )
def main(ntrain=1000, ndev=-1, pos=0.3, neg=-.3):
    n = 0
    data = json.load(sys.stdin)
    outfn = 'train.tsv'
    outf = open(outfn, 'w', encoding='utf-8')
    log('%s headlines' % len(data))
    for ts in data:
        if n < ntrain:
            n += 1
        else:
            if n == ntrain:
                n += 1
                outfn = 'dev.tsv'
                outf = open(outfn, 'w', encoding='utf-8')
            if ndev > 0: ndev -= 1
            if ndev == 0: break
        text = ts["title"]
        s = float(ts["sentiment"])
        nlabel = '1' if s >= pos else '0' if s < neg else '2'
        outf.write('%s\t%s\n' % (text, nlabel))

if __name__ == "__main__":
    plac.call(main)
