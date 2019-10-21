n=$1
shift
bytes=${bytes:-$((n*100000))}
range=0-${bytes}
curl -r$range https://www.cs.upc.edu/~nlp/wikicorpus/raw.en.tgz 2>/dev/null | tar xOzf - | python `dirname $0`/filter-wikitext.py "$@"
