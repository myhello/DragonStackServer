#ifndef _TCPSERVER_H
#define _TCPSERVER_H

#include "TcpEventServer.h"
#include "VmServer.h"
#include <set>
#include <vector>
#include <string.h>
#include "Lock.h"


class TcpServer : public TcpEventServer{
private:
  vector<Conn*> vec;

protected:
  //重载各个处理业务的虚函数
  void ReadEvent(Conn *conn);
  void WriteEvent(Conn *conn);
  void ConnectionEvent(Conn *conn);
  void CloseEvent(Conn *conn, short events);
public:
  TcpServer(int count) : TcpEventServer(count) { }
  ~TcpServer() { } 
  
  //退出事件，响应Ctrl+C
  static void QuitCb(int sig, short events, void *data);
  //定时器事件，每10秒向所有客户端发一句hello, world
  //static void TimeOutCb(int id, int short events, void *data);

};

#endif