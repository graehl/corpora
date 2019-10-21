pip install pytreebank
pip install plac
pip install revtok
pip install --upgrade nltk
python -m nltk.downloader treebank
[[ -d sst3 ]] || python ./download_sst.py -l 40 -n True -o sst3 -t True
