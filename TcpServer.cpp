/*
这是一个基于libevent的网络服务器程序，进行网络TCP服务器初始化工作。
*/

//TcpServer.cpp
#include "TcpServer.h"
#include "TaskQueue.h"

CMutex g_tcpLock;

char buffer[50];      //接受数据缓冲区

extern TaskQueue taskQueue;  //用于处理客户端发来的任务队列

void TcpServer::ReadEvent(Conn *conn)
{
  CMyLock lock(g_tcpLock);
  //char buffer[6];
  memset(buffer, 0, strlen(buffer));
  conn->GetReadBuffer(buffer, 50);

  struct Task* task = (struct Task*)malloc(sizeof(struct Task));

  //解析客户端发来的数据包"1#ab|cd|ef"
  char delims[]="#";
  char *result=NULL;
  result=strtok(buffer,delims);
  if (result!=NULL)
  {
     task->t_id = atoi(result);
     result = strtok(NULL,delims);
     strcpy(task->t_data,result);
  }

  taskQueue.enqueue(task);

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
