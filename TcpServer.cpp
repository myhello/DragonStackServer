/*
这是一个基于libevent的网络服务器程序，进行网络TCP服务器初始化工作。
*/

//TcpServer.cpp
#include "TcpServer.h"
#include "TaskQueue.h"

CMutex g_tcpLock;

char buffer[100];      //接受数据缓冲区

char lastBuffer[100]={'1'};   //重复命令去重比较

extern TaskQueue taskQueue;  //用于处理客户端发来的任务队列

void TcpServer::ReadEvent(Conn *conn)
{
  CMyLock lock(g_tcpLock);
  //char buffer[6];
  memset(buffer, 0,100); 

  int len = conn->GetReadBufferLen();
  //cout<<len<<endl;  

  conn->GetReadBuffer(buffer, len);
  cout<<buffer<<endl;

  if(strcmp(buffer,lastBuffer)==0){
      cout<<"double order !!"<<endl;
      return ;	
  }else{
      memset(lastBuffer,0,100);
      strcpy(lastBuffer,buffer);
  }


  struct Task* task = (struct Task*)malloc(sizeof(struct Task));

  //解析客户端发来的数据包"0#1#ab|cd|ef"
  char delims[]="#";
  char *result=NULL;
  result=strtok(buffer,delims);
  char *TRGN = result;
  if (result != NULL)
  {            
      result = strtok(NULL, delims);
  }else{
      cout<<"error task!..."<<endl;
      return ;
  }
  //cout<<11111111111111<<endl;
  char *TID = result; 
  if (result!=NULL)
  {
     task->t_id = atoi(TID);
     task->t_region = atoi(TRGN);
     result = strtok(NULL,delims);
     if(result==NULL){
	cout<<"error task!..."<<endl;
        return ;
     }
     strcpy(task->t_data,result);
  }else{
     cout<<"error task!..."<<endl;
     return ;
  }

  taskQueue.enqueue(task);

  //cout<<conn->GetReadBufferLen()<<endl;
}

void TcpServer::WriteEvent(Conn *conn)
{

}

void TcpServer::ConnectionEvent(Conn *conn)
{
  TcpServer *me = (TcpServer*)conn->GetThread()->tcpConnect;
  printf("new connection: %d\n", conn->GetFd());
  me->vec.push_back(conn);
}

void TcpServer::CloseEvent(Conn *conn, short events)
{
  printf("connection closed: %d\n", conn->GetFd());
}

void TcpServer::QuitCb(int sig, short events, void *data)
{ 
  printf("Catch the SIGINT signal, quit in one second\n");
  TcpServer *me = (TcpServer*)data;
  timeval tv = {1, 0};
  me->StopRun(&tv);
}

/*
void TcpServer::TimeOutCb(int id, short events, void *data)
{
  TcpServer *me = (TcpServer*)data;
  char temp[33] = "hello, world\n";
  for(int i=0; i<me->vec.size(); i++)
    me->vec[i]->AddToWriteBuffer(temp, strlen(temp));
}
*/
