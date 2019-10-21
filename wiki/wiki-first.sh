n=${1:-100000}
o=wiki-first.$n.txt
nlines() {
    perl -ne '++$n;END{print "$n"}' "$@"
}
if ! [[ -f $o || $(nlines $o) -lt "$n" ]] ; then
    if [[ $n -le 100000 ]] ; then
        [[ -d sentiment-mixes ]] || git clone https://github.com/graehl/sentiment-mixes.git
        (cd sentiment-mixes; git pull)
        head -n $n < sentiment-mixes/wiki/wiki-first.100000.txt > $o
    else
        `dirname $0`/head-wikitext.sh $((n/50)) --minlen 80 --first True | head -n $n > $o.tmp && mv $o.tmp $o
    fi
fi
echo $o
