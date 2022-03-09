import requests
from config import *

def sendSaleWebhook(name_tag,img,val,symbol, os_url,from_acnt,to_acnt):
    url = webhook_url_for_sales
    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data = {
        
    }
    custom = name_tag+ " was purchased for " + val + " " + symbol
    from_name =from_acnt
    to_name =to_acnt
    from_url='https://opensea.io/'
    to_url='https://opensea.io/'
    try:
        from_url = from_url + from_name
        to_url = to_url + to_name
    except:
        print("Error in parsing buyer and seller name")
    from_field = {
        "name" : "From",
        "value": f"[{from_name}]({from_url})",
        "inline":True 
    }
    to_field = {
        "name" : "To",
        "value": f"[{to_name}]({to_url})",
        "inline":True 
    }
    
    data["embeds"] = [
        {
            #"description" : "text in embed",
            "title" : custom,
            'color' : embed_color_in_decimal,
            "url" : os_url,
            "image": {
            "url": img
            },
            'fields' : [
                from_field,
                to_field
            ]
        }
    ]
    
    #data['embeds']['fields'].append(from_field)
    #data['embeds']['fields'].append(to_field)
    result = requests.post(url, json= data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))


def sendListWebhook(name_tag,img,val,symbol, os_url):
    url = webhook_url_for_lists # paste your webhook url here
    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data = {}
    custom = name_tag+ " was enlisted for " + str(val) + " " + symbol
    data["embeds"] = [
        {
            #"description" : "text in embed",
            "title" : custom,
            'color' : embed_color_in_decimal,
            "url" : os_url,
            "image": {
            "url": img
            }
        }
    ]
    #data['embeds']['fields'].append(from_field)
    #data['embeds']['fields'].append(to_field)
    result = requests.post(url, json= data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully For List Bot, code {}.".format(result.status_code))

def sendOfferListWebhook(name_tag,img,val,symbol, os_url):
    url = webhook_url_for_offer_lists # paste your webhook url here
    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data = {}
    custom = name_tag+ " was offered for " + str(val) + " " + symbol
    data["embeds"] = [
        {
            #"description" : "text in embed",
            "title" : custom,
            'color' : embed_color_in_decimal,
            "url" : os_url,
            "image": {
            "url": img
            }
        }
    ]
    #data['embeds']['fields'].append(from_field)
    #data['embeds']['fields'].append(to_field)
    result = requests.post(url, json= data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully For Offer List Bot, code {}.".format(result.status_code))





