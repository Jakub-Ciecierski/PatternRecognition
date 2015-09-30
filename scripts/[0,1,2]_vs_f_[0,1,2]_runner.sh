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
END_K=8

log_sub_dir="all_vs_${SUB_DIR}_all"

echo "Running cluster Batch for: [0,1,2]_vs_f_[0,1,2].sh"

for K in `seq ${START_K} ${END_K}`;
	do
			xterm --hold -e 'tests/[0,1,2]_vs_f_[0,1,2].sh -k='${K}' -f='${FOREIGN_FILE}' -d='${SUB_DIR} &
	done
