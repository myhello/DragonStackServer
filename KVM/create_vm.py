#-*- encoding:UTF-8 -*-
#!/usr/bin/python

import sys
import os
import socket
import time
import thread
import DealDB
import json
import log
from xmlrpclib import ServerProxy

#默认用户名和密码
user = "root"
pwd = "123456"
centos_user = 'centos'
ubunbu_user = 'ubuntu'
windows_user = 'Administrator'
oldpassword = 'Xidian320'


#从数据库找出某域所有server的ip
def find_all_servers(region):
	db = DealDB.DB_doing()
	serverips = []
	serveripslist = db.getServerips(region)
	for item in serveripslist:
		serverips.append(item[0])
	return serverips

def find_serverid(region,serverip):
	db = DealDB.DB_doing()
	gw_ip ,serverid = db.getServerId(region,serverip)
	return serverid,gw_ip

#轮训所有服务器，找到适合创建client传来参数虚拟机的kvmserver服务器的ip 
def find_server(region,cpu_cores,mem_size,new_disk,os_type):
	server_ips = find_all_servers(region)
	url = ''
	for server_ip in server_ips:
		url = "http://" + server_ip + ":8888"
		print "connect url: "+url
		try:
			svr = ServerProxy(url)   #如果server连不上，连下一个server
			if svr.canCreateVm(cpu_cores,mem_size,new_disk,os_type):
				return server_ip
			else:
				print "resoure is not enough!"
		except Exception, e:
			print "connect url "+url+" failed!"
			continue
	return None

#调用shell脚本进行NAT转发，返回dport
def NAT(ip,lport):
	os.system("/home/gw/DragonStackServer2.0/KVM/addNAT.sh "+ip+" "+str(lport))
        #NAT_shell = "./addNAT.sh "+ip+" "+str(lport)
	try:
		with open("/home/gw/DragonStackServer2.0/KVM/"+ip+":"+str(lport),"rb") as a:
	        		dport = a.read(5)
		os.system("rm /home/gw/DragonStackServer2.0/KVM/"+ip+":"+str(lport))
		#dport = os.popen(NAT_shell).read()
		print "NAT success!"
		return dport
	except Exception, e:
		print str(e),"read dport failed!"
		return None

#修改虚拟机密码
def updateVmPassword(os_type,vm_ip,password):
	if os_type==1 or os_type==4 :
		shell = "/usr/tcl/bin/expect linux_password.exp %s %s %s %s" % (ubunbu_user,oldpassword,vm_ip,password)
		os.system(shell)
		os.system("rm ~/.ssh/known_hosts")
	if os_type==2 or os_type==3 :
		shell = "/usr/tcl/bin/expect windows_password.exp %s %s %s %s" % (windows_user,oldpassword,vm_ip,password)
		os.system(shell)
	if os_type==5:
		shell = "/usr/tcl/bin/expect centos_password.exp %s %s %s %s" % (centos_user,oldpassword,vm_ip,password)
		os.system(shell)
		os.system("rm ~/.ssh/known_hosts")

def sendMail(user_id,lport,gw_ip,dport,password):
	db = DealDB.DB_doing()
	user_name,email,passwd = db.select_user(user_id)
	title = "--欢迎使用虚拟云主机--"
	os_name = ""
	os_info = ""
	if lport==22:
		os_name="ubuntu/centos"
		os_info="linux远程客户端软件"
	if lport==3389:
		os_info="windows远程桌面工具"
		os_name="Administrator"
	ip_port = gw_ip+":"+dport
	content = "尊敬的%s用户，你申请的虚拟机现已审核通过，请通过%s连接。\nIP:PORT为%s。\n用户名：%s        密码：%s\n如果使用有问题，请通过平台网址 http://222.25.188.1/cloudv2 登录查看相关说明！\n如有任何问题和意见，欢迎>    联系！谢谢！" % (user_name,os_info,ip_port,os_name,password)
	message = "echo \"%s\" | mailx -v -s \"%s\" %s" % (content,title,email)
	os.system(message)

def webproxy(vm_ip,server_ip,vnc_port):
	proxy = "sudo python /var/www/html/noVNC/webproxy.py %s %s %s" % (vm_ip,server_ip,vnc_port)
	os.system(proxy)

#判断虚拟机远程端口是否打开
def checkRemotePort(vm_ip,lport):
	sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sk.settimeout(3)
	#print sk
	try:
		sk.connect((vm_ip,lport))
		print 'Server port '+ str(lport)+' OK!'
		sk.close()
		return True
	except Exception,e:
		#print str(e)	
		return False

#按配置创建新虚拟机
def new_vm(region,os_type,cpu_cores,mem_size,new_disk,password,vm_id,nid,user_id,lid):
	server_ip = find_server(region,cpu_cores,mem_size,new_disk,os_type)
	print server_ip
	if not server_ip:
		log.MyLog("can not find kvmserver to create vm!!")
		return 
	serverid,gw_ip = find_serverid(region,server_ip)
	
  	svr = ServerProxy("http://"+server_ip+":8888")

	vm_lable = ""
	vm_template = ""
	os_type = int(os_type)
	lport = 0
	
	if os_type==2:
		vm_lable = "windows-"+str(vm_id)
		vm_template = "Windows-template"
		lport = 3389
	
	if os_type==5:
		vm_lable = "centos-"+str(vm_id)
		vm_template = "Centos-template"
		lport = 22
	if os_type==1:
		vm_lable = "ubuntu-desktop-"+str(vm_id)
		vm_template = "Ubuntu-template"
		lport = 22
    
	#扩展其他类型虚拟机

	if vm_template=="" or vm_lable=="" or lport==0:
		print "ostype input error!"
		return 
	vm_uuid = ""
	vm_ip = ""
	vnc_port = ""
	try:	
		#创建虚拟机
		vm_uuid,vm_ip,vnc_port = svr.createVM(vm_template,vm_lable,cpu_cores,mem_size,new_disk)

	except Exception,e:
		log.MyLog(str(e))		

	vm_ip = vm_ip.strip()
	print vm_uuid,vm_ip,vnc_port
	#vm_ip = raw_input("please input vm ip_address: ")
	print "vm ip_address is : "+vm_ip

	dport = NAT(vm_ip,lport)

	print vm_ip,lport
	print type(vm_ip),type(lport)
	while checkRemotePort(vm_ip,lport)==False:
		pass

	updateVmPassword(os_type,vm_ip,password)
	webproxy(vm_ip,server_ip,vnc_port)
	
        db = DealDB.DB_doing()
	db.update_vm(vm_uuid,vm_lable,vm_ip,serverid,vm_id)	
        db.update_vmlist(lid,dport,vm_ip,gw_ip,lport)
	db.update_new_apply(nid)
	
	sendMail(user_id,lport,gw_ip,dport,password)

if __name__ == '__main__':
	#接受客户端发来的vm参数，进行创建虚拟机

	vm_param = sys.argv[1]
	vm_param = vm_param.split("|")

	new_vm(vm_param[0],vm_param[1],vm_param[2],vm_param[3],vm_param[4],vm_param[5],vm_param[6],vm_param[7],vm_param[8],vm_param[9]);

	

