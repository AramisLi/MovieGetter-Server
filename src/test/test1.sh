#!/usr/bin/env bash


array=(a b c d)
echo ${#array[@]}

echo ${#array[*]}

echo `expr 2 + 5`
echo `date`

for i in array
do
    echo ${i}
done

curl www.baidu.com