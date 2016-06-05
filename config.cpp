#include "config.h" 

istream& operator>>(istream& i,config &p)
{
	i>>p.dbserver_ip>>p.server_port;
	return i;
}

ostream& operator<<(ostream& o,const config& p)
{
	o<<"dbserver_ip: "<<p.dbserver_ip<<" server_port: "<<p.server_port;
	return o;
}

string config::getDBServerIp(){
	return dbserver_ip;
}

int config::getServerPort(){
	return server_port;
}
