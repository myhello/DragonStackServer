/*
这是一个服务器入口程序，进行服务器配置和设置执行。
*/

//mainserver.cpp
#include "TcpServer.h"
#include "VmServer.h"
#include "DbServer.h"
#include "TaskQueue.h"
#include <iostream>
using namespace std;

#define  DB_HOST "192.168.0.254"
#define  SERVER_POST 2111
#define  DB_USER "root"
#define  DB_PASSWORD "xidian320"
#define  DATABASE "temp"

pthread_t taskthread;  

TaskQueue taskQueue;  //用于处理客户端发来的任务队列

void* ProcessRequest(void*)
{
  VmServer *vmserver = VmServer::Instantialize();

  DbServer dbserver(DB_HOST,DB_USER,DB_PASSWORD,DATABASE);

  enum VmService{
    CREATE_VM,
    RYCLE_VM,
    UPDATE_VM,
    NAT_VM
  };

  while(true){
	  printf("%d\n",taskQueue.getQsize());
    sleep(5);
  	if (!taskQueue.isEmpty())
  	{
      struct Task* task1 ;
  		taskQueue.dequeue(task1);
  		printf("%d\n",task1->t_id);

  		//判断task->t_id，执行不同的虚拟机服务
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
		    default:
		      break;
  		}
  		//printf("%s\n",task1->t_name);

	  	free(task1);
	  }
  }
  
}


int main(int argc, char *argv[])
{
  printf("pid: %d\n", getpid());

  pthread_create(&taskthread,NULL,ProcessRequest,NULL);

  TcpServer server(3);
  server.AddSignalEvent(SIGINT, TcpServer::QuitCb);
  //timeval tv = {10, 0};
  //server.AddTimerEvent(TestServer::TimeOutCb, tv, false);
  server.SetPort(SERVER_POST);
  server.StartRun();
  printf("done\n");
  
  return 0;
}
