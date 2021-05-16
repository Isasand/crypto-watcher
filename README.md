This script checks the latest price for the tokens you hold in Binance or Pancakeswap and outputs a list of current values for each token / coin, a total value for all of them and a total profit / loss if you provide your initial investment value. 

**This is a work in progress.**

example run (where x is a calculated/ collected value): 
```bash
~/Desktop/crypto via 🐍 v3.7.3 on ☁️  eu-west-1 took 17s 
❯ python3 crypto.py

No price information for GOLDTK, input version:value:currency (e.g v1:0.1:bnb or v2:24.6:usd) 'n':v2:0.4:bnb

+--------------------------------------------------------------------------+
|                               pancakeSwap                                |
+--------------------------------------------------------------------------+
| NAME            | V1 USD   /      BNB | V2 USD   /      BNB | PERCENTAGE |
+--------------------------------------------------------------------------+
| GMR             | xx.xx    /    xx.xx | 80.82    /     0.14 | 40.87    % |
| Safeicarus      | 69.43    /     0.12 | xx.xx    /    xx.xx | 17.77    % |
| Diamond Token   | 85.08    /     0.14 | xx.xx    /    xx.xx | 44.63    % |
| GOLDTK          | xx.xx    /    xx.xx | 236.61   /      0.4 | null     % |
| NFTart          | 59.8     /      0.1 | 60.21    /      0.1 | 4.93     % |
| Safeboob        | 77.38    /     0.13 | xx.xx    /    xx.xx | 48.19    % |
| ChowChow        | 88.37    /     0.15 | xx.xx    /    xx.xx | 49.87    % |
| Pig             | 48.2     /     0.08 | 50.42    /     0.09 | -12.05   % |
+--------------------------------------------------------------------------+
Total value: xxx.xx

+-----------------------------------------+
|                 Binance                 |
+-----------------------------------------+
| NAME               | VALUE              |
+-----------------------------------------+
+-----------------------------------------+
Total value: 0

Overall total: xxx.xxx
Profit / loss: xxx.xx

```

# Prerequisites

- python3 : 
https://www.python.org/downloads/
- The python `requests` module (https://pypi.org/project/requests/).  
- The python `json` module (https://docs.python.org/3/library/json.html). 
- The python `colorama` module (https://pypi.org/project/colorama/)
Run the following commands in a terminal to install the modules. 
```
pip install requests
```` 
```
pip install json
```
```
pip install colorama
```

# How to use 
**IMPORTANT** : Only tokens from PancakeSwap and Binance are currently supported. 

1. Download the `crypto.py` file and put it in a folder on your computer. 

2. Open the file and replace `0000` value for the `INVESTED` variable to your invested amount. 

3. Create a text file in the same folder as the script called `holdings.txt`.

For each token you hold, create a row in the `holdings.txt` file. 

For a token you hold from binance, the row should follow this convention:   
`{name}:Binance:{amount-that-you-hold}:{bnb-you-spent}` where `bnb-you-spent` are optional and just a nice to have, not fully supported yet. 

Example row for a token you hold from binance:  
```
ETH:Binance:0.04179
```

For a token you hold from PancakeSwap, the row should follow this convention:
`{name}:PancakeSwap:{token-adress}:{amount-that-you-hold}`
Example row for a token you hold from PancakeSwap:  
```
BONFIRE:PancakeSwap:0x5e90253fbae4dab78aa351f4e6fed08a64ab5590:193904333.915533:0.2
```

Example of `holdings.txt` file: 

```
BNB:Binance:0.284112
GMR:PancakeSwap:0x0523215dcafbf4e4aa92117d13c6985a3bef27d7:228120850.69031771
ADA:PancakeSwap:0x3ee2200efb3400fabb9aacf31297cbdd1d435d47:94.870701:0.4
```

4. To run the script, open a terminal and run the following command in the same folder as the script:
```
python3 crypto.py
```

# Good to know
- Some tokens will not have price information available in the used APIs, then you will be prompted to input the value you hold manually or skip that token. You enter the value manually following this convention: {version}:{value}:{currency} where version can be one of `v1` and `v2` and currency can be one of `bnb` and `usd`.   
- You can comment out a row in your holders file if you trade a lot back and forth. Just comment out a row with `#` like this: 
```
#BNB:Binance:0.284112
```
and the script will skip that token. 

# TODO:
- I will add support for more exchanges going forward. 
- I will enable support to read the amount of a token you hold from your wallet since some tokens give reflections and grow due to tokenomics.
- I will create a virtual environment for this project so that you don't have to download every module for itself when using the script. 
