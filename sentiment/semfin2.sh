export PYTHONIOENCODING=utf-8
[[ -d semfin2 ]] || git clone https://bitbucket.org/ssix-project/semeval-2017-task-5-subtask-2.git semfin2
#git clone https://bitbucket.org/ssix-project/semeval-2017-task-5-subtask-1.git
cd semfin2
set -x
python ../semfin.py --ntrain=1000 --ndev=142 --pos=0.3 --neg=-0.3 < Headline_Trainingdata.json
wc -l *.tsv
head *.tsv
