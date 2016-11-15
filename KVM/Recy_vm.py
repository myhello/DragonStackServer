#-*- encoding:UTF-8 -*-
#!/usr/bin/python

import MySQLdb
import os
import log
import sys
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

    def delete_nat(self,vm_list_id):
        sql1 = "delete from vm_list where id = "+"'"+vm_list_id+"'"
        self.cur.execute(str(sql1))
        self.conn.commit()
    
    '''
    def delete_vm(self,vm_uuid):
        sql2 = "delete from vm where uuid="+"'"+str(vm_uuid)+"'"
        self.cur.execute(str(sql2))
        self.conn.commit()
    '''

    def __del__(self):
        self.cur.close()
        self.conn.close()


def doTask(task):
    vm_info = task.split("|")

    try:
        
        db = DB_doing() 

        kvm_ip = vm_info[0]
        name_label = vm_info[2]
    
        #shell 远程调用KVM执行脚本
        #order = "ssh root@%s python /root/KVM_manager/deleteVM.py %s" % (kvm_ip,name_label)
        #os.system(order)
        
	#kvm delete vm operation
	url = "http://"+kvm_ip+":8888"
	print url
	svr = ServerProxy(url)
	svr.delete(name_label)
        
        db.delete_nat(vm_info[1])    #vm_list中的id
        #db.delete_vm(vm_info[2])     #vm uuid不删除

        delete_nat = 'sudo iptables -t nat -D PREROUTING -i eth1 -p tcp --dport %s -j DNAT --to-destination %s:%s' % (vm_info[5],vm_info[3],vm_info[4])  
        #print delete_nat
        os.system(delete_nat)
        os.system("sudo service iptables save")

        
        print "delete vm success!"    
    except Exception, e:
        print str(e)
        log.MyLog(str(e))
 
def main():
    task = sys.argv[1]     
    doTask(task)
    
             
if __name__ =='__main__':
    main()
