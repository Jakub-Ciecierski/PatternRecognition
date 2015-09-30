#!/bin/bash
for i in "$@"
do
case $i in
    -k=*|--k-clusters=*)
    K="${i#*=}"
    ;;
    *)
            # unknown option
    ;;
esac
done

log_pref_dir="k=${K}"

echo ${log_pref_dir}
python3.4 ../src/main.py \
	--test-type 11 \
	-h 20 \
	-c 1 \
	--learn 1000 \
	--k-cloud ${K} \
	-q 8 \
	--log-pref-dir ${log_pref_dir}
