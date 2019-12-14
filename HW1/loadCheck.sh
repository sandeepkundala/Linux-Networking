T="$1"
TP="$2"
X="$3"
Y="$4"
high="HIGH CPU usage"
veryHigh="Very HIGH CPU usage"
n=0
prev1Min=0

while [ $TP -gt $n ]
do
	if [ ! -f cpuLoad.csv ] ;
	then
	    printf "Timestamp,1min,5min,15min\n" >> cpuLoad.csv
	fi
	if [ ! -f cpuAlert.csv ] ;
	then
	    printf "Timestamp,Alert String,1min,5min,15min\n" >> cpuAlert.csv
	fi
	
	sleep $T
	n=$(( n+T )) 

	up="$(uptime)"
	IFS=' ,' read -ra upData <<< "$up"
	size="${#upData[@]}"
	
	printf "${upData[0]},${upData[$size-3]},${upData[$size-2]},${upData[$size-1]}\n" >> cpuLoad.csv

	oneOut=`echo "$X >= ${upData[$size-3]}" | bc`
	fiveOut=`echo "$Y >= ${upData[$size-2]}" | bc`
	if [[ $T -ne $n ]] ; then
		prevOut=`echo "${upData[$size-2]} > $prev1Min" | bc`
	fi

	if [[ oneOut -ne 1 ]] ; then
		printf "${upData[0]},$high,${upData[$size-3]},${upData[$size-2]},${upData[$size-1]}\n" >> cpuAlert.csv
	fi

	if [[ $T -ne $n ]] && [[ oneOut -ne 1 ]] && [[ fiveOut -ne 1 ]] && [[ prevOut -ne 1 ]] ; then
		printf "${upData[0]},$veryHigh,${upData[$size-3]},${upData[$size-2]},${upData[$size-1]}\n" >> cpuAlert.csv
	fi
	prev1Min="${upData[$size-3]}"
done
