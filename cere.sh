l=${1:-nom}
for t in task.*; do
    echo $t
    python cere.py targ.$l $t | sed -e 's/```//' > ${t##*.}-qwen.$l
done
