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

//执行sql函数
int DbServer::executesql(const char * sql) {
    /*query the database according the sql*/
    printf("%s\n",sql);
    if (mysql_query(&conn, sql)) // 如果失败
        return -1; // 表示失败

    return 0; // 成功执行
}

//执行sql失败
void DbServer::print_mysql_error(const char *msg) { // 打印最后一次错误
    if (msg)
        printf("%s: %s\n", msg, mysql_error(&conn));
    else
        puts(mysql_error(&conn));
}

//插入NAT记录
void DbServer::addNat(char* nat_id,char *dport_str){
    char sql[300];
    int id = atoi(nat_id);
    int dport = atoi(dport_str);
    sprintf(sql,"update other_nat set dport='%d',state=1 where id='%d'",dport,id);    
    if(executesql(sql))
        print_mysql_error(NULL);
    else
        printf("insert other_nat success! \n");
}

//检测数据库连接，断开则重连
void DbServer::checkConn()
{
	if(!mysql_ping(&conn)){
		printf("mysql connecting normal!\n");
		return ;
	}else{
		printf("mysql conn have been close!\n"); 		 
		db_connect();
	}
}

//其他数据库操作函数
//
//

