import json, requests
import os
try:
    from .func import *
except ImportError:
    from func import *
import time

def retrieve_uniswap_information():

    query = """
        query {
            pools(
                orderBy: totalValueLockedETH,
                orderDirection : desc,
                first:400
            ){
                id
                totalValueLockedETH
                token0Price
                token1Price
                feeTier
                token0{id symbol name decimals}
                token1{id symbol name decimals}
            }
        }
    """

    url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
    req = requests.post(url,json={'query':query})
    to_json = json.loads(req.text)
    return to_json


def step_0():
    pairs_list = retrieve_uniswap_information()['data']['pools']
    structured_pairs = structure_triangular_pairs(pairs_list)

    # <====saving strucured pairs=====>
    with open("structured_pairs.json", "w") as fp:
        json.dump(structured_pairs,fp)


def step_1():
    saved_file = os.getcwd() + r'\uniswapV3\structured_pairs.json'
    with open(saved_file,'r') as fp:
        structured_pairs = json.load(fp) 

    # calculating surface rates
    limit = int(len(structured_pairs))
    print(limit)
    surface_rates_list = []
    for t_pair in structured_pairs[0:limit]:
        surface_rate = calc_triangular_arb_surface_rate(t_pair,min_rate=1)
        if len(surface_rate) >1:
            surface_rates_list.append(surface_rate)
    return surface_rates_list
   
# step_0()
# step_1()