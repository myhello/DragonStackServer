#-*- encoding:UTF-8 -*-
#!/usr/bin/python

import socket,threading
import time,Queue
from xen import Xen
import MySQLdb
import os,sys
import log

class DB_doing():
    def __init__(self):
        self.conn = MySQLdb.connect(
        host = 'localhost',
        port = 3306,
        user='root',
        passwd='xidian320',
        db ='temp'
        )
        self.cur = self.conn.cursor()

    def get_info(self,vm_info):
        sql1 = "select vm.disk,vm.belong from workstation left join vm on workstation.id=vm.belong where vm.uuid = "+"'"+vm_info[1]+"'"+"and workstation.ip="+"'"+vm_info[0]+"'"
        num = self.cur.execute(str(sql1))
        data1 = self.cur.fetchmany(num)
        return data1[0][0]+long(vm_info[4]),data1[0][1]

    def update_info(self,vm_info):
        new_disk,belong = self.get_info(vm_info)
        sql2 = "update vm set cpu_cores="+"'"+str(vm_info[2])+"'"+",memory="+"'"+str(int(vm_info[3])*1024)+"'"+",disk="+"'"+str(new_disk)+"'"+" where uuid="+"'"+str(vm_info[1])+"'"+" and belong="+"'"+str(belong)+"'"
        self.cur.execute(str(sql2))

    def __del__(self):
        self.cur.close()
        self.conn.close()


def doTask(task):
    vm_info = task.split("|")

    xenserver_ip = vm_info[0]
        
    fields = {}
    fields['description'] = ''
    fields['cpu_cores'] = vm_info[2]
    fields['backup'] = False
    fields['mem_size'] = vm_info[3]
    List_tags = []
    fields['tags'] = List_tags
    
    url = "http://"+xenserver_ip
    user = "root"
    pwd = "123456"
    xen = Xen(url,user,pwd)
    try:
        db = DB_doing() 
        new_disk,belong = db.get_info(vm_info)
        new_disk = new_disk*1024*1024*1024

        xen.vm_stop(vm_info[1])
        time.sleep(10)

        xen.update_disk(vm_info[1],str(new_disk))
        print "add disk success!"    
    except Exception, e:
	log.MyLog(str(e))	
        print str(e)
    
    try:
        xen.vm_update(vm_info[1],fields)
        print "update vm success!"
    except Exception, e:
        print str(e)
        raise e
    

    try:
        db.update_info(vm_info)
        print "update database success!"
    except Exception, e:
        print str(e)
        raise e
        
 
def main():
    task = sys.argv[1]     
    doTask(task)


if __name__ =='__main__':
    main()
