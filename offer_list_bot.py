from threading import Timer
import time
import requests
import json
from webhook import *
from osAPI import *
from config import *

enlisted_id = []
to_print = {}
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
    try:
        events = get_offer_events(collection_name)
        assets = parse_offer_events(events)
        new_ids = []
        for id,token_id,price,symbol,img,os_url in reversed(assets):
            try:
                if id in enlisted_id:
                    continue
                enlisted_id.append(id)
                new_ids.append(id)
                val = float(price)/ratio
                name = f'{nft_name} {token_id}'
                try:
                    sendOfferListWebhook(name , img , str(val) , symbol,os_url)
                    time.sleep(0.7)
                except:
                    print("Error in sending webhook")
            except:
                print("Error in parsing one event")
        print(new_ids)


    except:
        print("Error in fetching events")

def filler():
    global enlisted_id
    try:
        events = get_offer_events(collection_name)
        assets = parse_offer_events(events)
        for id,token_id,price,symbol,img,os_url in assets:
            enlisted_id.append(id)
        return enlisted_id
    except:
        print("Error in fetching events")
def begin_offer_lists():
    if fetch_previous is False:
        previous_ids = filler()
        print(previous_ids)
    myclass= perpetualTimer(100,func)
    myclass.start()
#begin_offer_lists()
