#!/usr/bin/python
from elementtree import ElementTree
import elementtree.ElementTree as ET
from elementtree.ElementTree import Element
#open file
svgobj = ET.parse('/home/sompoch/Pictures/SVG/Broom_icon.svg') #python-logo-generic.svg ,Broom_icon.svg,gradiant.svg
# get toplevel element
rootx = svgobj.getroot()
elementsx = rootx.getchildren()
for j in elementsx:
    #print str(type(j))
    #print j.text
    tag_id = j.tag
    t_pos = tag_id.find('}')
    print tag_id[t_pos+1:]
    print j.items()
    v = j.getchildren()
    for k in v:
        #print k.tag
        
        tag_id = k.tag
        t_pos = tag_id.find('}')
        print tag_id[t_pos+1:]
        print "--->", k.items()
        h = k.getchildren()
        for c in h:
            print c.tag
            print  "      |--->",c.items()#,
            b = c.getchildren()
            for n in b:
                tag_id = n.tag
                t_pos = tag_id.find('}')
                print tag_id[t_pos+1:]
                print  "            |--->",n.items()#,
                list1 = n.items()
                
                #print "Find height ",list1.find('height')
                #


#defsx = elementsx[0]
#elementsx = defsx.getchildren()
#yellowelement = elementsx[0]
'''for defsa
for i in defsx:
    v = i.getchildren()
    #print v
    for k in v:
        print k.items()'''
#blueelement = elementsx[1]