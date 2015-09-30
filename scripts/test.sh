IFS="="
while read -r name value
do
	if [ "$name"-eq"START_K" ]
	then
		START_K=${value//\"/}
		echo 'start'
		echo ${value//\"/}
		
	elif [ "$name"-eq"END_K"]
	then
		END_K=${value//\"/}
		echo 'end'
		echo ${value//\"/}
	fi
done < "config.conf"

echo ${END_K}
echo ${START_K}

