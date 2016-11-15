server:NAT.o DbServer.o KvmServer.o XenServer.o TcpEventServer.o TcpServer.o mainserver.o config.o Lock.o TaskQueue.o
	g++ -g -o server NAT.o mainserver.o DbServer.o TcpEventServer.o TcpServer.o config.o KvmServer.o XenServer.o Lock.o TaskQueue.o -lpthread -levent -I/usr/include/mysql -L/usr/lib64/mysql -lmysqlclient 

DbServer.o:DbServer.cpp DbServer.h
	g++ -c DbServer.cpp -I/usr/include/mysql -L/usr/lib64/mysql -lmysqlclient

Lock.o:Lock.cpp Lock.h
	g++ -c Lock.cpp

NAT.o:NAT.cpp NAT.h 
	g++ -c NAT.cpp -I/usr/include/mysql -L/usr/lib64/mysql -lmysqlclient

TaskQueue.o:TaskQueue.cpp TaskQueue.h
	g++ -c TaskQueue.cpp

TcpServer.o:TcpServer.cpp TcpServer.h TcpEventServer.h VmServer.h Lock.h TaskQueue.h
	g++ -c TcpServer.cpp TcpEventServer.cpp Lock.cpp -I/usr/include/mysql -L/usr/lib64/mysql -lmysqlclient -levent 

KvmServer.o:KvmServer.cpp VmServer.h KvmServer.h NAT.h 
	g++ -c KvmServer.cpp  NAT.cpp  -I/usr/include/mysql -L/usr/lib64/mysql -lmysqlclient

XenServer.o:XenServer.cpp VmServer.h XenServer.h NAT.h 
	g++ -c XenServer.cpp  NAT.cpp  -I/usr/include/mysql -L/usr/lib64/mysql -lmysqlclient

mainserver.o:mainserver.cpp DbServer.h TcpServer.h VmServer.h config.h config.cpp KvmServer.h XenServer.h
	g++ -c mainserver.cpp config.cpp -I/usr/include/mysql -L/usr/lib64/mysql -lmysqlclient

clean:
	rm NAT.o DbServer.o KvmServer.o XenServer.o TcpEventServer.o config.o TcpServer.o mainserver.o Lock.o TaskQueue.o server
