#/bin/local/python 
import sqlite3 as lite
import os,sys
import time
import pyroweb_client
import subprocess
import pickle


def get_data(document_database):
    host = {}

    #FROM HOST 
    database_name = "tag.db"
    con = lite.connect(database_name)
    cur = con.cursor()
    query = "select * from HOST;"
    cur.execute(query)
    result = cur.fetchall()
    #print result


    for h in result:
        opc_list= []
        host[h[1]] = h[0],h[2],h[3],opc_list
        #host{alias_name} = host_id,real_ip , port , opc server list_all 


    database_name = "tag.db"
    con = lite.connect(database_name)
    cur = con.cursor()
    #FROM OPC_SERVER_NAME
    for u in host:
        #print host[u][3]
        h_id = host[u][0]
        query = "select OPC_NAME from OPC_SERVER_NAME WHERE HOST_ID="+str(h_id)+";"
        cur.execute(query)
        result = cur.fetchall()
        for y in result:
            host[u][3].append(y[0])
        

    # FROM ITEM  



    database_name = document_database#"test_opc_pyro4_temp.db"
    con = lite.connect(database_name)
    cur = con.cursor()
    query = "select * from ITEM;"
    cur.execute(query)
    result = cur.fetchall()
    #print result

    pre_read = {}
    #pre_read [type_interface][server_aliase_name][opc_server_name]['ip'] = ''       String
    #pre_read [type_interface][server_aliase_name][opc_server_name]['port'] = xxxx   number
    #pre_read [type_interface][server_aliase_name][opc_server_name]['tag']  = []     tag
    pre_read['OPC']={}
    pre_read['Bacnet']={}
    pre_read['Modbus']={}
    pre_read['XML']={}
    
        
    print '*******************'
    for j in result:
            tag=j[1]
            #print '---------------'
            #print tag
            
            find_interface = tag.split('.')
            if len(find_interface) >2: #confirm data lenght must grath than 2
                if find_interface[0].lower() == 'opc':
                    #print 'type interface is opc'
                    svr_alias_name = find_interface[1]
                    if not pre_read['OPC'].has_key(svr_alias_name):
                        pre_read['OPC'][svr_alias_name] = {}
                        pre_read['OPC'][svr_alias_name]['ip'] = host[svr_alias_name][1]
                        pre_read['OPC'][svr_alias_name]['port'] = host[svr_alias_name][2]
                        
                    
                    list_opc_in_host = host[svr_alias_name][3]
                    for y in list_opc_in_host:
                        if y in tag:
                            #print y
                            real_tag = tag.split(y+'.')
                            #print '\t\t---->',real_tag[1]
                            if not pre_read['OPC'][svr_alias_name].has_key(y):
                                pre_read['OPC'][svr_alias_name][y]={}
                                pre_read['OPC'][svr_alias_name][y]['tag']=[]
                                pre_read['OPC'][svr_alias_name][y]['tag'].append(real_tag[1])
                            else:
                                pre_read['OPC'][svr_alias_name][y]['tag'].append(real_tag[1])
                            
                    

    print '-------Display-------------------'
        
    for l in pre_read:
        if l == 'OPC':
            for t in pre_read[l]:
                print t, # show server alias name
                print pre_read[l][t]['ip'],
                print pre_read[l][t]['port']
                for y in pre_read[l][t]:
                    
                    if str(type(pre_read[l][t][y])) == '<type \'dict\'>':
                        print '    ',y
                        tag_list = pre_read[l][t][y]['tag']
                        for u in tag_list:
                            print '    \t\t\t\t\t     ---> ',u
    
    aliasName = 'PC23434'
    host = pre_read['OPC'][aliasName]['ip']
    port = pre_read['OPC'][aliasName]['port']
    opc_tag_value = {}
    #try:
    #while True:
    #option example : PC23434 test_opc_pyro4_temp.db localhost 7777 KEPware.KEPServerEx.V4 PC23434KEPware.KEPServerEx.V4.tag
    
    for t in pre_read['OPC'][aliasName]:
        if str(type(pre_read['OPC'][aliasName][t]))  == '<type \'dict\'>':
            if 'KEP' in t:
                tag_all = pre_read['OPC'][aliasName][t]['tag']
                tag_file = aliasName+t+'.tag'
                f = open(tag_file,'w')
                pickledList = pickle.dumps (tag_all)
                f.write(pickledList)
                f.close()
                cmd = ["start", "python","pyroweb_client.py",aliasName,document_database,host,str(port),t,tag_file] # t = opc server name
                theproc = subprocess.Popen(cmd,shell = True)
                theproc.communicate()
                time.sleep(5)
                #theproc = subprocess.Popen(["start", "python","db_update_value.py","Testfromsubprocess"],shell = True)
                #theproc.communicate()
                #pyroweb_client.opc_read(host,port,t,pre_read['OPC'][aliasName][t]['tag'],10,opc_tag_value)
    #except Exception,err:
        #print err
        
def test_db(database_name):
    #database_name = "test_opc_pyro4_temp.db"
    con = lite.connect(database_name)
    cur = con.cursor()
    cur.execute("CREATE TABLE ITEM(id INTEGER PRIMARY KEY,tag text,value text,time_stamp text,quality text,timeout int);")
    
    #result = cur.fetchall()
    con.close()
        

if __name__ == '__main__':
    
    #if len(sys.argv) > 1:
    file = "test_opc_pyro4.xgd"#sys.argv[1]
    database_name  = file.replace('.xgd','')+'_temp.db'
    print database_name
    get_data(database_name)
    

