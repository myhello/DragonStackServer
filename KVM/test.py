#!/usr/bin/python

import socket
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.settimeout(1)
try:
  sk.connect(('192.168.0.253',3389))
  print 'Server port 80 OK!'
except Exception:
  print 'Server port 80 not connect!'
sk.close()
