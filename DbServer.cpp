#include "DbServer.h"

DbServer::DbServer(const char *d_host,const char *d_user,const char *d_password,const char *d_name):db_host(d_host),db_user(d_user),db_password(d_password),db_name(d_name)
{
    db_connect();
}

DbServer::~DbServer(){
	mysql_close(&conn);
}

//连接数据库服务器
void DbServer::db_connect(){
    mysql_init(&conn);
    if(mysql_real_connect(&conn,db_host,db_user,db_password,db_name,0,NULL,CLIENT_FOUND_ROWS))  
    {
        printf("DB connect success...\n");
        mysql_query(&conn, "set names utf8");
    }
    else{
        printf("DB connect failed...\n");
    }
}
