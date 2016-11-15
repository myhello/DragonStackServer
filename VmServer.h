#ifndef _VMSERVER_H
#define _VMSERVER_H

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

class Lock  {
    private:
        pthread_mutex_t m_lock;
    public:
        Lock(pthread_mutex_t  cs) : m_lock(cs) {
            pthread_mutex_lock(&m_lock);
        }
        ~Lock() {
            pthread_mutex_unlock(&m_lock);
        }
};
//锁类，避免多线程操作虚拟机同步的错误//虚拟机所有接口

class VmServer
{

public:
	VmServer(){};

	VmServer(const VmServer&);
	VmServer& operator=(const VmServer&);
	/* data */


	//创建虚拟机
	virtual void createVm(char *test)=0;

	//NAT端口映射服务
	virtual void natServer(char *data,DbServer* dbServer)=0;

	//回收虚拟机
	virtual void recyVm(char *data)=0;

	//更新虚拟机配置
	virtual void updateVm(char *data)=0;

	//关闭锁定虚拟机
	virtual void LockVM(char *data)=0;
	
	//解锁开启虚拟机
	virtual void UnlockVM(char *data)=0;

	//多态析构
	virtual ~VmServer(){};
};

#endif
