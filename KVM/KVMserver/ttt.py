#!/usr/bin/env python
import os,libvirt,sys
from xml.dom.minidom import parseString
from SimpleXMLRPCServer import SimpleXMLRPCServer

def startVM(vm_label):
    shell = 'virsh start '+vm_label
    os.system(shell)

def shutdownVM(vm_label):
    shell = 'virsh destroy '+vm_label
    os.system(shell)
svr = SimpleXMLRPCServer(("",9999),allow_none=True)
svr.register_function(startVM)
svr.register_function(shutdownVM)

svr.serve_forever()
