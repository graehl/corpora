n=${1:-100000}
o=wiki-first.$n.txt
[[ -f $o ]] || `dirname $0`/head-wikitext.sh $((n/50)) --minlen 80 --first True | head -n $n > $o.tmp
mv $o.tmp $o
echo $o
