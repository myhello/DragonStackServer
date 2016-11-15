#include "XenServer.h"


pthread_mutex_t  XenServer::mutex = PTHREAD_MUTEX_INITIALIZER;

XenServer* XenServer::pInstance = 0;

XenServer::XenServer(){}

XenServer::~XenServer(){}

//单例模式VmServer
XenServer* XenServer::Instantialize()   {
    if(pInstance == NULL)   {      //如果对象已存在不需要加锁了
        //加锁
        Lock lock(mutex);    
        //双重检查
        if(pInstance == NULL)   {
            pInstance = new XenServer();
            cout<<"XenServer created successfully!"<<endl;
        }
    }
    return pInstance;
}

//创建进程去调用python的xenserver接口

//创建虚拟机
void XenServer::createVm(char *data)
{
    char proxy[100];
    sprintf(proxy,"python new_vm.py \"%s\"",data);
    system(proxy);
    //pid_t pid;
    //cout<<data<<endl;
	/*
    pid = fork();
    if (pid==0)
    {
        execlp("python/new_vm.py","python/new_vm.py",data,NULL);
        perror("python/new_vm.py");
        exit(errno);
    }else{
        pid = waitpid(pid,NULL,0);
        printf("child process return %d\n",pid);
    }*/
}

//NAT端口转发
void XenServer::natServer(char *data,DbServer* dbServer)
{
   NAT(data,dbServer);
}

//回收虚拟机
void XenServer::recyVm(char *data)
{
    //cout<<data<<endl;
    char proxy[100];
    sprintf(proxy,"python Recy_vm.py \"%s\"",data);
    system(proxy);
    //pid_t pid;
    /*
    pid = fork();
    if (pid==0)
    {
        execlp("python/Recy_vm.py","python/Recy_vm.py",data,NULL);
        perror("python/Recy_vm.py");
        exit(errno);
    }else{
        pid = waitpid(pid,NULL,0);
        printf("child process return %d\n",pid);
    }*/
}

//更新虚拟机配置
void XenServer::updateVm(char *data)
{
    //cout<<data<<endl;
    char proxy[100];
    sprintf(proxy,"python update_vm.py \"%s\"",data);
    system(proxy);
    //pid_t pid;
    /*
    pid = fork();
    if (pid==0)
    {
        execlp("python/update_vm.py","python/update_vm.py",data,NULL);
        perror("python/update_vm.py");
        exit(errno);
    }else{
        pid = waitpid(pid,NULL,0);
        printf("child process return %d\n",pid);
    }*/
}

//关闭锁定虚拟机
void XenServer::LockVM(char *data)
{
	char proxy[100];
	sprintf(proxy,"python shutdown.py \"%s\"",data);
	system(proxy);
}

//解锁开启虚拟机
void XenServer::UnlockVM(char *data)
{
	char proxy[100];
	sprintf(proxy,"python startup.py \"%s\"",data);
	system(proxy);
}
