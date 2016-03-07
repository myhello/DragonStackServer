#include "VmServer.h"


pthread_mutex_t  VmServer::mutex = PTHREAD_MUTEX_INITIALIZER;

VmServer* VmServer::pInstance = 0;

VmServer::VmServer(){}

//单例模式VmServer
VmServer* VmServer::Instantialize()   {
    if(pInstance == NULL)   {      //如果对象已存在不需要加锁了
        //加锁
        Lock lock(mutex);    
        //双重检查
        if(pInstance == NULL)   {
            pInstance = new VmServer();
            cout<<"VmServer created successfully!"<<endl;
        }
    }
    return pInstance;
}

//创建虚拟机
void VmServer::createVm(char *data)
{
    char proxy[100];
    sprintf(proxy,"sudo python python/new_vm.py %s",data);
    system(proxy);
}

//NAT端口转发
void VmServer::natServer(char *data,DbServer* dbServer)
{
    NAT(data,dbserver);
}

//回收虚拟机
void VmServer::recyVm(char *data)
{
    char proxy[100];
    sprintf(proxy,"sudo python python/Recy_vm.py %s",data);
    system(proxy);
}

//更新虚拟机配置
void VmServer::updateVm(char *data)
{
    char proxy[100];
    sprintf(proxy,"sudo python python/update_vm.py %s",data);
    system(proxy);
}
