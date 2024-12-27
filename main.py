import os
import requests
import smtplib
from dotenv import load_dotenv

load_dotenv('.env')

url = 'https://api.etherscan.io/v2/api'

# base mainnet chainid is 8453
# eth mainnet chainid is 1
# OP mainnet chainid is 10
# zksync mainnet chainid is 324

chains = ['1','8453','10','324']
addresses = os.getenv('addresses')
apikey = os.getenv('apikey')

text_body = []
for i in chains:
    for a in addresses:
        params = {
        'chainid' : f'{i}',
        'module' : 'account',
        'action' : 'balance',
        'address' : f'{a}',
        'tag' : 'latest',
        'apikey' : apikey
        }

        response = requests.get(url=url, params=params)
        ETHER = int(response.json()['result']) * 10**-18
        rounded = round(ETHER, 2)
        text = (f"The ETH Balance on chain {i} at address {a} is {rounded}.")
        text_body.append(text)

ETH = []
OP = []
BASE = []
ZKSYNC = []

ETH.append(text_body[0:11])

BASE.append(text_body[11:22])

OP.append(text_body[22:33])

ZKSYNC.append(text_body[33:len(text_body)])

with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(user=os.getenv('user'), password=os.getenv('password'))
    connection.sendmail(from_addr=os.getenv('user'), to_addrs=os.getenv('to_addrs'),
                        msg=f"Subject: Wallet Balances\n\nThe Balances in ETH MAINNET for the wallet addresses are as follows:\n\n {ETH} \n\nThe Balances in BASE MAINNET for the wallet addresses are as follows:\n\n {BASE} \n\nThe Balances in OP MAINNET for the wallet addresses are as follows:\n\n {OP} \n\nThe Balances in ZKSYNC MAINNET for the wallet addresses are as follows:\n\n {ZKSYNC}")
