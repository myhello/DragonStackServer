#include "NAT.h"

char* getdport(const char* confpath)
{
    FILE *fp;
    char *a = new char[6];    
    if((fp=fopen(confpath,"rt"))==NULL)
    {
        cout<<"Cannot open file!"<<endl;
        return a;
    }
    fgets(a,6,fp);
    return a;
}


void NAT(char* buffer,DbServer *dbserver)
{
	//从接收到的数据中获取ip和port信息，调用shell处理
    const char* d = "|";
    char *temp ;
    char *ip ;
    char *lport ;
    char *nat_id ;
    int count = 0;
    temp = strtok(buffer,d);
    while(temp){
        count++;
    	switch(count){
		    case 1:ip = temp; break;
	        case 2:lport = temp; break; 
	        case 3:nat_id = temp; break;
	        default: break;
		}
        temp = strtok(NULL,d);
    }
    char *nat = new char[50];
    sprintf(nat,"shell/addNAT1.sh %s %s",ip,lport);
    system(nat);
    //读取配置文件中的dport信息，准备发送
    char *dport_str = new char[BUF_SIZE];
    dport_str = getdport("shell/dport.conf");
    //sprintf(dport_str,"%d",dport);
    cout<<dport_str<<"------------------"<<endl;


    //将转发记录写入数据库
    dbserver->addNat(nat_id,dport_str);


    //将转发记录写入到数据库

}
