#!/bin/bash
kill -9 `ps -ef | grep "python KVMServer" | grep -v "grep" | awk '{print $2}'`
