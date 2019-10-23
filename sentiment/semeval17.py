#!/usr/bin/env python
import sys
import plac

@plac.annotations(
    ntrain=("max training lines", "option", "t", int),
    ndev=("max dev lines if >0", "option", "d", int),
    )
def main(ntrain=10284, ndev=-1):
    n = 0
    outfn = 'train.tsv'
    outf = open(outfn, 'w', encoding='utf-8')
    for l in sys.stdin:
        l = l.strip()
        f = l.split('\t')
        text = f[2]
        label = f[4]
        assert f[0] == f[3]
        if n < ntrain:
            n += 1
        else:
            if n == ntrain:
                n += 1
                outfn = 'dev.tsv'
                outf = open(outfn, 'w', encoding='utf-8')
            if ndev > 0: ndev -= 1
            if ndev == 0: break
        nlabel = 2 if label == 'neutral' else 1 if label == 'positive' else 0
        outf.write('%s\t%s\n' % (text, nlabel)

if __name__ == "__main__":
    plac.call(main)
