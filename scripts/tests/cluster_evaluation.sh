#!/bin/bash
for i in "$@"
do
case $i in
    -k=*|--k-clusters=*)
    K="${i#*=}"
    ;;
    
    -d=*|--sub-dir=*)
    SUB_DIR="${i#*=}"
    
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
	-q 10 \
	--log-sub-dir ${SUB_DIR} \
	--log-pref-dir ${log_pref_dir}
