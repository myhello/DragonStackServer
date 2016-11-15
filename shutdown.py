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
        	db ='dscloud'
        )
        self.cur = self.conn.cursor()
	
    def getVmUUID(self,vmids):
		vmuuids = {}
		for vmid in vmids:
			sql1 = "select workstation.ip,vm.uuid from workstation,vm where vm.belong=workstation.id and vm.id="+"'"+str(vmid)+"'"			 
			count = self.cur.execute(sql1)
			result = self.cur.fetchone()
			if vmuuids.has_key(result[0]):
				vmuuids[result[0]].append(result[1])	
			else:
				vmuuids[result[0]] = [result[1]]
		return vmuuids
			
    def updateVmState(self,vmids):
		for vmid in vmids:
			sql2 = "update vm set state=0,power_state='shutdown' where id="+"'"+str(vmid)+"'"
			self.cur.execute(sql2)
			self.conn.commit()
	
    def __del__(self):
        	self.cur.close()
        	self.conn.close()


def doTask(task):
    vmids = task.split("|")
    db = DB_doing()
    vmuuids = db.getVmUUID(vmids)
    try:
	for wsip,uuids in vmuuids.items():
		url = "http://"+wsip
		user = "root"
		pwd = "123456"
		xen = Xen(url,user,pwd)
		for uuid in uuids:
			xen.vm_stop(uuid)
	time.sleep(5)
	print "shutdown userVms success!"
	db.updateVmState(vmids)
    except Exception,e:
		log.MyLog(str(e))
		print str(e)
	
 
def main():
    task = sys.argv[1]     
    doTask(task)


if __name__ =='__main__':
    main()
