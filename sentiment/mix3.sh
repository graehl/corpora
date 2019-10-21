export PYTHONIOENCODING=utf-8
nwp=${1:-10000}
devwp=${2:-1000}
devimdb=${3:-5000}
ntweets=${4:-10000}
devtweets=${5:-1000}
nlines() {
    perl -ne '++$n;END{print "$n"}' "$@"
}
nwptotal=$((nwp+devwp))
./sst3.sh
[[ -d imdb ]] || python ./imdb.py
detok() {
    cat "$@" | python detok.py
}
d=mix3.$nwp
train=$d/train.tsv
dev=$d/dev.tsv
ln -sf $d mix3
mkdir -p $d
set -x
wpf=`../wiki/wiki-first.sh $nwptotal`
echo $wpf
[[ -d semeval17 ]] || ./semeval17.sh
( cat semeval17/train.tsv
 detok imdb/train.tsv
 cat sst3/train.tsv
 head -n $nwp < $wpf | perl -pe 'while(<>) { chomp; print "$_\t2\n" }' ) > $train
(cat semeval17/dev.tsv; head -n $devimdb < imdb/dev.tsv | detok ; cat sst3/dev.tsv) > $dev
# ; tail -n $devwp < $wpf
