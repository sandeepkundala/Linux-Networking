while true
do
  sleep 1h
  if [ -f cpuLoad.csv ] ; then
  	rm cpuLoad.csv
  fi
  if [ -f cpuAlert.csv ] ; then
  	rm cpuAlert.csv
  fi
done
