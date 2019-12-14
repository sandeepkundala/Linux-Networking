There are two shell scripts named loadCheck.sh and cleanUp.sh.

loadCheck.sh
-------------

This script logs the load averages in a CSV file with T seconds granularity for TP seconds. The csv file is named as "cpuLoad.csv"

It also generates "HIGH CPU uage" and "Very HIGH CPU usage" alerts based on the threshold values and other associated conditions for the Very High CPU usage and writes them to the "cpuAlert.csv" file

The log files are written to the current directory.

This script needs 4 arguments to run.

To make the shell script executable: chmod 775 <filename.sh>

Eg: 

./loadCheck.sh 10 60 2 2

Here, T is 10, TP is 60 and X,Y are 2 respectively.

Running:

The script logs load avergaes at 10,20,30,40,50 and 60 seconds respectively.

For Very HIGH CPU usage, the conditions checked are as follows

-> The previous 1 minute load average should be lesser than the current 1 minute load average.
-> The current 1 minute load average should be greater or equal to the threshold X
-> The current 5 minutes lod average should be greater or equal to the threshold Y


For HIGH CPU usage, the current 1 minute load average should be greater or equal to the threshold

cleanUp.sh
-----------

When the script is started, the lopp runs every hour and checks if the log files [cpuLoad.csv and cpuAlert.csv] are present. If yes, it deletes them.

It can be run as a background process so that it does not terminate.

To make the shell script executable: chmod 775 <filename.sh>

