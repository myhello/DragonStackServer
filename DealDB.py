#-*- encoding:UTF-8 -*-
#!/usr/bin/python

import MySQLdb
import sys
class DB_doing():
    def __init__(self):
        self.conn = MySQLdb.connect(
        host = 'localhost',
        port = 3306,
        user='root',
        passwd='xidian320',
        #db ='temp'
        db = 'dscloud'
        )
        self.cur = self.conn.cursor()

    def getServerips(self,belong):
     	sql = "select ip from workstation where belong = "+str(belong)
     	num =  self.cur.execute(sql)
     	data = self.cur.fetchmany(num)
     	return data

    def getServerId(self,region,serverip):
    	sql = "select id,gateway_ip from workstation where ip = "+"'"+str(serverip)+"'"+" and belong = "+str(region)
    	self.cur.execute(sql)
    	data = self.cur.fetchone()
    	return data[1],data[0]

    def update_info(self,vm_info):
        new_disk,belong = self.get_info(vm_info)
        sql2 = "update vm set cpu_cores="+"'"+str(vm_info[2])+"'"+",memory="+"'"+str(int(vm_info[3])*1024)+"'"+",disk="+"'"+str(new_disk)+"'"+" where uuid="+"'"+str(vm_info[1])+"'"+" and belong="+"'"+str(belong)+"'"
        self.cur.execute(str(sql2))
	self.conn.commit()

    def update_vm(self,vm_uuid,vm_label,vm_ip,belong,vm_id):
		sql = "update vm set uuid="+"'"+str(vm_uuid)+"'"+",name_label="+"'"+str(vm_label)+"'"+",ip="+"'"+str(vm_ip)+"'"+",belong="+"'"+str(belong)+"'"+",state=1,power_state='running' where id="+"'"+str(vm_id)+"'"
		print sql
		self.cur.execute(sql)
		self.conn.commit()

    def update_vmlist(self,lid,port,des_ip,gw_ip,local_port):
		sql = "update vm_list set des_ip="+"'"+str(des_ip)+"'"+",local_port="+"'"+str(local_port)+"'"+",gw_ip="+"'"+str(gw_ip)+"'"+",port="+"'"+str(port)+"'"+",state=1 where id="+"'"+str(lid)+"'"
		print sql
		self.cur.execute(sql)
		self.conn.commit()

    def update_new_apply(self,nid):
		sql = "update new_vm_apply set state=1 where id="+"'"+str(nid)+"'"
		print sql
		self.cur.execute(sql)
		self.conn.commit()
    
    def select_user(self,user_id):
	sql = "select username,email,password from user where id = "+"'"+user_id+"'"
        self.cur.execute(sql)
        data = self.cur.fetchone()
        return data[0],data[1],data[2]
		
    def __del__(self):
        self.cur.close()
        self.conn.close()

