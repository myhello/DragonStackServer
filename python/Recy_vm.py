#-*- encoding:UTF-8 -*-
#!/usr/bin/python

import socket,threading
import time,Queue
from xen import Xen
import MySQLdb
import os

class DB_doing():
    def __init__(self):
        self.conn = MySQLdb.connect(
        host = '222.25.140.1',
        port = 3306,
        user='root',
        passwd='xidian320',
        db ='temp'
        )
        self.cur = self.conn.cursor()

    def delete_nat(self,vm_list_id):
        sql1 = "delete from vm_list where id = "+"'"+vm_list_id+"'"
        self.cur.execute(str(sql1))
        self.conn.commit()

    def delete_vm(self,vm_uuid):
        sql2 = "delete from vm where uuid="+"'"+str(vm_uuid)+"'"
        self.cur.execute(str(sql2))
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()


def doTask(task):
    vm_info = task.split("|")

    xenserver_ip = vm_info[0]
    
    url = "http://"+xenserver_ip
    user = "root"
    pwd = "123456"
    xen = Xen(url,user,pwd)
    try:
        db = DB_doing() 
        db.delete_nat(vm_info[1])    #vm_list中的id
        db.delete_vm(vm_info[2])     #vm uuid

        delete_nat = 'sudo iptables -t nat -D PREROUTING -i eth1 -p tcp --dport %s -j DNAT --to-destination %s:%s' % (vm_info[5],vm_info[3],vm_info[4])  
        print delete_nat
        os.system(delete_nat)
        os.system("sudo service iptables save")

        xen.vm_destroy(vm_info[2])   
        
        print "delete vm success!"    
    except Exception, e:
        print str(e)
        raise e
        
 
def main():
    task = sys.argv[1]     
    doTask(task)
    
             
if __name__ =='__main__':
    main()
