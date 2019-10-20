import plac
import sys
import pytreebank
from pathlib import Path



def needs_csv_quotes(x):
    return x.find(',') >= 0 or x.find('"') >= 0


def escape_inside_quotes(x):
    return x.replace('"', '""')


def csv_quoted(x):
    return '"%s"' % escape_inside_quotes(x) if needs_csv_quotes(x) else x


def csv_quoted_fields(xs):
    return ','.join(csv_quoted(str(x)) for x in xs)


def lts(sst, key, fine, neutrals=True, nexti=0, minlen=0):
    i = nexti
    for parse in sst[key]:
        i += 1
        for label, text in parse.to_labeled_lines():
            if len(text) < minlen:
                #log("too short: %s" % text)
                continue
            if not fine:
                if not neutrals and label == 2: continue
                label = 'NEGATIVE' if label < 2 else 'NEUTRAL' if label == 2 else 'POSITIVE'
            yield (label, text, i)


def csvout(outf, lts, tsv=False, encoding='utf-8'):
    if isinstance(outf, str):
        log(outf)
        outf = open(outf, 'w', encoding=encoding)
    nexti = 0
    for label, text, i in lts:
        nexti = i
        if tsv:
            outf.write(str(label) + '\t' + text + '\n')
        else:
            print(csv_quoted_fields((str(i - 1), str(label), text)), file=outf)
    return nexti


def log(x):
    sys.stderr.write('INFO: %s\n' % x)


@plac.annotations(
    fine=("fine-grained (0-4 including neutral) output", "option", "f", bool),
    neutrals=("0-1 => 0, 3-4 => 4", "option", "n", bool),
    minlen=("min length in chars", "option", "l", int),
    outdir=("outdir/train.csv, outdir/test.csv", "option", "o", str),
    mergedev=("merge dev, test into train", "option", "m", bool),
    tsv=("simple tsv class text output", "option", "t", bool)
    )
def main(outdir="SST", fine=False, mergedev=False, encoding='utf-8', minlen=2, neutrals=False, tsv=False):
    path = Path(outdir)
    csvext='.csv'
    if tsv: csvext='.tsv'
    def csv4(x):
        r = '%s/%s%s' % (outdir, x, csvext)
        log(r)
        return r
    if not path.exists():
        path.mkdir()
    sst = pytreebank.load_sst()
    log("Stanford Sentiment Treebank loaded; %s train, %s dev, %s test sentences" % (len(sst['train']), len(sst['dev']), len(sst['test'])))
    otrain = open(csv4('train'), 'w', encoding=encoding)
    n1 = csvout(otrain, lts(sst, 'train', fine, neutrals, minlen=minlen), tsv)
    if mergedev:
        log('mergedev')
        n2 = csvout(otrain, lts(sst, 'dev', fine, neutrals, nexti=n1, minlen=minlen), tsv)
        n3 = csvout(otrain, lts(sst, 'test', fine, neutrals, nexti=n2, minlen=minlen), tsv)
        sf = open('%s/%s'%(outdir, 'train-dev-test-ids.txt'), 'w')
        splits = '[0...%s) train ...%s) dev (%s) ...%s) test (%s)' % (n1, n2, n2 - n1, n3, n3 - n2)
        log(splits)
        print(splits, file=sf)
        keys = []
    else:
        log('dev, test')
        keys = ['dev', 'test']
    for key in keys:
        csvout(csv4(key), lts(sst, key, fine, neutrals, minlen=minlen), tsv)


def callmain():
    plac.call(main)


if __name__ == "__main__":
    callmain()
