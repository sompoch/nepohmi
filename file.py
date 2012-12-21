import os

f = open(r'configure/color_palette.cfg')
lines=[]
for i in range(4):
    lines.append(f.readline())
    c = lines[i].replace('\'',"")
    c = c.replace('\n',"")
    c =c.split(',')
    print c[5]
f.close()
#print lines
'''lines[1] = "isn't a\n"
f = open(r'configure/color_palette.cfg', 'w')
f.writelines(lines)
f.close()'''