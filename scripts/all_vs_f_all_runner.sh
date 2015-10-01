#!/bin/bash
for i in "$@"
do
case $i in
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

#-----------------------------------------------------------------------

START_K=2
END_K=10

log_sub_dir="all_vs_${SUB_DIR}_all"

echo "Running cluster Batch for: all_vs_f_all.sh"

for K in `seq ${START_K} ${END_K}`;
	do
			xterm --hold -e 'tests/all_vs_f_all.sh -k='${K}' -f='${FOREIGN_FILE}' -d='${SUB_DIR} &
	done
