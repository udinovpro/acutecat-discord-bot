

# Open-Sea Sales bot. 
# Version 3.0 
# jaian_as_zed



from threading import Timer
import time
import requests
import json
from webhook import *
from osAPI import *
from config import *


enlisted_id = []
to_print ={}

query_limit = '20'
ratio = 1000000000000000000 


fetch_previous = False

class perpetualTimer():
   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

def printer():
    print('ipsem lorem')

def func():
    global enlisted_id
    global to_print
    global ratio
    
    try:
        events = get_events_from_name(collection_name)
        for event in reversed(events):
            try:
                #print(block['last_sale']['transaction']['id'])
                id,token,name,img,os_link,sym,price,seller_name,buyer_name = get_infos(event)
                val = float(price)/ratio
                
                name = nft_name + " "+ name
                #print(val)
                #print(id,token,name,img,os_link,sym,price,seller_name,buyer_name,sep='\n')
                print("\n")
                if id in enlisted_id:
                    print(id)
                    continue
                else:
                    try:
                        to_print[id] = val
                        enlisted_id.append(id)
                        sendSaleWebhook(name, img , str(val),sym ,os_link,seller_name, buyer_name)
                        #sendTwitter(name, img, str(val),sym ,os_link,seller_name , buyer_name)
                        #print(id,val)
                        time.sleep(2.9)     
                    except:
                        print("Error in sending webhook")
            except:
                print("Error in a single event info extraction")
        print(to_print)
        to_print.clear()
    except:
        print("Error in getting events")


def filler():
    global enlisted_id
    try:
        events = get_events_from_name(collection_name)
        for event in events:
            try:
                id,token,name,img,os_link,sym,price,seller_name,buyer_name = get_infos(event)
                enlisted_id.append(id)
            except:
                print("Error in filler")
    except:
        print("Error in getting events")
    return enlisted_id

def begin_sales():
    if fetch_previous is False:
        previous_ids = filler()
        print(previous_ids)
    myclass= perpetualTimer(90,func)
    myclass.start()
#begin_sales()
