# -*- coding: utf-8 -*-
import requests
import time
import os
import re
import json
from requests import get
import pymysql
import math

requests.packages.urllib3.disable_warnings() 
INTERVAL = 3 
ADMIN_ID = 55602609 
URL = 'https://api.telegram.org/bot'
TOKEN = '151237123:AAHwAEN2T7NOJk0O8gRto8yK9wdWEa7ChKE'
offset = 0 
uptime_oid = ' 1.3.6.1.2.1.1.3.0'
temp_oid = ' iso.3.6.1.4.1.6527.3.1.2.2.1.8.1.18.1.134217729'
snmpw = 'snmpwalk -v 2c -c mpls_msk '

   
def get_url_api(graph_name):
    graph_url = zenoss_api + graph_name
    f = os.popen(graph_url)

def dead_hosts_api():
    final_list = []
    event_url = 'http://stas:9863d1c59@10.77.4.113:8080/zport/dmd/evconsole_router'
    data_api = {"action": "EventsRouter", "method": "query", "data": [{"limit": 200, "params": {"severity": [5], "eventGroup":"Ping", "DeviceClass": ['	/Network/Router/AGR', '/Network/Switch/CSA', '/Network/Router/BBR/', '/Network/Router/ASBR/'], "eventState": [0,1]}}], "tid": 1}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(event_url, data=json.dumps(data_api), headers=headers)
    res = r.json()
    if res['result']['events']:
        for i in range(len(res['result']['events'])):
            final_list.append(res['result']['events'][i]['device']['text'])
        return ('Devices are out of service: '+'\n'+str(final_list).replace(', ', '\n'))
    else:
       return "All devices is up"
       
def dead_ports_api():
    final_list = []
    event_url = 'http://stas:9863d1c59@10.77.4.113:8080/zport/dmd/evconsole_router'
    data_api = {"action": "EventsRouter", "method": "query", "data": [{"limit": 200, "params": {"severity": [5], "eventGroup":"trap", "DeviceClass": ["	/Network/Router/AGR", "/Network/Switch/CSA", "/Network/Router/BBR/", "/Network/Router/ASBR/"], "eventClass": ["/Net/Link"], "eventState": [0,1]}}], "tid": 1}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(event_url, data=json.dumps(data_api), headers=headers)
    res = r.json()
    if res['result']['events']:#res['result']['events'][0]['details']['deviceName'][0]
        for i in range(len(res['result']['events'])):
            final_list.append(res['result']['events'][i]['details']['deviceName'][0]+": "+res['result']['events'][i]['details']['ifDescr'][0].replace(', 10/100/Gig Ethernet SFP,', '').replace(', 10-Gig Ethernet,', ''))
        return ('Port are out of service: '+"\n"+str(final_list).replace(', ', "\n"))
    else:
       return "All devices is up"
       
def deadbs():
 agr_url = '\'http://stas:9863d1c59@10.77.4.113:8080/zport/dmd/Devices/Network/Router/AGR/devices/'
 csa_url = '\'http://stas:9863d1c59@10.77.4.113:8080/zport/dmd/Devices/Network/Switch/CSA/devices/'
 end_url = '/getRRDValue?dsname=bsCount_bsCount\''
 event_url = 'http://stas:9863d1c59@10.77.4.113:8080/zport/dmd/evconsole_router'
 data_api = {"action": "EventsRouter", "method": "query", "data": [{"limit": 200, "params": {"severity": [5], "eventGroup":"Ping", "DeviceClass": ['/Network/Router/AGR', '/Network/Switch/CSA', '/Network/Router/BBR/', '/Network/Router/ASBR/'], "eventState": [0,1]}}], "tid": 1}
 headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
 r = requests.post(event_url, data=json.dumps(data_api), headers=headers)
 res = r.json()
 csa_bs = 0
 agr_bs = 0
 bs_sum = 0
 result = 0 
 if res['result']['events']:
    for i in range(len(res['result']['events'])):
        if "CSA" in res['result']['events'][i]['device']['text']:
            bs = csa_url + res['result']['events'][i]['device']['text'] + end_url
            csa_curl = os.popen('curl '+bs)
            csa_bs = csa_curl.read()
            #csa_bs = float(csa_bs)
            if math.isnan(float(csa_bs)) == True:
                csa_bs = 0
            elif csa_bs != '':
                csa_bs = float(csa_bs)
            else:
                csa_bs = 0
        elif "AGR" in res['result']['events'][i]['device']['text']:
            bs = agr_url + res['result']['events'][i]['device']['text'] + end_url
            agr_curl = os.popen('curl '+bs)
            agr_bs = float(agr_curl.read())
        
        bs_sum = int(csa_bs + agr_bs)
        result += bs_sum
    return ("BS are out of service: "+ str(result))
 return "All BS is up"
 
 def find_element_in_list(element, list_element):
   matching = [s for s in list_element if element in s]
   bs_arr = re.findall(r'M\w\w\w\w\w\'|2-77-\w\w-\w\w\w\w\'|2-50-\w\w-\w\w\w\w', str(matching))
   bs_arr_1 = re.findall(r'M\w\w\w\w\w|2-77-\w\w-\w\w\w\w|2-50-\w\w-\w\w\w\w', str(bs_arr))
   bs_arr_final = re.sub(', ', '\n', str(bs_arr_1))
   return bs_arr_final
    
def bs_list():
    f = open('/home/stas/zenoss_all.txt', 'r')
    read_f = f.readlines()
    
    matching = [s for s in read_f if cmd in s]
    bs_arr = re.findall(r'M\w\w\w\w\w\W|2-77-\w\w-\w\w\w\w|2-50-\w\w-\w\w\w\w', str(matching))
    bs_arr_1 = re.findall(r'M\w\w\w\w\w|2-77-\w\w-\w\w\w\w|2-50-\w\w-\w\w\w\w', str(bs_arr))
    bs_arr_final = re.sub(', ', '\n', str(bs_arr_1))
    send_text(from_id, bs_arr_final)
    f.close()

def mbh_cdma(cmd):

  from xlrd import open_workbook, cellname
  wb = open_workbook(filename = '/home/stas/mbh_cdma.xlsx', encoding_override = "cp1251")   
  ws = wb.sheet_by_name('list')
  if cmd == '/cdma':
    return('Please, enter host name!')
  else:
    reg = re.findall(r'M\w00\w\w\w\w', cmd)
    if reg:
        num_position = reg[0].replace('MO00', 'MO').replace('MS00', 'MS')
        if num_position in str(ws.col(4)):
            for i in range(ws.nrows):
                if num_position in str(ws.row(i)):
                    cdma_station = str(ws.col(6)[i]).replace('text:', '')
                    return "CDMA Station: "+cdma_station
                    
                    
                
        else:
             return('Node not found')
    else:
        return('Unknown Node')    

def bs_rrl(cmd):

  from xlrd import open_workbook, cellname
  wb = open_workbook(filename = '/home/stas/rrl_bs.xlsx', encoding_override = "cp1251")   
  ws = wb.sheet_by_name('rrl_bs')
  if cmd == '/rrl':
    return('Please, enter BS name!')
  else:
    reg = re.findall(r'M\w\w\w\w\w$', cmd)
    if reg:
        if str(reg[0]) in str(ws.col(0)):
            for i in range(ws.nrows):
                if reg[0] in str(ws.row(i)):
                    find_rrl = re.findall(r'M\w\w\w\w\w', str(ws.row(i)))
                    if find_rrl[1::]:
                        return('BS '+str(reg[0])+': '+'\n'+str(find_rrl[1::]).replace(', ', '\n'))
                    else:
                        return('Empty RRL Path')
                    
                
        else:
             return('BS not found')
    else:
        return('Unknown BS')

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
            if not 'edited_message' in update or not 'text' in update['edited_message']:
                log_event('Unknown update: %s' % update) 
                continue 
        if 'message' in update:
            from_id = update['message']['chat']['id']
            bot_id = update['message']['from']['id']
            name = update['message']['from']
            
            read_file = open('/home/stas/zenoss_bot_users', 'r')
            zabbix_users = read_file.readlines()
            read_file.close()
            
            matching_prev = [s for s in zabbix_users if str(from_id) == s.replace('\n', '')]
        
            if matching_prev == []:
                send_text(bot_id, "You're not autorized to use me!")
                log_event('Unautorized: %s' % update)
                continue
                
            if from_id != "":
                message = update['message']['text'] 
                parameters = (offset, name, from_id, message)
                log_event('Message (id%s) from %s (id%s): "%s"' % parameters) 
                run_command(*parameters)
        elif 'edited_message' in update:
            from_id_edit_mess = update['edited_message']['from']['id']
            bot_id_edit_mess = update['edited_message']['from']['id']
            name_edit_mess = update['edited_message']['from']
            
            read_file = open('/home/stas/zenoss_bot_users', 'r')
            zabbix_users = read_file.readlines()
            read_file.close()

            matching_prev = [s for s in zabbix_users if str(from_id_edit_mess) == s.replace('\n', '')]
        
            if matching_prev == []:
                send_text(bot_id_edit_mess, "You're not autorized to use me!")
                log_event('Unautorized: %s' % update)
                continue
            if from_id_edit_mess != '':
                message = update['edited_message']['text'] 
                parameters = (offset, name_edit_mess, from_id_edit_mess, message)
                log_event('Message (id%s) from %s (id%s): "%s"' % parameters) 
                run_command_edit(*parameters)
        
     

days = '\d{1,3}\sdays\.\s\d\d:\d\d:\d\d'
hours = '\d\d:\d\d:\d\d'
         
def run_command(offset, name, from_id, cmd):
    db = pymysql.connect("localhost", "root", "Fhtyf1977", "zenoss")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM zenoss")
    res_sql = cursor.fetchall()

    if cmd == '/status':  
        send_text(from_id, dead_hosts_api())
    elif cmd == '/port':
        send_text(from_id, dead_ports_api())
    elif '/uptime' in cmd:
      bs_arr = re.findall('M\w00\w\w\w\w-\w\w\w0\w', str(cmd).upper())
      if bs_arr:
        node_find = [i[1] for i in res_sql if bs_arr[0] in i[1]]
        if node_find:
            uptime_snmp = snmpw+bs_arr[0]+uptime_oid
            up_snmpwalk = os.popen(uptime_snmp)
            current_uptime_pre = up_snmpwalk.read()
            if current_uptime_pre:
                current_uptime = re.findall(r'\d{1,3}\sdays,\s\d{1,2}:\d{1,2}:\d{1,2}|\d{1,2}:\d{1,2}:\d{1,2}|\d{1,2}:\d{1,2}', str(current_uptime_pre))
                send_text(from_id, 'Uptime for '+bs_arr[0]+': '+str(current_uptime[0]))
            else:
                send_text(from_id, 'No Response from '+bs_arr[0])
        else:
            send_text(from_id, 'Unknown device')
      else:
            send_text(from_id, 'Please, enter the device\'s name')
    elif '/temp' in cmd:
      bs_arr = re.findall('M\w00\w\w\w\w-\w\w\w0\w', str(cmd).upper())
      if bs_arr:
        node_find = [i[1] for i in res_sql if bs_arr[0] in i[1]]
        
        if node_find:
            temp_snmp = snmpw+bs_arr[0]+temp_oid
            up_snmpwalk = os.popen(temp_snmp)
            current_uptime_pre = up_snmpwalk.read()
            if current_uptime_pre:
                current_uptime = re.findall(r'\s[\d]+', str(current_uptime_pre))
                send_text(from_id, 'Temperature on '+bs_arr[0]+'is:'+str(current_uptime[0]))
            else:
                send_text(from_id, 'No Response from '+bs_arr[0])
        else:
            send_text(from_id, 'Unknown device')
      else:
            send_text(from_id, 'Please, enter the device\'s name')
    elif '/cdma' in cmd:
        send_text(from_id, mbh_cdma(str(cmd).upper()))
    elif '/rrl' in cmd:
        send_text(from_id, bs_rrl(str(cmd).upper()))
    elif any([i[2] for i in res_sql if str(cmd).upper() in i[2].split(', ')]):
        #find in cmd BS name
        bs_find = [i[1] for i in res_sql if str(cmd).upper() in i[2]]
        send_text(from_id, bs_find[0])
                    
                    
    elif any([i[1] for i in res_sql if str(cmd).upper() == i[1]]):
         #find in cmd Node name
         node_find = [i[1] for i in res_sql if str(cmd).upper() in i[1]]
         all_bs_on_node = [i[2] for i in res_sql if str(cmd).upper() in i[1]]
         if all_bs_on_node == ['']:
            all_bs_on_node = "0 BS on this node"
            send_text(from_id, all_bs_on_node)
         else:
            all_bs_on_node = str(len(all_bs_on_node[0].split(', ')))+" BS on this node: "+"\n"+str(all_bs_on_node).replace(', ', '\n')
            send_text(from_id, all_bs_on_node)

    elif 'MS' in str(cmd).upper():
            send_text(from_id, 'Unknown BS or device')
    elif 'MO' in str(cmd).upper():
            send_text(from_id, 'Unknown BS or device')
    elif cmd == '/bs_sum': 
        send_text(from_id, deadbs()) 
    
    else:
        send_text(from_id, 'Please do not write in this chat. This chat is only for notification. To communicate with colleagues use personal chat, PLEASE.')
    
    
def run_command_edit(offset, name_edit_mess, from_id_edit_mess, cmd):
    db = pymysql.connect("localhost", "root", "Fhtyf1977", "zenoss")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM zenoss")
    res_sql = cursor.fetchall()

    if cmd == '/status':  
        send_text(from_id_edit_mess, dead_hosts_api())
    elif cmd == '/port':
        send_text(from_id_edit_mess, dead_ports_api())
    elif '/uptime' in cmd:
      bs_arr = re.findall('M\w00\w\w\w\w-\w\w\w0\w', str(cmd).upper())
      if bs_arr:
        node_find = [i[1] for i in res_sql if bs_arr[0] in i[1]]
        if node_find:
            uptime_snmp = snmpw+bs_arr[0]+uptime_oid
            up_snmpwalk = os.popen(uptime_snmp)
            current_uptime_pre = up_snmpwalk.read()
            if current_uptime_pre:
                current_uptime = re.findall(r'\d{1,3}\sdays,\s\d{1,2}:\d{1,2}:\d{1,2}|\d{1,2}:\d{1,2}:\d{1,2}|\d{1,2}:\d{1,2}', str(current_uptime_pre))
                send_text(from_id_edit_mess, 'Uptime for '+bs_arr[0]+': '+str(current_uptime[0]))
            else:
                send_text(from_id_edit_mess, 'No Response from '+bs_arr[0])
        else:
            send_text(from_id_edit_mess, 'Unknown device')
      else:
            send_text(from_id_edit_mess, 'Please, enter the device\'s name_edit_mess')
    elif '/temp' in cmd:
      bs_arr = re.findall('M\w00\w\w\w\w-\w\w\w0\w', str(cmd).upper())
      if bs_arr:
        node_find = [i[1] for i in res_sql if bs_arr[0] in i[1]]
        
        if node_find:
            temp_snmp = snmpw+bs_arr[0]+temp_oid
            up_snmpwalk = os.popen(temp_snmp)
            current_uptime_pre = up_snmpwalk.read()
            if current_uptime_pre:
                current_uptime = re.findall(r'\s[\d]+', str(current_uptime_pre))
                send_text(from_id_edit_mess, 'Temperature on '+bs_arr[0]+'is:'+str(current_uptime[0]))
            else:
                send_text(from_id_edit_mess, 'No Response from '+bs_arr[0])
        else:
            send_text(from_id_edit_mess, 'Unknown device')
      else:
            send_text(from_id_edit_mess, 'Please, enter the device\'s name_edit_mess')
    elif '/cdma' in cmd:
        send_text(from_id_edit_mess, mbh_cdma(str(cmd).upper()))
    elif '/rrl' in cmd:
        send_text(from_id_edit_mess, bs_rrl(str(cmd).upper()))
    elif any([i[2] for i in res_sql if str(cmd).upper() in i[2].split(', ')]):
        #find in cmd BS name_edit_mess
        bs_find = [i[1] for i in res_sql if str(cmd).upper() in i[2]]
        send_text(from_id_edit_mess, bs_find[0])
                    
                    
    elif any([i[1] for i in res_sql if str(cmd).upper() == i[1]]):
         #find in cmd Node name_edit_mess
         node_find = [i[1] for i in res_sql if str(cmd).upper() in i[1]]
         all_bs_on_node = [i[2] for i in res_sql if str(cmd).upper() in i[1]]
         if all_bs_on_node == ['']:
            all_bs_on_node = "0 BS on this node"
            send_text(from_id_edit_mess, all_bs_on_node)
         else:
            all_bs_on_node = str(len(all_bs_on_node[0].split(', ')))+" BS on this node: "+"\n"+str(all_bs_on_node).replace(', ', '\n')
            send_text(from_id_edit_mess, all_bs_on_node)

    elif 'MS' in str(cmd).upper():
            send_text(from_id_edit_mess, 'Unknown BS or device')
    elif 'MO' in str(cmd).upper():
            send_text(from_id_edit_mess, 'Unknown BS or device')
    elif cmd == '/bs_sum': 
        send_text(from_id_edit_mess, deadbs()) 
    
    else:
        send_text(from_id_edit_mess, 'Please do not write in this chat. This chat is only for notification. To communicate with colleagues use personal chat, PLEASE.')

def log_event(text):
    with open('/home/stas/zenoss.log', 'a') as f:
    
        event = '%s >> %s' % (time.ctime(), text)
        print (event, file=f)

def send_text(chat_id, text):
    
    log_event('Sending to %s: %s' % (chat_id, text)) 
    data = {'chat_id': chat_id, 'text': text} 
    request = requests.get(URL + TOKEN + '/sendMessage', data=data) 
	
    if not request.status_code == 200: 
        return False 
    return request.json()['ok'] 

    
    
def send_photo(chat_id, url, photo_id):
    data = {'chat_id': chat_id}
    photo_name = '%s.jpeg' % photo_id
    with open(photo_name, "wb") as file:
        response = get(url)
        file.write(response.content)
    log_event('Sending to %s: %s' % (chat_id, photo_id)) 
    files = {'photo': open(photo_name, "rb")} 
    request = requests.post(URL + TOKEN + '/sendPhoto', data=data, files=files) 
	
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