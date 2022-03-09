import requests 
import json
import time


def get_last_sale(cName):
    url = "https://api.opensea.io/api/v1/assets"
    querystring = {"order_direction":"desc","offset":"0","limit":"1","collection":cName}
    response = requests.request("GET", url, params=querystring)
    cnt = 0
    while response.status_code != 200:
        response = requests.request("GET", url, params=querystring)
        cnt = cnt + 1
        if cnt > 5:
            break
        time.sleep(0.3)

    jsonObject = json.loads(response.text)
    return jsonObject

def get_address(cName):
    last_item = get_last_sale(cName)
    address, token = parse_address_token(last_item)
    return address

def parse_address_token(objct):
    token = objct['assets'][0]['token_id']
    address = objct['assets'][0]['asset_contract']['address']
    return address,token

def get_asset(address, token):
    url = f"https://api.opensea.io/api/v1/asset/{address}/{token}/"
    response = requests.request("GET", url)
    cnt = 0
    while response.status_code !=200:
        response = requests.request("GET", url)
        time.sleep(0.3)
        cnt = cnt + 1
        if cnt > 5:
            break

    jsonObject = json.loads(response.text)
    return jsonObject
def get_floor_from_asset(objct):
    floor_price= objct['collection']['stats']['floor_price']
    return floor_price

def get_floor(cName):
    last_sale = get_last_sale(cName)
    address,token = parse_address_token(last_sale)
    asset = get_asset(address,token)
    floor = get_floor_from_asset(asset)
    return floor

def get_tratis_from_asset(objct):
    return objct['traits']

def get_counts(cName, token):
    last_sale = get_last_sale(cName)
    address,_token = parse_address_token(last_sale)
    asset = get_asset(address , token)
    return asset['collection']['stats']['count']


def get_traits(cName , token):
    last_sale = get_last_sale(cName)
    address,_token = parse_address_token(last_sale)
    asset = get_asset(address , token)
    traits = get_tratis_from_asset(asset)
    #print(traits)
    return traits
def get_image(cName,token):
    last_sale = get_last_sale(cName)
    address,_token = parse_address_token(last_sale)
    asset = get_asset(address , token)
    img = asset["image_url"]
    if img is None: 
        img = asset['asset_contract']['image_url']
    return img

def get_event(address, token):
    

    url = "https://api.opensea.io/api/v1/events"

    querystring = {"asset_contract_address":address,"token_id":token,"event_type":"transfer","only_opensea":"false","offset":"0","limit":"3"}

    headers = {"Accept": "application/json",
    "X-API-KEY": "b451777778cf4289b8a32474898a854d"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    cnt = 0
    while response.status_code != 200:
        time.sleep(1)
        response = requests.request("GET", url, params=querystring)
        cnt = cnt + 1
        if cnt > 5:
            break

    jsonObject = json.loads(response.text)
    
    return jsonObject

def get_from(objct):
    seller = objct['asset_events'][0]
    return seller['from_account']
def get_to(objct):
    buyer = objct['asset_events'][0]
    return buyer['to_account']

def get_stats(cName):
    last_sale = get_last_sale(cName)
    address,token = parse_address_token(last_sale)
    asset = get_asset(address,token)
    return asset['collection']['stats']







#Sale bot ----------------

def get_events_for_sale_bot(name):
    
    url = "https://api.opensea.io/api/v1/events"

    querystring = {"collection_slug":'acutecat',"event_type":"successful","only_opensea":"false","offset":"0","limit":"20"}

    headers = {"Accept": "application/json",
    "X-API-KEY": "b451777778cf4289b8a32474898a854d"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    cnt = 0
    while response.status_code != 200:
        time.sleep(1)
        response = requests.request("GET", url, headers=headers, params=querystring)
        cnt = cnt + 1
        if cnt > 5:
            break
    
    objct = json.loads(response.text)
    return objct

def get_events_from_name(cName):

    items = get_events_for_sale_bot(cName)
    return items['asset_events']


def get_infos(objct):
    id = objct['asset']['id']
    token = objct['asset']['token_id']
    name = objct['asset']['name']
    img = objct['asset']['image_url']
    os_link = objct['asset']['permalink']
    sym = objct["payment_token"]["symbol"]
    price = objct['total_price']
    date = objct['created_date']
    id = str(id) + date
    seller_name = 'None'
    try:
        seller_name =  objct['seller']['user']['username']
        if seller_name is None:
            raise Exception()
    except:
        try:
            seller_name =  objct['seller']['address']
            if seller_name is None:
                raise Exception()
        except:
            seller_name = 'None'
    
    buyer_name = 'None'
    try:
        buyer_name = objct['transaction']["from_account"]["user"]["username"]
        if buyer_name is None:
            raise Exception()
    except:
        try:
            buyer_name = objct['transaction']["from_account"]['address']
            if buyer_name is None:
                raise Exception()
        except:
            buyer_name = 'None'
    
    return id,token,name,img,os_link,sym,price,seller_name,buyer_name

########

#list bot

def get_events(cName):
    
   

    url = "https://api.opensea.io/api/v1/events"

    querystring = {"collection_slug":'acutecat',"event_type":"created","only_opensea":"false","offset":"0","limit":"20"}

    headers = {"Accept": "application/json",
    "X-API-KEY": "b451777778cf4289b8a32474898a854d"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    while response.status_code!=200:
        response = requests.request("GET", url, params=querystring)
        time.sleep(1)
    jsonObject = json.loads(response.text)
    return jsonObject

def parse_events(objct):
    assets = []
    for asset in objct['asset_events']:
        try :
            #print(*asset , sep='\n')
            #print(*asset['payment_token'],sep='\n')
            #print(asset['asset']['token_id'],asset['starting_price'],sep=' ')
            symbol = asset['payment_token']['symbol']
            token_id = asset['asset']['name']
            price = asset['starting_price']
            id = asset['asset']['id']
            img = asset['asset']['image_url']
            date = asset['created_date']
            os_url = asset['asset']['permalink']
            id = str(id) + date
            #print(symbol , token_id , price , id ,img , date)
            assets.append(tuple((id,token_id,price,symbol,img,os_url)))
        except:
            print("error in parsing one event")
    return assets

#print(parse_events(get_events('dogs-unchained')))

#offer_list bot

def get_offer_events(cName):
    
   

    url = "https://api.opensea.io/api/v1/events"

    querystring = {"collection_slug":cName,"event_type":"offer_entered","only_opensea":"false","offset":"0","limit":"20"}

    headers = {"Accept": "application/json",
    "X-API-KEY": "b451777778cf4289b8a32474898a854d"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    while response.status_code!=200:
        response = requests.request("GET", url, params=querystring)
        time.sleep(1)
    jsonObject = json.loads(response.text)
    return jsonObject

def parse_offer_events(objct):
    assets = []
    for asset in objct['asset_events']:
        try :
            #print(*asset , sep='\n')
            #print(*asset['payment_token'],sep='\n')
            #print(asset['asset']['token_id'],asset['starting_price'],sep=' ')
            symbol = asset['payment_token']['symbol']
            token_id = asset['asset']['name']
            price = asset['bid_amount']
            id = asset['asset']['id']
            img = asset['asset']['image_url']
            date = asset['created_date']
            os_url = asset['asset']['permalink']
            id = str(id) + date
            #print(symbol , token_id , price , id ,img , date)
            assets.append(tuple((id,token_id,price,symbol,img,os_url)))
        except:
            print("error in parsing one event")
    return assets





#a,t = parse_address_token(get_last_sale('lazy-lions'))
#print(a,t)
#print(get_floor_from_asset(get_asset(a,t)))
#print(*get_traits('skulliesgmi',33),sep='\n')
#print(get_floor('acutecat'))