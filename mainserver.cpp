/*
这是一个服务器入口程序，进行服务器配置和设置执行。
*/

//mainserver.cpp
#include "TcpServer.h"
#include "VmServer.h"
#include "KvmServer.h"
#include "XenServer.h"
#include "DbServer.h"
#include "TaskQueue.h"
#include "config.h"

#define  DB_HOST "localhost"
//#define  SERVER_PORT 10000 
#define  DB_USER "root"
#define  DB_PASSWORD "xidian320"
#define  DATABASE "dscloud"

pthread_t taskthread;  

TaskQueue taskQueue;  //用于处理客户端发来的任务队列

extern CMutex g_tcpLock;

config conf;

void* ProcessRequest(void*)
{
  VmServer *vmserver = NULL;

  DbServer dbserver(conf.getDBServerIp().c_str(),DB_USER,DB_PASSWORD,DATABASE);
  
  enum VmService{
    CREATE_VM,
    RYCLE_VM,
    UPDATE_VM,
    NAT_VM,
	LOCK_USER,
	UNLOCK_USER
  };

  while(true){
	 // printf("%d\n",taskQueue.getQsize());
    sleep(5);
  	if (!taskQueue.isEmpty())
  	{
      
      CMyLock lock(g_tcpLock);

      struct Task* task1 ;
  	  taskQueue.dequeue(task1);
  	  printf("%d\n",task1->t_id);

      lock.~CMyLock();

  		//判断task->t_id，执行不同的虚拟机服务
      if(task1->t_region==0){
          vmserver = KvmServer::Instantialize();
          //vmserver = new KvmServer();
      }else{
          vmserver = XenServer::Instantialize();
          //vmserver = new XenServer();
      }
  		switch( VmService(task1->t_id) ){
		    case CREATE_VM:
			    vmserver->createVm(task1->t_data);
			    break;
			case RYCLE_VM:
			    vmserver->recyVm(task1->t_data);
			    break;
			case UPDATE_VM:
			    vmserver->updateVm(task1->t_data);
			    break;
		    case NAT_VM:
		        vmserver->natServer(task1->t_data,&dbserver);
		        break;
			case LOCK_USER:
				vmserver->LockVM(task1->t_data);
				break;
			case UNLOCK_USER:
				vmserver->UnlockVM(task1->t_data);
				break;
		    default:
		        break;
  		}
  		//printf("%s\n",task1->t_data);

	  	free(task1);
		//应该考虑一下悬垂指针啊
		task1=NULL;

	  }
  }
  
}


int main(int argc, char *argv[])
{
  printf("pid: %d\n", getpid());
  
  ifstream file("server.conf"); 
  file>>conf;
  if(file.fail()){
	cout<<"读取配置文件失败！"<<endl;
	exit(1);
  }
  cout<<conf<<endl;
 
  pthread_create(&taskthread,NULL,ProcessRequest,NULL);

  TcpServer server(3);
  server.AddSignalEvent(SIGINT, TcpServer::QuitCb);
  //timeval tv = {10, 0};
  //server.AddTimerEvent(TestServer::TimeOutCb, tv, false);
  server.SetPort(conf.getServerPort());
  server.StartRun();
  printf("done\n");
  
  return 0;
}
