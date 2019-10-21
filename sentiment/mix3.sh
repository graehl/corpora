export PYTHONIOENCODING=utf-8
nwp=${1:-10000}
./sst3.sh
[[ -d imdb ]] || python ./imdb.py
wpf=`../wiki/wiki-first.sh $nwp`
echo $wpf
detok() {
    python detok.py
}
skip1() {
    (
    read
    detok ) < $1
}
d=mix3.$nwp
mkdir -p $d
train=$d/train.tsv
dev=$d/dev.tsv
(cat sst3/train.tsv
 skip1 imdb/train.tsv
 perl -pe 'while(<>) { chomp; print "$_\t2\n" }' < $wpf
 ) > $train
(cat sst3/dev.tsv) > $dev
