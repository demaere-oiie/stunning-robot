l=${1:-nom}
for t in task.*; do
    echo ${t##*.}-qwen.$l
done
