export PYTHONIOENCODING=utf-8
nwiki=${nwiki:-10000}
devwiki=${devwiki:-0}
nimdb=${nimdb:-0}
devimdb=${devimdb:-0}
ntweets=${ntweets:-100}
devtweets=${devtweets:-0}
nfin=${nfin:-1000}
devfin=${devfin:-142}
nsst=${nsst:-0}
devsst=${devsst:-0}
nlines() {
    perl -ne '++$n;END{print "$n"}' "$@"
}
nwikitotal=$((nwiki+devwiki))
if [[ $devwiki -gt 0 && $nwikitotal -lt 100000 ]] ; then
    nwikitotal=100000
fi
./sst3.sh
[[ -d imdb ]] || python ./imdb.py
detok() {
    cat "$@" | python detok.py
}
d=mix3.$nwiki
train=$d/train.tsv
dev=$d/dev.tsv
ln -sf $d mix3
mkdir -p $d
set -x
wikif=`../wiki/wiki-first.sh $nwikitotal`
echo $wikif
./semeval17.sh
./semfin.sh
( cat semeval17/train.tsv | head -n $ntweets
  cat semfin2/train.tsv | head -n $nfin
 cat imdb/train.tsv | head -n $nimdb | detok
 cat sst3/train.tsv | head -n $nsst
 head -n $nwiki < $wikif | perl -pe 'while(<>) { chomp; print "$_\t2\n" }' ) > $train
(cat semeval17/dev.tsv | head -n $devtweets
 cat imdb/dev.tsv | head -n $devimdb | detok
 cat sst3/dev.tsv | head -n $devsst
 cat $wikif | tail -n $devwiki
) > $dev
