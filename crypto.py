
import requests
import json
import colorama

colorama.init()

INVESTED = 0000

def get_binance_price(token): 
    response = requests.get("https://api.binance.com/api/v3/ticker/price")
    for x in response.json(): 
        for k,v in x.items():
            if v == token: 
                return x['price']
    return False 

bnb_price_in_usd = float(get_binance_price('BNBUSDT'))


def get_pcswap_price(adress, version, token):
    err = []
    resp = requests.get("https://api.pancakeswap.info/api/{}tokens/{}".format(('' if version != 'v2' else 'v2/'), adress))
    if resp.ok and '0' == resp.json()['data']['price']:
        status_ok = False
    else: status_ok = resp.ok
    if 'error' in resp.json():
        return err, False, False, False, False
    return err, status_ok, resp.json()['data']['price'], resp.json()['data']['price_BNB'], resp.json()['data']['symbol']

def calculate_value(price, amount):
    return price * amount

def color_percentage(percentage):
    if percentage > 0:
        return "\033[92m{}\033[0m".format(percentage)
    elif percentage == 0:
        return "\033[90m{}\033[0m".format("null")
    else: return "\033[91m{}\033[0m".format(percentage)

def create_pancakeswap_valuemap(f):
    err = []
    for x in f:
        if not x.startswith("#"):
            if x.split(":")[1] == "PancakeSwap":
                name = x.split(":")[0]
                v1 = {}
                v2 = {}
                value_map[name] = {}
                for version in ["v1", "v2"]:
                    err, status_ok, price_usd, price_bnb, symbol = get_pcswap_price(x.split(":")[2], version, name)

                    if status_ok:
                        amount = x.split(":")[3].strip('\n')
                        val_usd = calculate_value(
                            float(price_usd), 
                            float(amount)
                        )
                        val_bnb = calculate_value(
                            float(price_bnb), 
                            float(amount)
                        )
                        value_map[name][version] = {}
                        value_map[name][version]['usd'] = val_usd 
                        value_map[name][version]['bnb'] = val_bnb
                        try: 
                            value_map[name]['bnb_spent'] = float(x.split(":")[4])
                        except: pass
    return err, value_map

def pretty_print_pancake_table_and_get_total(value_map):
    total = 0
    failed = []
    for token, info in value_map.items():
        if not 'v1' in info and not 'v2' in info:
            value = input("No price information for {}, input version:value:currency (e.g v1:0.1:bnb or v2:24.6:usd) 'n':".format(token))
            if value != 'n':
                if value.split(':')[0] == 'v1':
                    info['v1'] = {}
                    if value.split(':')[2] == 'bnb':
                        info['v1']['bnb'] = float(value.split(':')[1])
                        info['v1']['usd'] = info['v1']['bnb'] * bnb_price_in_usd
                    elif value.split(':')[2] == 'usd':
                        info['v1']['usd'] = float(value.split(':')[1])
                        info['v1']['bnb'] = info['v1']['usd'] / bnb_price_in_usd
                elif value.split(':')[0] == 'v2':
                    info['v2'] = {}
                    if value.split(':')[2] == 'bnb':
                        info['v2']['bnb'] = float(value.split(':')[1])
                        info['v2']['usd'] = info['v2']['bnb'] * bnb_price_in_usd
                    elif value.split(':')[2] == 'usd':
                        info['v2']['usd'] = float(value.split(':')[1])
                        info['v2']['bnb'] = info['v2']['usd'] / bnb_price_in_usd

    print("\n+--------------------------------------------------------------------------+")
    print("| {:^72} |".format("pancakeSwap"))
    print("+--------------------------------------------------------------------------+")
    print("| {:<15} | {:<8} / {:>8} | {:<8} / {:>8} | {} |".format('NAME', 'V1 USD', 'BNB', "V2 USD", "BNB", "PERCENTAGE"))
    print("+--------------------------------------------------------------------------+")

    for token, info in value_map.items():
        percentage = 0
        # token exists both in v1 and v2
        if 'v1' in info and 'v2' in info:
            if info['v1']['usd'] > info['v2']['usd']:
                total += info['v1']['usd']
                if 'bnb_spent' in info:
                    bnb_diff = info['v1']['bnb'] - info['bnb_spent']
            else:
                total += info['v2']['usd']
                if 'bnb_spent' in info:
                    bnb_diff = info['v2']['bnb'] - info['bnb_spent']
            v1_usd = round(info['v1']['usd'], 2)
            v1_bnb = round(info['v1']['bnb'], 2)
            v2_usd = round(info['v2']['usd'], 2)
            v2_bnb = round(info['v2']['bnb'], 2)

        # token exists only in v1
        elif 'v1' in info:
            total += info['v1']['usd']
            if 'bnb_spent' in info:
                bnb_diff = info['v1']['bnb'] - info['bnb_spent']
            most_val = "\033[92m{}\033[0m".format('v1')
            v2_usd = "xx.xx"
            v2_bnb= "xx.xx"
            v1_usd = round(info['v1']['usd'], 2)
            v1_bnb = round(info['v1']['bnb'], 2)
        
        # token exists only in v2
        elif 'v2' in info:
            total += info['v2']['usd']
            if 'bnb_spent' in info:
                bnb_diff = info['v2']['bnb'] - info['bnb_spent']
            most_val = "\033[92m{}\033[0m".format('v2')
            v1_usd = "xx.xx"
            v1_bnb = "xx.xx"
            v2_usd = round(info['v2']['usd'], 2)
            v2_bnb = round(info['v2']['bnb'], 2)
        else:
            v1_usd = "xx.xx"
            v1_bnb = "xx.xx"
            v2_usd = "xx.xx"
            v2_bnb = "xx.xx"

        if 'bnb_spent' in info:
            percentage = round(((bnb_diff / info['bnb_spent']) * 100), 2)
        print(
            "| {:<15} | {:<8} / {:>8} | {:<8} / {:>8} | {:17} % |".format(
                token,
                v1_usd,
                v1_bnb,
                v2_usd,
                v2_bnb,
                color_percentage(percentage)
            )
        )
    print("+--------------------------------------------------------------------------+")
    return total

def create_binance_valuemap(f):
    total = 0
    binance = {}
    for x in f:
        if not x.startswith("#"):
            if x.split(":")[1] == "Binance": 
                price_in_usd = float(get_binance_price(x.split(":")[0]+"USDT"))
                if not price_in_usd:
                    err.append("No convertion to USDT for token: " + x.split(":")[0])
                else:
                    price_usd = calculate_value(
                        price_in_usd,
                        float(x.split(":")[2].strip('\n')),
                    )

                    total += price_usd

                    if price_usd != 0.0:
                        binance[x.split(":")[0]] = price_usd
                    else: 
                        err.append("No price information available for token: " + x.split(":")[0])
    return total, binance, err

def pretty_print_binance_table(value_map):
    print("| {:<18} | {:<18} |".format("NAME", "VALUE"))
    print("+-----------------------------------------+")
    for token, price in value_map.items():
        print("| {:<18} | {:<18} |".format(token, price))
    print("+-----------------------------------------+")


f = open("holdings.txt", "r")
bnb_price_in_usd = float(get_binance_price('BNBUSDT'))
total = 0 
err = []
binance = {}

value_map = {}
try:
    err, value_map = create_pancakeswap_valuemap(f)
except Exception as e:
    print(e)

total_pcsw = pretty_print_pancake_table_and_get_total(value_map)
print("Total value: {}\n".format(total_pcsw))

print("\n+-----------------------------------------+")
print("| {:^39} |".format("Binance"))
print("+-----------------------------------------+")

f = open("holdings.txt", "r")
total_binance, binance, err = create_binance_valuemap(f)

pretty_print_binance_table(binance)
print("Total value: {}\n".format(total_binance))

print("Overall total: {}".format(total_binance + total_pcsw))
print("Profit / loss: {}".format(total_binance + total_pcsw - INVESTED))
