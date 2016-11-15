#-*- encoding:UTF-8 -*-
#!/usr/bin/python

import socket,threading
import time,Queue
import MySQLdb
import os,sys
import log
from xmlrpclib import ServerProxy

class DB_doing():
    def __init__(self):
        self.conn = MySQLdb.connect(
        host = 'localhost',
        port = 3306,
        user='root',
        passwd='xidian320',
        db ='dscloud'
        )
        self.cur = self.conn.cursor()

    def get_info(self,vm_info):
        sql1 = "select vm.disk,vm.belong from workstation left join vm on workstation.id=vm.belong where vm.name_label = "+"'"+vm_info[1]+"'"+"and workstation.ip="+"'"+vm_info[0]+"'"
        num = self.cur.execute(str(sql1))
        data1 = self.cur.fetchmany(num)
        return data1[0][0]+long(vm_info[4]),data1[0][1]

    def update_info(self,vm_info):
        new_disk,belong = self.get_info(vm_info)
        sql2 = "update vm set cpu_cores="+"'"+str(vm_info[2])+"'"+",memory="+"'"+str(int(vm_info[3])*1024)+"'"+",disk="+"'"+str(new_disk)+"'"+" where name_label="+"'"+str(vm_info[1])+"'"+" and belong="+"'"+str(belong)+"'"
        self.cur.execute(str(sql2))

    def __del__(self):
        self.cur.close()
        self.conn.close()


def doTask(task):
    vm_info = task.split("|")
 
    print vm_info
    try:
        db = DB_doing() 

        #远程调用KVM脚本updateVM
        kvm_ip = vm_info[0]
        name_label = vm_info[1]
        vcpus = vm_info[2]           
        memorys = vm_info[3]       #单位GB
        disks = vm_info[4]         #单位GB(新增硬盘)

        #order = "ssh root@%s python /root/KVM_manager/correctVM.py %s %s %s %s" % (kvm_ip,name_label,vcpus,memorys,disks)
        #os.system(order)

        url = "http://"+kvm_ip+":8888"
        print "connect KVMServer : "+url
        svr = ServerProxy(url)
        svr.correct(name_label,vcpus,memorys,disks)

        db.update_info(vm_info)

        print "updata vm success!"
        print "update database success!"

    except Exception, e:
        log.MyLog(str(e))	
        print str(e)
        
 
def main():
    task = sys.argv[1]     
    doTask(task)


if __name__ =='__main__':
    main()
