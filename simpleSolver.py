import json
import pandas as pd
from liquidityProviders import cf
# Ouvrir le fichier json et charger son contenu dans une variable
with open('instance_request_count_999.json', 'r', encoding='utf-8') as f:
    auction = json.load(f)

trades = []
interactions = []
i = 0
for order in auction['orders']:
    j = 0
    best = 0
    for pool in auction['liquidity']:
        if (set(pool['tokens'].keys()) == set([order['sellToken'], order['buyToken']]) 
            and order['buyAmount']<pool['tokens'][order['buyToken']]['balance']
            and pool['kind'] == 'constantProduct'):

            if order['kind'] == 'sell':
                buyAmount = cf(int(pool['tokens'][order['sellToken']]['balance']), int(pool['tokens'][order['buyToken']]['balance']), float(pool['fee']), True)(int(order['sellAmount']))

                if buyAmount >= int(order['buyAmount']):
                    break
                if best == 0:
                    best = buyAmount
                if buyAmount > best:
                    best = buyAmount
                    trades.pop()
                    interactions.pop()

                trades.append({'kind':'fulfillment', 'order' : order['uid'], 'fee' : 0, 'executedAmount' : order['sellAmount']})
                interactions.append({
                    'kind':'liquidity', 
                    'pool' : pool['id'], 
                    'inputToken' : order['sellToken'], 
                    'outputToken' : order['buyToken'], 
                    'inputAmount' : order['sellAmount'], 
                    'outputAmount' : str(buyAmount),
                    'internalize' : False
                })
                j +=1

            if order['kind'] == 'buy':
                sellAmount = cf(int(pool['tokens'][order['sellToken']]['balance']), int(pool['tokens'][order['buyToken']]['balance']), float(pool['fee']), False)(int(order['buyAmount']))
                if sellAmount < int(order['sellAmount']):
                    break
                if best == 0:
                    best = sellAmount
                if sellAmount < best and best !=0:
                    best = sellAmount
                trades.pop()
                interactions.pop()

                trades.append({'kind':'fulfillment', 'order' : order['uid'], 'fee' : 0, 'executedAmount' : order['buyAmount']})
                interactions.append({
                    'kind':'liquidity', 
                    'pool' : pool['id'], 
                    'inputToken' : order['sellToken'], 
                    'outputToken' : order['buyToken'], 
                    'inputAmount' : str(sellAmount), 
                    'outputAmount' : order['buyAmount'],
                    'internalize' : False
                })
                j+=1
    

print(len(trades))
print(len(interactions))
print(len(auction['orders']))