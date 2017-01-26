# -*- coding: utf-8 -*-
import requests
import time
import re
import pymysql

requests.packages.urllib3.disable_warnings() 
INTERVAL = 3 
ADMIN_ID = 55602609 
URL = 'https://api.telegram.org/bot'
TOKEN = '284154350:AAGJM-wWavP1CGTqJtqM1tOhPHUnuYkHyFg'
offset = 0 

   
def open_tt():
    db = pymysql.connect("localhost", "root", "Fhtyf1977", "taskme_v2.0", charset = 'utf8')
    cur = db.cursor()
    cur.execute("select * from msk_task_list where state='open'")
    all_open_tt = cur.fetchall()
    final = ''
    for i in range(len(all_open_tt)):
        final += str(all_open_tt[i][0])+". "+all_open_tt[i][2] + '\n'
    return ("Все ТТ, открытые на данный момент: "+'\n'+final)
    cur.close()
    db.close()
    
 
def avr_open_tt():
    db = pymysql.connect("localhost", "root", "Fhtyf1977", "taskme_v2.0", charset = 'utf8')
    cur = db.cursor()
    cur.execute("select * from msk_task_list where state='open' and type='tt'")
    all_open_tt = cur.fetchall()
    final = ''
    for i in range(len(all_open_tt)):
        final += str(all_open_tt[i][0])+". "+all_open_tt[i][2] + '\n'
    return ("АВР ТТ, открытые на данный момент: "+'\n'+final)
    cur.close()
    db.close()
    
def task_open_tt():
    db = pymysql.connect("localhost", "root", "Fhtyf1977", "taskme_v2.0", charset = 'utf8')
    cur = db.cursor()
    cur.execute("select * from msk_task_list where state='open' and type='task'")
    all_open_tt = cur.fetchall()
    final = ''
    for i in range(len(all_open_tt)):
        final += str(all_open_tt[i][0])+". "+all_open_tt[i][2] + '\n'
    return ("Задачи, открытые на данный момент: "+'\n'+final)
    cur.close()
    db.close()
 
def detail_open_tt(cmd):
    db = pymysql.connect("localhost", "root", "Fhtyf1977", "taskme_v2.0", charset = 'utf8')
    cur = db.cursor()
    cur.execute("select * from msk_task_list where state='open'")
    all_open_tt = cur.fetchall()
    num_tt = re.search('\d+', cmd)
    if num_tt:
        num_tt = '{:d}'.format(int(num_tt.group()))
        if num_tt in cmd:
            cur.execute("select * from msk_task_list where id='%s'" % num_tt)
            tt = cur.fetchall()
            if tt:
                target = tt[0][3]
                group = tt[0][6]
                return ("Detail info of TT# "+ str(num_tt)+": \n"+target+"\n\n"+"Ответственный регион: "+'\n'+group)
            else:
                return("TT is not found")
    else:
        return ("Wrong number of TT.")
    cur.close()
    db.close()
    
def extensive_tt(cmd):
    db = pymysql.connect("localhost", "root", "Fhtyf1977", "taskme_v2.0", charset = 'utf8')
    cur = db.cursor()
    cur.execute("select * from msk_task_list where state='open'")
    all_open_tt = cur.fetchall()
    num_tt = re.search('\d+', cmd)
    if not num_tt:
        return ("Wrong number of TT.")
    else:
        num_tt = '{:d}'.format(int(num_tt.group()))
        if num_tt in cmd:
            cur.execute("select * from msk_task_comments where task_id='%s'" % num_tt)
            tt = cur.fetchall()
            if tt:
                final = ''
                for i in range(len(tt)):
                    cur.execute("select * from msk_users where login='%s'" % tt[i][3])
                    user = cur.fetchall()
                    date_tt = tt[i][4].ctime()
                    final += "================================================"+"\n"+date_tt+"  "+"### "+user[0][5]+" "+user[0][6]+" ###"+"  Comment№ "+str(tt[i][6])+"\n\n"+tt[i][2].replace('-&amp;gt;', '->') + '\n\n'
                return("Detail comments of TT# "+str(tt[0][1])+": "+'\n'+final)
            else:
                return("TT is not found or comments is empty")
    cur.close()
    db.close()
        
            

            
            
def check_updates():
    
    global offset
    data = {'offset': offset + 1, 'limit': 5, 'timeout': 0} #
    
    try:
        request = requests.post(URL + TOKEN + '/getUpdates', data=data) 
		
    except:
        log_event('Error getting updates') 
        return False 

    if not request.status_code == 200: return False 
    if not request.json()['ok']: return False 
    for update in request.json()['result']:
        offset = update['update_id'] 

        
        if not 'message' in update or not 'text' in update['message']:
            log_event('Unknown update: %s' % update) 
            continue 
        from_id = update['message']['chat']['id']
        bot_id = update['message']['from']['id']
        name = update['message']['from']
        read_file = open('/home/stas/zenoss_bot_users', 'r')
        zabbix_users = read_file.readlines()
        read_file.close()
        
        matching_prev = [s for s in zabbix_users if str(from_id) == s.replace('\n', '')]
        #arr_prev = re.search(str(bot_id), str(matching_prev))
        if matching_prev == []:
                send_text(bot_id, "You're not autorized to use me!")
                log_event('Unautorized: %s' % update)
                continue
        if from_id != "":
         message = update['message']['text'] 
         parameters = (offset, name, from_id, message)
         log_event('Message (id%s) from %s (id%s): "%s"' % parameters) 

       
         run_command(*parameters)


         
def run_command(offset, name, from_id, cmd):

    if cmd == '/status':  
        send_text(from_id, open_tt())
    elif "/detail" in cmd:
        send_text(from_id, detail_open_tt(cmd))
    elif "/comments" in cmd:
        send_text(from_id,extensive_tt(cmd))
    elif cmd == "/avr_status":
        send_text(from_id, avr_open_tt())
    elif cmd == "/task_status":
        send_text(from_id, task_open_tt())
    else:
        send_text(from_id, 'Wrong command.')
    

def log_event(text):
    with open('/home/stas/inventory_bot.log', 'a') as f:
    
        event = '%s >> %s' % (time.ctime(), text)
        print (event, file=f)

def send_text(chat_id, text):
    
    log_event('Sending to %s: %s' % (chat_id, text)) 
    data = {'chat_id': chat_id, 'text': text} 
    request = requests.get(URL + TOKEN + '/sendMessage', data=data) 
	
    if not request.status_code == 200: 
        return False 
    return request.json()['ok'] 


if __name__ == "__main__":
    while True:
        try:
            check_updates()
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            print ('Прервано пользователем..')
            break
	    

