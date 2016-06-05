#ifndef _CONFIG_H
#define _CONFIG_H

#include <iostream>
#include <fstream>

using namespace std;

class config{
        string dbserver_ip;
        int server_port;

public:
        friend istream& operator>>(istream& i,config& p);
        friend ostream& operator<<(ostream& o,const config& p);
        string getDBServerIp();
        int getServerPort();
};

#endif
