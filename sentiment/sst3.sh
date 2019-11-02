pip install --upgrade plac
pip install --upgrade nltk
python -m nltk.downloader treebank
if [[ -d sst3 ]] ; then
    ls sst3
else
    pip install --upgrade pytreebank
    python ./download_sst.py -l 40 -n True -o sst3 -t True
fi
