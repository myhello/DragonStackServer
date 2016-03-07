server:DbServer.o VmServer.o TcpEventServer.o TcpServer.o mainserver.o Lock.o TaskQueue.o
	g++ -g -o server mainserver.o DbServer.o TcpEventServer.o TcpServer.o VmServer.o Lock.o TaskQueue.o -lpthread -levent -I/usr/include/mysql -L/usr/lib64/mysql -lmysqlclient 

DbServer.o:DbServer.cpp DbServer.h
	g++ -c DbServer.cpp -I/usr/include/mysql -L/usr/lib64/mysql -lmysqlclient

Lock.o:Lock.cpp Lock.h
	g++ -c Lock.cpp

TaskQueue.o:TaskQueue.cpp TaskQueue.h
	g++ -c TaskQueue.cpp

TcpServer.o:TcpServer.cpp TcpServer.h TcpEventServer.h VmServer.h Lock.h TaskQueue.h
	g++ -c TcpServer.cpp TcpEventServer.cpp Lock.cpp 

VmServer.o:VmServer.cpp VmServer.h
	g++ -c VmServer.cpp

mainserver.o:mainserver.cpp DbServer.h TcpServer.h VmServer.h
	g++ -c mainserver.cpp -I/usr/include/mysql -L/usr/lib64/mysql -lmysqlclient

clean:
	rm DbServer.o VmServer.o TcpEventServer.o TcpServer.o mainserver.o Lock.o TaskQueue.o server
