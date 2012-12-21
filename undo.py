#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
import global_var

def undoListStore(listUndo,action,value,data1,data2):
    #print 'Undo Select len of undo ' + str(len(listUndo))
    keepData = [action,value,data1,data1]
    listUndo.insert(0,keepData)
    lenOfUndo = len(listUndo)
    if lenOfUndo > 20 :
        del listUndo[20:lenOfUndo]
    #print listUndo[0][0:2]
    return True
    