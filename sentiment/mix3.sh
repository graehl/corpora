export PYTHONIOENCODING=utf-8
nwiki=${nwiki:-10000}
devwiki=${devwiki:-0}
nimdb=${nimdb:-0}
devimdb=${devimdb:-0}
ntweets=${ntweets:-100}
devtweets=${devtweets:-0}
nfin=${nfin:-1000}
devfin=${devfin:-142}
nfin1=${nfin:-1400}
devfin1=${devfin1:-300}
nsst=${nsst:-0}
devsst=${devsst:-0}
d=mix3.w$nwiki-$devwiki.i$nimdb-$devimdb.t$ntweets-$devtweets.f$nfin-$devfin.f1$nfin1-$devfin1.s$nsst-$devsst
echo $d
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
train=$d/train.tsv
dev=$d/dev.tsv
mkdir -p $d
rm -f mix3
ln -sf $d mix3
set -x
wikif=`../wiki/wiki-first.sh $nwikitotal`
echo $wikif
ls -l $wikif
./semeval17.sh
./semfin2.sh
./semfin1.sh
wc -l semeval17/train.tsv  semfin2/train.tsv imdb/train.tsv sst3/train.tsv $wikif
( cat semeval17/train.tsv | head -n $ntweets
  cat semfin1/train.tsv | head -n $nfin1
  cat semfin2/train.tsv | head -n $nfin
 cat imdb/train.tsv | head -n $nimdb | detok
 cat sst3/train.tsv | head -n $nsst
 cat $wikif | head -n $nwiki | perl -pe 'while(<>) { chomp; print "$_\t2\n" }' ) > $train
(cat semeval17/dev.tsv | head -n $devtweets
 cat imdb/dev.tsv | head -n $devimdb | detok
 cat sst3/dev.tsv | head -n $devsst
  cat semfin1/dev.tsv | head -n $devfin1
  cat semfin2/dev.tsv | head -n $devfin
 cat $wikif | tail -n $devwiki
) > $dev
