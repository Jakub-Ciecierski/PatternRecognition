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

log_sub_dir="[0,1,2]_vs_${SUB_DIR}_all"
log_pref_dir="k=${K}"

python3.4 ../src/main.py \
	--test-type 10 \
	--f-file ${FOREIGN_FILE} \
	--n-train-file ../resources/0\,1\,2/training_\[0\,\ 1\,\ 2\].txt \
	--n-test-file ../resources/0\,1\,2/test_\[0\,\ 1\,\ 2\].txt \
	--mvee 0.0003 \
	-q 8 \
	-k ${K} \
	--log-sub-dir ${log_sub_dir} \
	--log-pref-dir ${log_pref_dir}

