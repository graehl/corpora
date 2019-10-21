import csv


def needs_csv_quotes(x):
    return x.find(',') >= 0 or x.find('"') >= 0


def escape_inside_quotes(x):
    return x.replace('"', '""')


def csv_quoted(x):
    return '"%s"' % escape_inside_quotes(x) if needs_csv_quotes(x) else x


def csv_quoted_fields(xs):
    return ','.join(csv_quoted(str(x)) for x in xs)


def tsv_quoted(x):
    return x.replace("\t", "  ")


def openread(inf, encoding='utf-8'):
    return open(inf, 'r', encoding=encoding, errors='ignore') if isinstance(inf, str) else inf


def csvread(inf, delimiter=',', encoding='utf-8', quotechar='"'):
    return csv.reader(openread(inf, encoding), delimiter=delimiter, quotechar=quotechar)


def tsvread(inf):
    # tsv files can't have tabs in fields
    return csvread(inf, delimiter='\t', quotechar=None)


def csv2tsv(inf, out):
    for xs in csvread(inf):
        print('\t'.join(tsv_quoted(x) for x in xs), file=out)


def log(x):
    import sys
    sys.stderr.write('INFO: %s\n' % x)


def tsv2csv(inf, out):
    for xs in tsvread(inf):
        print(csv_quoted_fields(xs), file=out)


def csv2ft(inf, out, ft=True):
    for xs in csvread(inf):
        if len(xs) > 1:
            if ft:
                if len(xs) == 2:
                    print('__label__%s %s' % (xs[0].replace('-1.0','NEGATIVE').replace('1.0','POSITIVE'), xs[1]), file=out)
                else:
                    log(xs)
            else:
                print('\t'.join(escape_inside_quotes(x, '\t') for x in xs), file=out)


def main(args, encoding='utf-8'):
    import sys
    ft = len(args) > 0 and args[0] == '-f'
    if ft: args = args[1:]
    if len(args) == 0:
        args = ['-']
    for f in args:
        b = f[:-4] if f.endswith(".csv") else f
        o = '%s.tsv' % b
        stdinout = f == '-'
        csv2ft(sys.stdin if stdinout else open(f, 'r', encoding=encoding, errors='ignore'), sys.stdout if stdinout else open(o, 'w', encoding=encoding), ft)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
