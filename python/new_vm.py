#-*- encoding:UTF-8 -*-
import os
import xen
import socket
import time
import thread
import DealDB
import json

#xenserver的默认用户名和密码
user = "root"
pwd = "123456"
centos_user = 'centos'
ubunbu_user = 'ubuntu'
windows_user = 'Administrator'
oldpassword = 'Xidian320'


#从数据库找出某域所有xenserver的ip
def find_all_xenservers(region):
	db = DealDB.DB_doing()
	xenserverips = []
	xenserveripslist = db.getServerips(region)
	for item in xenserveripslist:
		xenserverips.append(item[0])
	return xenserverips

def find_serverid(region,serverip):
	db = DealDB.DB_doing()
	serverid = db.getServerId(region,serverip)
        return serverid

#判断某个xenserver是否剩余了满足创建虚拟机的配置量
def canCreateVm(xenserver,cpu_cores,mem_size,new_disk,os_type):
	os_type = int(os_type)
	vm_template = ""
	if os_type==1:
		vm_template = "My Ubuntu Template"
	if os_type==2:
		vm_template = "My Windows Template"
	if os_type==3:
		vm_template = "My Windows Server Template"
	if os_type==4:
		vm_template = "My Ubuntu Server Template"
	if os_type==6:
		vm_template = "My Centos Template"
	if xenserver.hasTemplate(vm_template):
		live,free_memory,free_disk = xenserver.freeDeploy()
		if live:
			if free_memory>int(mem_size)*1024*1024 and free_disk>int(new_disk)*1024*1024*1024:
				return True
			else:
                print "free deploy is not enough"
				return False
		else:
			return False
	else:
		print "can not find template!"
		return False

#轮训所有服务器，找到适合创建client传来参数虚拟机的xenserver服务器的ip 
def find_xenserver(region,cpu_cores,mem_size,new_disk,os_type):
	xenserver_ips = find_all_xenservers(region)
	url = ''
	for xenserver_ip in xenserver_ips:
		url = "http://" + xenserver_ip
		try:
			xenserver = xen.Xen(url,user,pwd)   #如果server连不上，连下一个server
			if canCreateVm(xenserver,cpu_cores,mem_size,new_disk,os_type):
				return xenserver_ip
		except Exception, e:
			continue
	return None

#调用shell脚本进行NAT转发，返回dport
def NAT(ip,lport):
	os.system("shell/addNAT.sh "+ip+" "+str(lport))
	try:
		with open(ip+":"+str(lport),"rb") as a:
			dport = a.read(5)
		os.system("rm "+ip+":"+str(lport))
		print "NAT success!"
		return dport
	except Exception, e:
		print str(e),"read dport failed!"
		return None

#修改虚拟机密码
def updateVmPassword(os_type,vm_ip,password):
	if os_type==1 or os_type==4 :
		shell = "/usr/tcl/bin/expect expect/linux_password.exp %s %s %s %s" % (ubunbu_user,oldpassword,vm_ip,password)
		os.system(shell)
	if os_type==2 or os_type==3 :
		shell = "/usr/tcl/bin/expect expect/windows_password.exp %s %s %s %s" % (windows_user,oldpassword,vm_ip,password)
		os.system(shell)
	if os_type==6:
		shell = "/usr/tcl/bin/expect expect/centos_password.exp %s %s %s %s" % (centos_user,oldpassword,vm_ip,password)


#将需要发送的数据封装为json
def dataToJson(ip,vm_uuid,vm_lable,lport,dport,serverid):
	result={}
	result['vm_uuid'] = vm_uuid
	result['vm_lable'] = vm_lable
	result['ip'] = ip
	result['lport'] = lport
	result['dport'] = dport
	result['serverid'] = serverid
	return json.dumps(result)


#按配置创建新虚拟机
def new_vm(region,os_type,cpu_cores,mem_size,new_disk,password,vm_id):
	server_ip = find_xenserver(region,cpu_cores,mem_size,new_disk,os_type)
	if not server_ip:
		print 'can not create vm !'
		return 
	serverid = find_serverid(region,server_ip)

	url = "http://" + server_ip

	fields = {}
	fields['description'] = 'my_os'
	fields['cpu_cores'] = int(cpu_cores)
	fields['backup'] = False
	fields['mem_size'] = int(mem_size)/1024
	List_tags = ['os','']
	fields['tags'] = List_tags
	new_disk = int(new_disk)*1024*1024*1024
    print fields
	xenserver = xen.Xen(url,user,pwd)

	vm_lable = ""
	vm_template = ""
	os_type = int(os_type)
	lport = 0
	if os_type==1:
		vm_lable = "ubuntu-desktop-"+str(vm_id)
		vm_template = "My Ubuntu Template"
		lport = 22
	if os_type==2:
		vm_lable = "windows7-"+str(vm_id)
		vm_template = "My Windows Template"
		lport = 3389
	if os_type==3:
		vm_lable = "windows-server-"+str(vm_id)
		vm_template = "My Windows Server Template"
		lport = 3389
	if os_type==4:
		vm_lable = "ubuntu-server-"+str(vm_id)
		vm_template = "My Ubuntu Server Template"
		lport = 22
	if os_type==6:
		vm_lable = "centos"+str(vm_id)
		vm_template = "My Centos Template"
		lport = 22
      
	if vm_template=="" or vm_lable=="" or lport==0:
		print "ostype input error!"
		return 

	vm_uuid,vm_ref = xenserver.vm_template_copy(vm_template,vm_lable)
    #print vm_uuid,vm_ref
	xenserver.update_disk(vm_uuid,str(new_disk))
	xenserver.vm_update(vm_uuid,fields)

	while xenserver.read_ip_address(vm_ref) == None or not(xenserver.read_ip_address(vm_ref).startswith('192.168.0')): time.sleep(1)
	print "vm create success！Reported IP: ", xenserver.read_ip_address(vm_ref)

	dport = NAT(xenserver.read_ip_address(vm_ref),lport)
 
    #目前windows的改密码程序不能退出啊	
    updateVmPassword(os_type,xenserver.read_ip_address(vm_ref),password)

    result = dataToJson(xenserver.read_ip_address(vm_ref),vm_uuid,vm_lable,lport,dport,serverid)
    print "send result data:"
    print result


if __name__ == '__main__':
	#创建tcp监听服务器，接受客户端发来的vm参数，开启线程进行创建，返回的参数回送给client进行数据库添加

	vm_param = sys.argv[1]
	vm_param = vm_param.split("|")

	new_vm(vm_param[0],vm_param[1],vm_param[2],vm_param[3],vm_param[4],vm_param[5],vm_param[6]);

	

