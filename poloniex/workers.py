import json, requests, time

"""takes api endpoint and returns tickers json from exchange"""
def get_tickers(url):
    return requests.get(url).json() 


"""takes tickers json array and converts it to list = ['ETH_USDT','BTC_USDT',...]"""
def ticker_json_to_list(ticker_json):
    return [pair['symbol'] for pair in ticker_json]


"""takes ticker_list and retunrs a list of dictionaries cointaining pairs and thier data """
def structured_triangular_pairs(coin_list):

    # Declare Variables
    triangular_pairs_list = []
    remove_duplicates_list = []
    pairs_list = coin_list[0:]

    # Get Pair A
    for pair_a in pairs_list:
        pair_a_split = pair_a.split("_")
        a_base = pair_a_split[0]
        a_quote = pair_a_split[1]

        # Assign A to a Box
        a_pair_box = [a_base, a_quote]

        # Get Pair B
        for pair_b in pairs_list:
            pair_b_split = pair_b.split("_")
            b_base = pair_b_split[0]
            b_quote = pair_b_split[1]

            # Check Pair B
            if pair_b != pair_a:
                if b_base in a_pair_box or b_quote in a_pair_box:

                    # Get Pair C
                    for pair_c in pairs_list:
                        pair_c_split = pair_c.split("_")
                        c_base = pair_c_split[0]
                        c_quote = pair_c_split[1]

                        # Count the number of matching C items
                        if pair_c != pair_a and pair_c != pair_b:
                            combine_all = [pair_a, pair_b, pair_c]
                            pair_box = [a_base, a_quote, b_base, b_quote, c_base, c_quote]

                            counts_c_base = 0
                            for i in pair_box:
                                if i == c_base:
                                    counts_c_base += 1

                            counts_c_quote = 0
                            for i in pair_box:
                                if i == c_quote:
                                    counts_c_quote += 1

                            # Determining Triangular Match
                            if counts_c_base == 2 and counts_c_quote == 2 and c_base != c_quote:
                                combined = pair_a + "," + pair_b + "," + pair_c
                                unique_item = ''.join(sorted(combine_all))

                                if unique_item not in remove_duplicates_list:
                                    match_dict = {
                                        'pair_a' : {"symbol": pair_a,"base": a_base,"quote": a_quote,},
                                        'pair_b' : {"symbol": pair_b,"base": b_base,"quote": b_quote,},
                                        'pair_c' : {"symbol": pair_c,"base": c_base,"quote": c_quote,},
                                        'combined': combined,
                                    }
                                    triangular_pairs_list.append(match_dict)
                                    remove_duplicates_list.append(unique_item)
    return triangular_pairs_list


"""takes structured_triangular_pairs and live_tickers then adds latest price data to pair dictionaries"""
def get_prices(t_pair,latest_prices):
    
    pair_a = t_pair['pair_a']
    pair_b = t_pair['pair_b']
    pair_c = t_pair['pair_c']
    
    for item in latest_prices:
        if item['symbol'] == pair_a['symbol']:
            pair_a['ask'] = item['ask']   
            pair_a['bid'] = item['bid']   
            pair_a['base_amount'] = 1   
            pair_a['quote_amount'] = 1   
        
        if item['symbol'] == pair_b['symbol']:
            pair_b['ask'] = item['ask']   
            pair_b['bid'] = item['bid']   
            pair_b['base_amount'] = 1   
            pair_b['quote_amount'] = 1   
        
        if item['symbol'] == pair_c['symbol']:
            pair_c['ask'] = item['ask']   
            pair_c['bid'] = item['bid']   
            pair_c['base_amount'] = 1   
            pair_c['quote_amount'] = 1   


# <======convineince method for cal_surface_rate======>
def fetch_next_pair(tri_pair_list,current_pair_symbol,coin,direction):
    tri_pair_list = [i for i in tri_pair_list if not (i['symbol'] == current_pair_symbol)]    
    for pair in tri_pair_list:
        if str(coin) in  [str(pair['base']),str(pair['quote'])]:            
            return pair


"""teturns pair with swap information if positive surface rate is found"""
def cal_surface_rate(tri_pair):
    pair_a = tri_pair['pair_a']
    pair_b = tri_pair['pair_b']
    pair_c = tri_pair['pair_c']
    directions = ['foward','reverse']
    tri_pair_list = [pair_a,pair_b,pair_c]    
    
    for direction in directions:
        # this is TRADE 1
        pair_a_symbol = pair_a['symbol']
        pair_a_base = pair_a['base']
        pair_a_quote = pair_a['quote']
        pair_a_ask = pair_a['ask']
        pair_a_bid = pair_a['bid']
        pair_a_base_amount = pair_a['base_amount']
        pair_a_quote_amount = pair_a['quote_amount']

        if direction == 'foward': #Base to Quote swap
            t1_rate = 1/float(pair_a_ask)
            t1_direction = f'{pair_a_base} to {pair_a_quote}'
            swap1_direction = 'base_to_quote'
            coin = pair_a_quote  #parameter for returning next pair
            initial_amount = pair_a_base_amount
        else: #Quote to Base swap
            t1_rate = float(pair_a_bid)
            t1_direction = f'{pair_a_quote} to {pair_a_base}'
            swap1_direction = 'quote_to_base'
            coin = pair_a_base  #parameter for returning next pair
            initial_amount = pair_a_quote_amount
        t1_acquired_coin = initial_amount * t1_rate
        t1_msg = f'1: swap {t1_direction} at rate:{t1_rate} => {t1_acquired_coin}'
        # t1_msg = f'1: flow = {direction} | swap {t1_direction} at rate:{t1_rate} => {t1_acquired_coin}'
        
        next_pair = fetch_next_pair(tri_pair_list,pair_a['symbol'],coin,direction)
        next_pair_symbol = next_pair['symbol']
        next_pair_base = next_pair['base']
        next_pair_quote = next_pair['quote']
        next_pair_ask = next_pair['ask']
        next_pair_bid = next_pair['bid']
        if coin == next_pair_base: #foward swap (Base to Quote)
            t2_rate = 1/float(next_pair_ask)
            t2_direction = f'{next_pair_base} to {next_pair_quote}'
            swap2_direction = 'base_to_quote'
            t2_coin = next_pair_quote
        elif coin == next_pair_quote: #reverse swap (Quote to Base)
            t2_rate = float(next_pair_bid)
            t2_direction = f'{next_pair_quote} to {next_pair_base}'
            swap2_direction = 'quote_to_base'
            t2_coin = next_pair_base
        t2_acquired_coin = t1_acquired_coin * t2_rate
        t2_msg = f'2: swap {t2_direction} at rate:{t2_rate}  => {t2_acquired_coin}'

        last_pair = fetch_next_pair(tri_pair_list,next_pair['symbol'],t2_coin,direction)
        last_pair_symbol = last_pair['symbol']
        last_pair_base = last_pair['base']
        last_pair_quote = last_pair['quote']
        last_pair_ask = last_pair['ask']
        last_pair_bid = last_pair['bid']
        if t2_coin == last_pair_base: #foward swap (Base to Quote)
            t3_rate = 1/float(last_pair_ask) if float(last_pair_ask) != 0 else 0
            t3_direction = f'{last_pair_base} to {last_pair_quote}'
            swap3_direction = 'base_to_quote'
            t3_coin = last_pair_quote
        elif t2_coin == last_pair_quote: #reverse swap (Quote to Base)
            t3_rate = float(last_pair_bid)
            t3_coin = last_pair_base
            t3_direction = f'{last_pair_quote} to {last_pair_base}'
            swap3_direction = 'quote_to_base'
        t3_acquired_coin = t2_acquired_coin * t3_rate
        t3_msg = f'3: swap {t3_direction} at rate:{t3_rate}  => {t3_acquired_coin}'
        # t3_msg = f'3: direction = {direction} swap {t3_direction} at rate:{t3_rate} => {t3_acquired_coin}'
        
        profit = t3_acquired_coin - initial_amount
        percentage = (profit/initial_amount) * 100
    
        if profit > 0:
            # output result 
            surface_dict = {
                'swap_1': coin,
                'swap_2': t2_coin,
                'swap_3': t3_coin,
                'contract_1': pair_a_symbol,
                'contract_2': next_pair_symbol,
                'contract_3': last_pair_symbol,
                'direction_trade_1': swap1_direction,
                'direction_trade_2': swap2_direction,
                'direction_trade_3': swap3_direction,
                'starting_amount': initial_amount,
                'acquired_coin_t1': t1_acquired_coin,
                'acquired_coin_t2': t2_acquired_coin,
                'acquired_coin_t3': t3_acquired_coin,
                'swap_1_rate': t1_rate,
                'swap_2_rate': t2_rate,
                'swap_3_rate': t3_rate,
                'profit_loss': profit,
                'profit_loss_perc': percentage,
                'direction':direction,
                'trade_description_1': t1_msg,
                'trade_description_2': t2_msg,
                'trade_description_3': t3_msg,
            }
        
            return surface_dict
    return {}


# <======convineince method for get_depth_from_order_book======>
def reformated_orderbook(prices,c_direction):
    
    price_list_main = []
    asks = prices['asks']
    asks_paired = list(zip(asks[::2], asks[1::2]))
    bids = prices['bids']
    bids_paired = list(zip(bids[::2], bids[1::2]))
    if c_direction == 'base_to_quote':
        for p in asks_paired:
            ask_price = float(p[0])
            adj_price = 1/ask_price if ask_price != 0 else 0
            adj_quantity = float(p[1]) * ask_price
            price_list_main.append([adj_price,adj_quantity])
    
    if c_direction == 'quote_to_base':
        for p in bids_paired:
            bid_price = float(p[0])
            adj_price = bid_price if bid_price != 0 else 0
            adj_quantity = float(p[1])
            price_list_main.append([adj_price,adj_quantity])
    return price_list_main


# <======convineince method for get_depth_from_order_book======>
def calculate_acquired_coin(startin_amount,order_book):
    """
    CHALLENGES:
    full amount of capital can be eaten on the first level (level 0)
    some of the capital can be eaten-up by multiple levels
    some coins may not have enough luquidity
    """

    trading_balance = startin_amount
    quantity_bought = 0
    acquired_coin = 0
    counts = 0

    for level in order_book:
        level_price = level[0]
        level_available_quantity = level[1]

        # amount-in is <= first level total amount
        if trading_balance <= level_available_quantity:
            quantity_bought = trading_balance
            trading_balance = 0
            amount_bought = quantity_bought * level_price

        # amount-in is > given level total amount
        if trading_balance > level_available_quantity:
            quantity_bought = level_available_quantity
            trading_balance -= quantity_bought
            amount_bought = quantity_bought * level_price
        
        # Accumulate acquired coin
        acquired_coin += amount_bought
        
        if trading_balance == 0:
            return acquired_coin

        counts +=1
        if counts == len(order_book):
            return 0


"""Get Depth From Orderbook"""
def get_dept_from_order_book(surface_arb):
    
    # Extract initial variables
    swap_1 = surface_arb['swap_1']
    starting_amount = 100
    starting_amount_dict = {
        'USDT':100,
        'USDC':100,
        'BTC':0.05,
        'ETH':0.1
    }
    
    if swap_1 in starting_amount_dict:
        starting_amount = starting_amount_dict[swap_1]

    # define pairs
    contract_1 = surface_arb['contract_1']
    contract_2 = surface_arb['contract_2']
    contract_3 = surface_arb['contract_3']

    # define direction of trades
    contract_1_direction = surface_arb['direction_trade_1']
    contract_2_direction = surface_arb['direction_trade_2']
    contract_3_direction = surface_arb['direction_trade_3']
    contract_1_description = surface_arb['trade_description_1']
    contract_2_description = surface_arb['trade_description_2']
    contract_3_description = surface_arb['trade_description_3']
    

    # after getting the capital, we define the pairs(contracts) and thier directions
    # then trade it through the orderbook depth to see if there is truly an arbitrage opportunity
    # TODO: we need to understand how the depth trade really works.

    # get order book for first trade assessment
    url1 = f"https://api.poloniex.com/markets/{contract_1}/orderBook?limit=10"
    dept_1_prices  = get_tickers(url1)
    dept_1_reformatted_prices = reformated_orderbook(dept_1_prices,contract_1_direction)

    url2 = f"https://api.poloniex.com/markets/{contract_2}/orderBook?limit=20"
    dept_2_prices  = get_tickers(url2)
    dept_2_reformatted_prices = reformated_orderbook(dept_2_prices,contract_2_direction)

    url3 = f"https://api.poloniex.com/markets/{contract_3}/orderBook?limit=20"
    dept_3_prices  = get_tickers(url3)
    dept_3_reformatted_prices = reformated_orderbook(dept_3_prices,contract_3_direction)
    
    # get acquired coins
    acquired_coin_t1 = calculate_acquired_coin(starting_amount,dept_1_reformatted_prices)
    acquired_coin_t2 = calculate_acquired_coin(acquired_coin_t1,dept_2_reformatted_prices)
    acquired_coin_t3 = calculate_acquired_coin(acquired_coin_t2,dept_3_reformatted_prices)

    # Calculate Profit-Loss for Real Rate
    profit_loss = acquired_coin_t3 - starting_amount

    real_rate_perc = (profit_loss/starting_amount) * 100 if profit_loss != 0 else 0
    if real_rate_perc > 0:
        result =  {
            'starting_amount': starting_amount,
            'acquired_coin': acquired_coin_t3,
            'profit-loss': profit_loss,
            'real_rate_percent': real_rate_perc,
            'contract_1': contract_1,
            'contract_2': contract_2,
            'contract_3': contract_3,
            'contract_1_direction': contract_1_direction,
            'contract_2_direction': contract_2_direction,
            'contract_3_direction': contract_3_direction,
            'contract_1_description': contract_1_description,
            'contract_2_description': contract_2_description,
            'contract_3_description': contract_3_description,
        }
        return result
    else:
        return {}
