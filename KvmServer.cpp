#include "KvmServer.h"


pthread_mutex_t  KvmServer::mutex = PTHREAD_MUTEX_INITIALIZER;

KvmServer* KvmServer::pInstance = 0;

KvmServer::KvmServer(){}

KvmServer::~KvmServer(){}

//单例模式VmServer
KvmServer* KvmServer::Instantialize()   {
    if(pInstance == NULL)   {      //如果对象已存在不需要加锁了
        //加锁
        Lock lock(mutex);    
        //双重检查
        if(pInstance == NULL)   {
            pInstance = new KvmServer();
            cout<<"KvmServer created successfully!"<<endl;
        }
    }
    return pInstance;
}

//创建进程去调用Kvmserver接口

//创建虚拟机
void KvmServer::createVm(char *data)
{
    cout<<"createVm data is "<<data<<endl;
    char proxy[100];
    sprintf(proxy,"python KVM/create_vm.py \"%s\"",data);
    system(proxy);
}

//NAT端口转发
void KvmServer::natServer(char *data,DbServer* dbServer)
{
    //NAT(data,dbServer);
    cout<<"NAT data is "<<data<<endl;
    NAT(data,dbServer);
}

//回收虚拟机
void KvmServer::recyVm(char *data)
{
    cout<<"recyVm data is "<<data<<endl;
    char proxy[100];
    sprintf(proxy,"python KVM/Recy_vm.py \"%s\"",data);
    system(proxy);
}

//更新虚拟机配置
void KvmServer::updateVm(char *data)
{
    cout<<"updateVm data is "<<data<<endl;
    char proxy[100];                                       
    sprintf(proxy,"python KVM/update_vm.py \"%s\"",data);
    system(proxy);

 
}

//关闭锁定虚拟机
void KvmServer::LockVM(char *data)
{
	cout<<"LockVM data is "<<data<<endl;
}

//解锁开启虚拟机
void KvmServer::UnlockVM(char *data)
{
	cout<<"UnlockVM data is "<<data<<endl;
}
