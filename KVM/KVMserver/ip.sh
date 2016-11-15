#MODIFY 2015-06-10 
#ping当前网段内在线的主机,以便产生arp记录. 
subnet=`route -n|grep "UG" |awk '{print $2}'|sed 's/..$//g'` 
#for ip in $subnet.{1..253};do 
for ip in 192.168.0.{1..253};do
{ 
ping -c1 $ip >/dev/null 2>&1 
}& 
done 
#依次查找arp记录. 
running_vms=`virsh list |grep "$1"` 
#echo -ne "共有`echo "$running_vms"|wc -l`个虚拟机在运行.\n" 
for i in `echo "$running_vms" | awk '{ print $2 }'`;do 
mac=`virsh dumpxml $i |grep "mac address"|sed "s/.*'\(.*\)'.*/\1/g"` 
ip=`arp -ne |grep "$mac" |awk '{printf $1}'` 
#printf "%-30s %-30s\n" $i $ip 
printf "%-30s %-30s\n"  $ip 
#echo $ip > /home/Dragonstack/DragonStackServer/VMServer/ip.txt
done

