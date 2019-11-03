export PYTHONIOENCODING=utf-8
[[ -d semfin1 ]] || git clone https://bitbucket.org/ssix-project/semeval-2017-task-5-subtask-1.git semfin1
cd semfin1
if false ; then
    cp config.yml semfin1
    set -x
    pip install --upgrade pip
    pip install --upgrade tweepy
    pip install -r requirements.txt
    #python rebuild.py Microblog_Trialdata.json
    python rebuild.py Microblog_Trainingdata.json
fi
python ../semfin.py --ntrain=1400 --ndev=300 --pos=0.3 --neg=-0.3 < Microblog_Trainingdata.json
head *.tsv
wc -l *.tsv
