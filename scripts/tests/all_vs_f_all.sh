#!/bin/bash
for i in "$@"
do
case $i in
    -k=*|--k-clusters=*)
    K="${i#*=}"
    ;;
    
    -f=*|--f-file=*)
    FOREIGN_FILE="${i#*=}"
    ;;
    
    -d=*|--sub-dir=*)
    SUB_DIR="${i#*=}"
    
    ;;
    *)
            # unknown option
    ;;
esac
done

log_sub_dir="all_vs_${SUB_DIR}_all"
log_pref_dir="k=${K}"

python3.4 ../src/main.py \
	--test-type 10 \
	--f-file ${FOREIGN_FILE} \
	--n-train-file ../resources/all/training_\[0\,\ 1\,\ 2\,\ 3\,\ 4\,\ 5\,\ 6\,\ 7\,\ 8\,\ 9\].txt \
	--n-test-file ../resources/all/test_\[0\,\ 1\,\ 2\,\ 3\,\ 4\,\ 5\,\ 6\,\ 7\,\ 8\,\ 9\].txt \
	--mvee 0.0003 \
	-q 10 \
	-k ${K} \
	--log-sub-dir ${log_sub_dir} \
	--log-pref-dir ${log_pref_dir}
