import time

import ccxt
from configparser import ConfigParser

#从配置文件中读取私人api
cp = ConfigParser()
cp.read('user.conf')
section = cp.sections()[0]
apiKey = cp.get(section, "apiKey")
secret = cp.get(section, "secret")

#初始化交易所
binance_exchange = ccxt.binance({
    'apiKey': apiKey,
    'secret': secret,
    'timeout': 15000,
    'enableRateLimit': True
})

#定义下单参数
take_symbol = 'ETH/USDT'
take_type = 'limit'
take_side = 'buy'
take_amount = 0.005
take_price = 3000 # 实盘要用最新价格

#查询余额
# print(binance_exchange.fetch_balance()['free']['USDT'])

#单个网格交易
#下一个订单
#监控订单状态
#如果买单成交，则下一个卖单
#如果卖单成交，则下一个买单

#下单
take_order = binance_exchange.create_order(take_symbol,take_type,take_side,take_amount,take_price)

# 获取订单id
take_order_id = take_order['id']
print(take_order_id)

# 获取线上订单side
take_order_side = take_order['side']
print(take_order_side)

# 获取线上订单 price
take_order_price = take_order['price']

while 1:

    # 获取ETH最新价格
    ETH_last = binance_exchange.fetch_ticker(take_symbol)['last']

    # 查询订单状态
    order_status = binance_exchange.fetch_order_status(take_order_id, take_symbol)
    print(order_status) #open

    # 如果 买单 成交
    if order_status == 'closed' and take_order_side == 'buy':
        # 设置一个卖单
        sell_side = 'sell'
        sell_price = take_order_price + 1000
        take_sell_order = binance_exchange.create_order(take_symbol,take_type,sell_side,take_amount,sell_price)
        take_order_id = take_sell_order['id']
        take_order_side = take_sell_order['side']
        time.sleep(1)
    #如果 卖单 成交
    elif order_status == 'closed' and take_order_side == 'sell':
        # 设置一个买单
        buy_side = 'buy'
        buy_price = ETH_last - 200
        take_buy_order = binance_exchange.create_order(take_symbol, take_type, buy_side, take_amount, buy_price)
        take_order_id = take_buy_order['id']
        take_order_side = take_buy_order['side']
        take_order_price = take_buy_order['price']
        time.sleep(1)
    else:
        print('fuck')
        time.sleep(1)