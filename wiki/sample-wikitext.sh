export PYTHONIOENCODING=utf-8
mb=${1:-1}
bytes=${bytes:-$((mb*1000000))}
range=0-${bytes}
first=True
minlen=80
curl -r$range https://www.cs.upc.edu/~nlp/wikicorpus/raw.en.tgz | tar xOzf - | python ./filter-wikitext.py --first $first --minlen $minlen > wp.${mb}mb.$first.txt
