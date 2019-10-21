#!/usr/bin/python

import os
import os.path
import sys
import subprocess
import glob
import plac

def pp(x):
    return x.replace('<br />', ' ').replace('\t', ' ').replace('  ', ' ')


def log(x):
    print(str(x), file=sys.stderr)

@plac.annotations(
    download=("aclImdb download dir", "option", "d", str),
    outd=("output directory for train.tsv dev.tsv", "option", "o", str),
    devtexturl=("alternate dev text (no labels) url", "option", "u", str),
    )
def main(outd='imdb', download='aclImdb', devtexturl=''):
  tarf = 'aclImdb_v1.tar.gz'
  assert os.path.isfile(tarf) or subprocess.call(['wget', 'https://ai.stanford.edu/~amaas/data/sentiment/%s' % tarf]) == 0
  assert os.path.isdir(download) or subprocess.call(['tar', 'xzf', tarf]) == 0

  try:
      os.makedirs(outd)
  except:
      pass


  log(devtexturl)
  for corpin, corpout in (('test', 'dev'), ('train', 'train'), ):
      outfn = '%s/%s.tsv' % (outd, corpout)
      outf = open(outfn, 'w', encoding='utf-8')
      print('sentence\tlabel', file=outf)
      log(outfn)
      if corpout == 'dev' and devtexturl is not None:
          log(devtexturl)
          import urllib.request
          for line in urllib.request.urlopen(devtexturl):
              print('%s\t1' % pp(line.decode('utf-8').strip()), file=outf)
      else:
          for name, label in (('neg', '0'), ('pos', '1')):
              log((corpin, corpout, name, label, outfn))
              fs = '%s/%s/%s/*.txt' % (download, corpin, name)
              for fn in glob.glob(fs):
                  with open(fn, 'r', encoding='utf-8') as f:
                      print('%s\t%s' % (pp(f.read().replace('\n', '')), label), file=outf)

if __name__ == "__main__":
    plac.call(main)
    callmain()
