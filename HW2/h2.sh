file=/var/customlogs/logs/monitor.csv
host=$(hostname)
i=0
limit=$(($1*60))
while [ $i -lt $limit ];
do
	sleep 60
	if [ ! -s "$file" ]; then
		mkdir -p /var/customlogs/logs/
    		touch $file
		echo "hostname, cpu1min, cpu5min, cpu15min" >> $file;
	fi
	t1=$(uptime)
        echo ${t1#*load average: } | (
        	IFS=', ' && read L1 L5 L15
		count_dt=$(date "+%Y-%m-%d %H:%M:%S")
		echo "${host}, ${L1}, ${L5}, ${L15}" >> $file
    	)
	i=$((i+60));
done
