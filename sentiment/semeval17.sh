export PYTHONIOENCODING=utf-8
cd semeval17
set -x
[[ -s train.tsv && -s dev.tsv ]] || paste SemEval2017-task4-test.subtask-A.english.txt SemEval2017_task4_subtaskA_test_english_gold.txt | python ../semeval17.py
wc -l *.tsv
head *.tsv
