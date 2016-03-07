#include <stdlib.h>  
#include <stdio.h>  
#include <errno.h>  
#include <string.h>  
#include <unistd.h>  
#include <netdb.h>  
#include <sys/socket.h>  
#include <netinet/in.h>  
#include <sys/types.h>  
#include <arpa/inet.h>  
  
int main(int argc, char *argv[])  
{  
    int sockfd;  
    char buffer[1024];  
    struct sockaddr_in server_addr;  
    struct hostent *host;  
    int portnumber,nbytes;  

    if((host=gethostbyname("localhost"))==NULL)  
    {  
            fprintf(stderr,"Gethostname error\n");  
            exit(1);  
    }  

    if((portnumber=atoi("2111"))<0)  
    {  
            fprintf(stderr,"Usage:%s hostname portnumber\a\n",argv[0]);  
            exit(1);  
    }  

    /* 客户程序开始建立 sockfd描述符  */  
    if((sockfd=socket(AF_INET,SOCK_STREAM,0))==-1)  
    {  
            fprintf(stderr,"Socket Error:%s\a\n",strerror(errno));  
            exit(1);  
    }  

    /* 客户程序填充服务端的资料       */  
    bzero(&server_addr,sizeof(server_addr));  
    server_addr.sin_family=AF_INET;  
    server_addr.sin_port=htons(portnumber);  
    server_addr.sin_addr=*((struct in_addr *)host->h_addr);  

    /* 客户程序发起连接请求         */  
    if(connect(sockfd,(struct sockaddr *)(&server_addr),sizeof(struct sockaddr))==-1)  
    {  
            fprintf(stderr,"Connect Error:%s\a\n",strerror(errno));  
            exit(1);  
    }  
  	char buff[] = "hello";
    /* 连接成功了           */ 
    int t = 3; 
    while(t--)
	{
        send(sockfd, buff, 5, 0);
	    //if((nbytes=read(sockfd,buffer,1024))==-1)  
        //{  
        //        fprintf(stderr,"Read Error:%s\n",strerror(errno));  
        exit(1);  
        //}  
        //buffer[nbytes]='\0';  
        //printf("I have received:%s\n",buffer);  
        //sleep(5);	
	}
    sleep(10);
    /* 结束通讯     */  
    close(sockfd);  
    exit(0);  
}  
