
import requests
import json

INVESTED = 0000

def get_binance_price(token): 
    response = requests.get("https://api.binance.com/api/v3/ticker/price")
    for x in response.json(): 
        for k,v in x.items():
            if v == token: 
                return x['price']
    return False 

def get_pcswap_price(adress):
    response = requests.get("https://api.pancakeswap.info/api/tokens/" + adress)
    return response.json()['data']['price_BNB']

def calculate_pcswap_value(pancake_price, amount, bnb_price):
    return pancake_price * bnb_price_in_usd * amount

def calculate_binance_value(binance_price, amount):
    return binance_price * amount

f = open("holdings.txt", "r")
bnb_price_in_usd = float(get_binance_price('BNBUSDT'))
total = 0 
err = []

for x in f:
    if not x.startswith("#"):
        try: 
            if x.split(":")[1] == "PancakeSwap":

                price = calculate_pcswap_value(
                    float(get_pcswap_price((x.split(":")[2]))), 
                    float(x.split(":")[3].strip('\n')),
                    bnb_price_in_usd
                )
                total += price

                if price != 0.0:
                    print(x.split(":")[0] + ": " + str(price) + " USDT")
                else: err.append("No price information available for token: " + x.split(":")[0])

            elif x.split(":")[1] == "Binance": 
                price_in_usd = float(get_binance_price(x.split(":")[0]+"USDT"))
                if not price_in_usd:
                    err.append("No convertion to USDT for token: " + x.split(":")[0])
                else:
                    price = calculate_binance_value(
                        price_in_usd,
                        float(x.split(":")[2].strip('\n')),
                    )

                    total += price

                    if price != 0.0:
                        print(x.split(":")[0] + ": " + str(price) + " USDT")
                    else: 
                        err.append("No price information available for token: " + x.split(":")[0])
            else:
                err.append("Exchange not supported for token: " + x.split(":")[0])
        except Exception as e:
            print("The row was in the wrong format, follow the conventon in the readme and make sure that you don't keep empty rows in the file.")

print("\n")
for e in err: 
    print(e)
    answer = input("Input value manually or press 'n':")
    if answer == 'n': continue 
    else: total += float(answer)
        
print("\n*****************************\n")
print("Total USD: ", total)
print("TOTAL PROFIT: " + str(total - INVESTED) + " USD")
