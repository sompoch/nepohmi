#!/usr/bin/env python

# Copyright (c) 2009 Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.spread import pb
from twisted.internet import reactor
from twisted.python import util

class Two(pb.Referenceable):
    def remote_print(self, arg):
        print "Two.print() called with", arg

def main():
    two = Two()
    factory = pb.PBClientFactory()
    reactor.connectTCP("localhost", 8008, factory)
    def1 = factory.getRootObject()
    def1.addCallback(lambda object: object.callRemote("echo", "input")) # hands our 'two' to the callback
    def1.addCallback(lambda echo: 'server echoed: '+echo)
    def1.addCallback(util.println)
    def1.addCallback(lambda _: reactor.stop())
    reactor.run()

def get_data():
    util.println

main()