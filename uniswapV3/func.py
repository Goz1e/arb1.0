""""STRUCTURE TRADING TRI PAIRS"""
def structure_triangular_pairs(pairs_list):
    triangular_pairs_list = []
    remove_duplicates_list = []
    # pair_list = pairs[:limit]
    count = 0
    for pair_a in pairs_list:

        # Get first pair (A)
        a_base = pair_a["token0"]["symbol"]
        a_quote = pair_a["token1"]["symbol"]
        a_pair = a_base + "_" + a_quote
    
        # Put (A) into box for checking at (B)
        a_pair_box = [a_base, a_quote]

        # Get second pair (B)
        for pair_b in pairs_list:
            b_base = pair_b["token0"]["symbol"]
            b_quote = pair_b["token1"]["symbol"]
            b_pair = b_base + "_" + b_quote
    
            # Get third pair (C)
            if a_pair != b_pair:
                if b_base in a_pair_box or b_quote in a_pair_box:

                    # Get third pair (C)
                    for pair_c in pairs_list:
                        c_base = pair_c["token0"]["symbol"]
                        c_quote = pair_c["token1"]["symbol"]
                        c_pair = c_base + "_" + c_quote
    
                        # Count number of (C) items
                        if c_pair != a_pair and c_pair != b_pair:
                            combine_all = [a_pair, b_pair, c_pair]
                            pair_box = [a_base, a_quote, b_base, b_quote, c_base, c_quote]

                            counts_c_base = 0
                            for i in pair_box:
                                if i == c_base:
                                    counts_c_base += 1

                            counts_c_quote = 0
                            for i in pair_box:
                                if i == c_quote:
                                    counts_c_quote += 1

                            if counts_c_base == 2 and counts_c_quote == 2 and c_base != c_quote:
                                combined = a_pair + "," + b_pair + "," + c_pair
                                unique_string = ''.join(sorted(combined))

                                # Output pair
                                if unique_string not in remove_duplicates_list:
                                    pair_a['symbol'] = a_pair
                                    pair_b['symbol'] = b_pair
                                    pair_c['symbol'] = c_pair
                                    pair_c['base_amount'] = 1
                                    pair_c['base_amount'] = 1
                                    pair_c['base_amount'] = 1
                                    output_dict = {
                                        'pair_a' : pair_a,
                                        'pair_b' : pair_b,
                                        'pair_c' : pair_c,
                                        'combined': combined,
                                    }
                                    triangular_pairs_list.append(output_dict)
                                    remove_duplicates_list.append(unique_string)

    return triangular_pairs_list


def fetch_next_pair(tri_pair_list,current_symbol,swap2):
    tri_pair_list = [i for i in tri_pair_list if not (i['symbol'] == current_symbol)]    
    for pair in tri_pair_list:
            if swap2 in [pair['token0']['symbol'],pair['token1']['symbol']]:
                return pair


# calulating surface rate arbitrage
def calc_triangular_arb_surface_rate(tri_pair,min_rate):

    min_surface_rate = min_rate
    surface_dict = {}
    starting_amount = 1

    pair_a = tri_pair['pair_a']
    pair_b = tri_pair['pair_b']
    pair_c = tri_pair['pair_c']
    
    directions = ['forward','reverse']
    tri_pair_list = [pair_a,pair_b,pair_c]    
    
    for direction in directions:
        pair1 = pair_a
        pair1_token0price = float(pair1['token0Price'])
        pair1_token1price = float(pair1['token1Price'])
        pair1_base = pair1['token0']['symbol']
        pair1_quote = pair1['token1']['symbol']
        pair1_symbol = pair1['symbol']
        pool_contract_1 = pair1['id']

        if direction == 'forward': 
            swap1 = pair1_base    
            swap2 = pair1_quote
            t1_rate = pair1_token0price
            swap1_direction = "baseToQuote"
            loop_direction = direction
        else: #Quote to Base swap
            swap1 = pair1_quote    
            swap2 = pair1_base    
            t1_rate = pair1_token1price
            swap1_direction = "quoteToBase"
            loop_direction = direction
        t1_acquired_coin = starting_amount * t1_rate if t1_rate !=0 else 0 
        t1_msg = f'1: swap {swap1_direction} @ rate:{t1_rate} => {t1_acquired_coin}'
    
        pair2 = fetch_next_pair(tri_pair_list,pair1_symbol,swap2)
        # print(direction,pair1_symbol,pair2['symbol'])
    
        pair2_base = pair2['token0']['symbol']
        pair2_quote = pair2['token1']['symbol']
        pair2_token0Price = float(pair2['token0Price'])
        pair2_token1Price = float(pair2['token1Price'])
        pair2_symbol = pair2['symbol'] 
        pool_contract_2 = pair2['id']

        if swap2 == pair2_base: #foward swap (Base to Quote)
            t2_rate = pair2_token0Price if pair2_token0Price != 0 else 0
            swap2_direction = 'baseToQuote'
            swap3 = pair2_quote
        else: #reverse swap (Quote to Base)
            t2_rate = pair2_token1Price if pair2_token1Price != 0 else 0
            swap2_direction = 'quoteToBase'
            swap3 = pair2_base
        t2_acquired_coin = t1_acquired_coin * t2_rate
        t2_msg = f'2: swap {swap2_direction} @ rate:{t2_rate} => {t2_acquired_coin}'
        # print(t1_msg,t2_msg,'\n')
        
        pair3 = fetch_next_pair(tri_pair_list,pair2_symbol,swap3)
        # print(direction,pair1_symbol,pair3['symbol'])
    
        pair3_token0Price = float(pair3['token0Price'])
        pair3_token1Price = float(pair3['token1Price'])
        pair3_base = pair3['token0']['symbol']
        pair3_quote = pair3['token1']['symbol']
        pair3_symbol = pair3['symbol'] 
        pool_contract_3 = pair3['id']

        if swap3 == pair3_base: #foward swap (Base to Quote)
            t3_rate = pair3_token0Price if pair3_token0Price != 0 else 0
            swap3_direction = 'baseToQuote'
        else: #reverse swap (Quote to Base)
            t3_rate = pair3_token1Price if pair3_token1Price != 0 else 0
            swap3_direction = 'quoteToBase'
        t3_acquired_coin = t2_acquired_coin * t3_rate
        t3_msg = f'3: swap {swap3_direction} @ rate:{t3_rate} => {t3_acquired_coin}'
    
    
        
        profit = t3_acquired_coin - starting_amount
        percentage = (profit/starting_amount) * 100
        if percentage > min_rate and percentage < 20:
            # output result 
            surface_dict = {
                'swap_1': swap1,
                'swap_2': swap2,
                'swap_3': swap3,
                'contract_1': pair1_symbol,
                'contract_2': pair2_symbol,
                'contract_3': pair3_symbol,
                'direction_trade_1': swap1_direction,
                'direction_trade_2': swap2_direction,
                'direction_trade_3': swap3_direction,
                'starting_amount': starting_amount,
                'acquired_coin_t1': t1_acquired_coin,
                'acquired_coin_t2': t2_acquired_coin,
                'acquired_coin_t3': t3_acquired_coin,
                'swap_1_rate': t1_rate,
                'swap_2_rate': t2_rate,
                'swap_3_rate': t3_rate,
                'profit_loss': profit,
                'profit_loss_perc': percentage,
                'real_rate_percent': percentage,
                'direction':direction,
                'contract_1_description': t1_msg,
                'contract_2_description': t2_msg,
                'contract_3_description': t3_msg,
            }
            return surface_dict
    return {} 
    # return surface_dict
