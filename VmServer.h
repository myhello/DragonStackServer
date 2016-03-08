#ifndef _VMSERVER_H
#define _VMSERVER_H

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

using namespace std;

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
//锁类，避免多线程操作虚拟机同步的错误

class VmServer
{
private:
	VmServer();
	VmServer(const VmServer&);
	VmServer& operator=(const VmServer&);

public:
	static VmServer *Instantialize();
    static VmServer *pInstance;
    static pthread_mutex_t  mutex;

	//创建虚拟机
	void createVm(char *test);

	//NAT端口映射服务
	void natServer(char *data,DbServer* dbServer);

	//回收虚拟机
	void recyVm(char *data);

	//更新虚拟机配置
	void updateVm(char *data);

	~VmServer();

	/* data */
};

#endif
