import os
try:
    from .workers import *
except ImportError:
    from workers import *

url = "https://api.poloniex.com/markets/ticker24h"

# creates structured triangular pairs list
def step_0():
    tickers=get_tickers(url)
    ticker_list = ticker_json_to_list(tickers)
    structured_pairs = structured_triangular_pairs(ticker_list[0:1500])
    with open('poloniex_tpair_list.json','w') as fp:
        json.dump(structured_pairs,fp)
    print('step 0 completed!')
    print(len(structured_pairs))

# adds latest price data to pairs dict in triangular pairs list
def step_1(structured_pairs):
    arb_list = []
    latest_prices=get_tickers(url)

    for t_pair in structured_pairs[0:]:
        get_prices(t_pair,latest_prices)
        surface_arb = cal_surface_rate(t_pair)
        if len(surface_arb)>2:
            real_rate_arb = get_dept_from_order_book(surface_arb)
            if len(real_rate_arb) >1:
                arb_list.append(real_rate_arb)
    if len(arb_list) < 1:
        return None
    print(len(arb_list))
    # return None
    return arb_list
            
