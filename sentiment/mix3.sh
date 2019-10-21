export PYTHONIOENCODING=utf-8
nwp=${1:-10000}
devwp=${2:-1000}
devimdb=${3:-5000}
nwptotal=$((nwp+devwp))
./sst3.sh
[[ -d imdb ]] || python ./imdb.py
detok() {
    for f in "$@"; do
        python detok.py < "$f"
    done
}
d=mix3.$nwp
train=$d/train.tsv
dev=$d/dev.tsv
ln -sf $d mix3
mkdir -p $d
set -x
wpf=`../wiki/wiki-first.sh $nwptotal`
echo $wpf
(cat sst3/train.tsv
 detok imdb/train.tsv
 head -n $nwp < $wpf | perl -pe 'while(<>) { chomp; print "$_\t2\n" }'
) > $train
(cat sst3/dev.tsv; detok imdb/dev.tsv | head -n $devimdb) > $dev
# ; tail -n $devwp < $wpf
