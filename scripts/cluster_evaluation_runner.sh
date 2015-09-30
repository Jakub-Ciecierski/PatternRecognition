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

echo "Running cluster Batch for: cluster_evaluation.sh"

for K in `seq ${START_K} ${END_K}`;
	do
			xterm --hold -e 'tests/cluster_evaluation.sh -k='${K} &
	done
