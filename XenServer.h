#ifndef _XENSERVER_H
#define _XENSERVER_H

#include "NAT.h"
#include "DbServer.h"
#include <unistd.h>
#include <pthread.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <iostream>

#include "VmServer.h"

using namespace std;

class XenServer:public VmServer
{
private:
        XenServer();
	XenServer(const XenServer&);
	XenServer& operator=(const XenServer&);

public:
	static XenServer *Instantialize();
        static XenServer *pInstance;
        static pthread_mutex_t  mutex;

	//创建虚拟机
	virtual void createVm(char *test);

	//NAT端口映射服务
	virtual void natServer(char *data,DbServer* dbServer);

	//回收虚拟机
	virtual void recyVm(char *data);

	//更新虚拟机配置
	virtual void updateVm(char *data);

	//关闭锁定虚拟机
	virtual void LockVM(char *data);
	
	//解锁开启虚拟机
	virtual void UnlockVM(char *data);

	~XenServer();

	/* data */
};

#endif
