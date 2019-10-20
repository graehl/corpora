import plac
import sys
import pytreebank
import sentiment.csv2tsv
from pathlib import Path


def lts(sst, key, fine, nexti=0):
    i = nexti
    for parse in sst[key]:
        i += 1
        for label, text in parse.to_labeled_lines():
            if not fine:
                if label == 2: continue
                label = 0 if label < 2 else 4
            yield (label, text, i)


def csvout(outf, lts, encoding='utf-8'):
    if isinstance(outf, str):
        outf = open(outf, 'w', encoding=encoding)
    nexti = 0
    for label, text, i in lts:
        nexti = i
        print(sentiment.csv2tsv.csv_quoted_fields((str(i - 1), str(label), text)), file=outf)
    return nexti


def log(x):
    sys.stderr.write('INFO: %s\n' % x)


@plac.annotations(
    fine=("fine-grained (0-5 including neutral) output", "option", "f", bool),
    outdir=("outdir/train.csv, outdir/test.csv", "option", "o", str),
    mergedev=("merge dev, test into train", "option", "m", bool)
    )
def main(outdir="SST", fine=False, mergedev=True, encoding='utf-8'):
    path = Path(outdir)
    def csv4(x):
        r = '%s/%s.csv' % (outdir, x)
        log(r)
        return r
    if not path.exists():
        path.mkdir()
    sst = pytreebank.load_sst()
    log("Stanford Sentiment Treebank loaded; %s train, %s dev, %s test sentences" % (len(sst['train']), len(sst['dev']), len(sst['test'])))
    otrain = open(csv4('train'), 'w', encoding=encoding)
    n1 = csvout(otrain, lts(sst, 'train', fine))
    if mergedev:
        n2 = csvout(otrain, lts(sst, 'dev', fine, nexti=n1))
        n3 = csvout(otrain, lts(sst, 'test', fine, nexti=n2))
        sf = open('%s/%s'%(outdir, 'train-dev-test-ids.txt'), 'w')
        splits = '[0...%s) train ...%s) dev (%s) ...%s) test (%s)' % (n1, n2, n2 - n1, n3, n3 - n2)
        log(splits)
        print(splits, file=sf)
        keys = []
    else:
        keys = ['dev', 'test']
    for key in keys:
        csvout(csv4(key), lts(sst, key, fine))


def callmain():
    plac.call(main)


if __name__ == "__main__":
    callmain()
