#-*- encoding:UTF-8 -*-

import MySQLdb

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

    def getServerips(self,belong):
     	sql = "select ip from workstation where belong = "+str(belong)
     	num =  self.cur.execute(sql)
     	data = self.cur.fetchmany(num)
     	return data

    def getServerId(self,region,serverip):
    	sql = "select id from workstation where ip = "+"'"+str(serverip)+"'"+" and belong = "+str(region)
    	self.cur.execute(sql)
    	data = self.cur.fetchone()
    	return data[0]

    def update_info(self,vm_info):
        new_disk,belong = self.get_info(vm_info)
        sql2 = "update vm set cpu_cores="+"'"+str(vm_info[2])+"'"+",memory="+"'"+str(int(vm_info[3])*1024)+"'"+",disk="+"'"+str(new_disk)+"'"+" where uuid="+"'"+str(vm_info[1])+"'"+" and belong="+"'"+str(belong)+"'"
        self.cur.execute(str(sql2))

    def __del__(self):
        self.cur.close()
        self.conn.close()

