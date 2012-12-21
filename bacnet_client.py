#!/usr/bin/env python

from twisted.spread import pb
from twisted.internet import reactor
from twisted.python import util
import time

class bacnet_read_tag():
    def read_tag(self,input):
        
        factory = pb.PBClientFactory()
        reactor.connectTCP("localhost", 8008, factory)
        d = factory.getRootObject()
        d.addCallback(lambda object: object.callRemote("echo", "input"))#lambda object: object.callRemote("echo", input)
        d.addCallback(lambda echo: 'server echoed: '+echo)
        d.addErrback(lambda reason: 'error: '+str(reason.value))
        d.addCallback(util.println)
        d.addCallback(lambda _: reactor.stop())
        reactor.run()
        
    def remote_echo(self, st):

        # Copyright (c) 2009 Twisted Matrix Laboratories.
        # See LICENSE for details.
        '''two = Two()
        factory = pb.PBClientFactory()
        reactor.connectTCP("localhost", 8008, factory)
        def1 = factory.getRootObject()
        def1.addCallback(self.got_obj, two) # hands our 'two' to the callback
        reactor.run()'''
        
    def sendData(self,object):
        object.callRemote("echo", "sompoch")

    '''def got_obj(self,obj, two):
        print "got One:", obj
        print "giving it our two"
        obj.callRemote("takeTwo", two)
        
    def error_connect(self):
        print 'Error on connect' + str(reason.value)
        #lambda reason: 'error: '+str(reason.value)
        
        
class Two(pb.Referenceable):
    def remote_print(self, arg):
        print "Two.print() called with", arg'''
        
        
if __name__ == "__main__":
    #for t in range(1):
    st = bacnet_read_tag()
    st.read_tag('test')
    print st #time.sleep(2)