#!/usr/bin/env python
import plac
import re
import io
import sys
import codecs

EOA_line='ENDOFARTICLE.'

def log(x):
    sys.stderr.write('INFO: %s\n' % str(x))


blanks = re.compile(r'\s+')
doc = re.compile('^(?:</doc>|<doc id=.*title="([^"]+)".*)$')
@plac.annotations(
    minlen=("min length in chars", "option", "l", int),
    first=("first para only", "option", "f", bool),
)
def main(minlen=40, first=True):
    eof = False
    start = True
    title = ''
    i = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='ignore')
    n = 0
    for line in i:
        m = doc.match(line)
        if m:
            start = True
            title = m.group(1)
            if title:
                n += 1
                if n % 100 == 0:
                    sys.stderr.write('\n'+title)
                else:
                    sys.stderr.write('.')
            continue
        if first and not start: continue
        start = False
        line = line.strip()
        line = blanks.sub(' ', line)
        if len(line) < minlen: continue
        print(line)
        sys.stderr.write('\n')


if __name__ == "__main__":
    main()
