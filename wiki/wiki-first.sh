n=${1:-100000}
o=wp-first.$n.txt
./head-wikitext.sh $((n/100)) --minlen 80 --first True | head -n $n > $o
echo $o
