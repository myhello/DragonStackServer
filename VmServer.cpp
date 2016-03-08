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

//创建进程去调用python

//创建虚拟机
void VmServer::createVm(char *data)
{
    //char proxy[100];
    //sprintf(proxy,"sudo python python/new_vm.py %s",data);
    //system(proxy);
    pid_t pid;
    pid = fork();
    if (pid==0)
    {
        /* code */
        execlp("python/new_vm.py","python/new_vm.py",data);
        perror("python/new_vm.py");
        exit(errno);
    }else{
        pid = waitpid(pid,NULL,0);
        printf("child process return %d\n",pid);
    }
}

//NAT端口转发
void VmServer::natServer(char *data,DbServer* dbServer)
{
    NAT(data,dbserver);
}

//回收虚拟机
void VmServer::recyVm(char *data)
{
    //char proxy[100];
    //sprintf(proxy,"sudo python python/Recy_vm.py %s",data);
    //system(proxy);
    pid_t pid;
    pid = fork();
    if (pid==0)
    {
        /* code */
        execlp("python/Recy_vm.py","python/Recy_vm.py",data);
        perror("python/Recy_vm.py");
        exit(errno);
    }else{
        pid = waitpid(pid,NULL,0);
        printf("child process return %d\n",pid);
    }
}

//更新虚拟机配置
void VmServer::updateVm(char *data)
{
    //char proxy[100];
    //sprintf(proxy,"sudo python python/update_vm.py %s",data);
    //system(proxy);
    pid_t pid;
    pid = fork();
    if (pid==0)
    {
        /* code */
        execlp("python/update_vm.py","python/update_vm.py",data);
        perror("python/update_vm.py");
        exit(errno);
    }else{
        pid = waitpid(pid,NULL,0);
        printf("child process return %d\n",pid);
    }
}
