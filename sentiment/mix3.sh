export PYTHONIOENCODING=utf-8
nwp=${1:-10000}
devwp=${2:-1000}
nwptotal=$((nwp+devwp))
./sst3.sh
[[ -d imdb ]] || python ./imdb.py
wpf=`../wiki/wiki-first.sh $nwptotal`
echo $wpf
detok() {
    python detok.py
}
d=mix3.$nwp
ln -sf $d mix3
mkdir -p $d
train=$d/train.tsv
dev=$d/dev.tsv
nwp=$((nwp-devwp))
set -x
(cat sst3/train.tsv
 detok imdb/train.tsv
 head -n $nwp < $wpf | perl -pe 'while(<>) { chomp; print "$_\t2\n" }'
) > $train
(cat sst3/dev.tsv; tail -n $devwp < $wpf) > $dev
