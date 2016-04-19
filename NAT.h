#ifndef _NAT_H
#define _NAT_H

#include "DbServer.h"
#include <iostream>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <string>
#include <string.h>
#include <stdlib.h>
using namespace std;

void NAT(char* buffer,DbServer *dbserver);

char* getdport(const char* confpath);

#define BUF_SIZE 1024
#endif
