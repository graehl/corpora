nwp=${1:-10000}
[[ -d sst3 ]] || ./sst3.sh
[[ -d imdb ]] python ./imdb.py
wpf=`../wiki/wiki-first.sh $nwp`
skip1() {
    read
    cat
}
d=mix3.$nwp
mkdir -p $d
train=$d/train.tsv
dev=$d/dev.tsv
(cat sst3/train.tsv
 skip1 imdb/train.tsv
 perl -pe 'while(<>) { chomp; print "$_\t2\n" }' $wpf
 ) > $train
(cat sst3/dev.tsv) > $dev
