#!/bin/bash
if [ $# != 2 ]
then 
    echo 'please input the two params'
	exit
fi
 
ip=$1
port=$2

start=20000
flag=${ip}:${port}

ddport=
condition=0
x=0
for line in `sudo iptables -nL -t nat --line | grep $flag`
do
    lines[$x]=$line
    x=$(expr $x + 1)
done

num=${#lines[@]}
if [ $num != 0 ]
then
    for((i=8;i<num;i=i+9))
    do
        temp=${lines[i]}
        temp=${temp#*:}
        if [ $temp = $flag ]
        then
            condition=1
            ddport=${lines[i-1]}
            ddport=${ddport#*:}
            echo $ddport
            break
        fi
    done
fi

if [ $condition -eq 1 ]
then 
	echo 'the port has already been NAT'
    eval echo $ddport > $flag
else
    for((i=$start;i<50000;i++))
    do
        dport=$i
        #echo $dport
   		isExitPort=`sudo sudo iptables -nL -t nat | awk '{print $7}' | grep -n $dport | wc -l`
		if [ $isExitPort -ge 1 ]
        then 
        	continue
        else
        	eval sudo iptables -t nat -A PREROUTING -i eth1 -p tcp --dport $dport -j DNAT --to-destination $ip:$port
            eval echo $dport > $flag
            break
        fi
    done
    sudo service iptables save
	echo "NAT port $i success!"
fi


