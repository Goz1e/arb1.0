import os
try:
    from .func import *
except ImportError:
    print('import error caught')
    from func import *
import time

url = "https://data.binance.com/api/v3/ticker/price"
price_url = "https://data.binance.com/api/v3/ticker/bookTicker"


# get tickers from binance API and save locally
def step_0():
    tickers = get_tickers(url)
    tickers_list = get_coin_list(tickers)
    structured_pairs = structured_triangular_pairs(tickers_list[0:1500])
    with open('binance_tpairs_list.json','w') as fp:
        json.dump(structured_pairs,fp)
    # print('step 0 completed!')
    # print(len(structured_pairs))

# get current price data and calculate arbitrage
def step_1():
    arb_list = []
    saved_file = os.getcwd() + r'\binance\binance_tpairs_list.json'

    with open(saved_file) as json_file:
        structured_pairs  = json.load(json_file)
    prices_json = get_tickers(price_url)
    
    for t_pair in structured_pairs[0:]:   
        get_prices_for_tpair(t_pair, prices_json)
        surface_arb = cal_surface_rate(t_pair)
        if len(surface_arb)>1:
            real_rate_arb = get_dept_from_order_book(surface_arb)
            if len(real_rate_arb) >1:
                arb_list.append(real_rate_arb)
    if len(arb_list) < 1:
        return None
    # print(len(arb_list))
    return arb_list


# while True:
#     step_1()
#     time.sleep(1)
# step_0()
# step_1()
