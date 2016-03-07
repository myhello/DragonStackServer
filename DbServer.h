#ifndef _DBSERVER_H
#define _DBSERVER_H

#include <mysql.h>
#include <stdio.h>

class DbServer
{
public:
	DbServer(const char *d_host,const char *d_user,const char *d_password,const char *d_name);
	~DbServer();
	
	//连接数据库服务器
	void db_connect();

/* data */
private:
	const char *db_user;
	const char *db_password;
	const char *db_host;
	const char *db_name;
	MYSQL conn;
};

#endif