from django.shortcuts import render
from django.contrib import messages
from poloniex.main import step_1
from binance.main import step_1 as binance1
from uniswapV3.main import step_1 as uniswap1
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os, json, boto3
from django.templatetags.static import static


# Intatntitating s3 bucket 
s3 = boto3.resource('s3',
aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"],
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'])
bucket = s3.Bucket('arby1.0')

@login_required(login_url='accounts:index')
def dashboard(request):    
    template_name = 'arb/dashboard.html'
    context = {'title':'dashboard'}
    return render(request,template_name,context)


@login_required(login_url='accounts:index')
def poloniex(request):
    poloniex_s3_obj = bucket.Object('static/arb/json/poloniex_tpair_list.json').get()
    byte_array = poloniex_s3_obj['Body'].read()
    data = json.loads(byte_array)
    arb_list = step_1(data)

    template_name = 'arb/detail.html'
    context = {'title':'poloniex'}
    if arb_list != None:
        context['arb_list'] = arb_list
    # messages.info(request, "constantly refresh this page to get latest data!")
    return render(request,template_name,context)

@login_required(login_url='accounts:index')
def binance(request):
    
    binance_obj = bucket.Object('static/arb/json/binance_tpairs_list.json').get()
    byte_array = binance_obj['Body'].read()
    data = json.loads(byte_array)
    arb_list = binance1(data)
   
    template_name = 'arb/detail.html'
    context = {'title':'binance'}
    if arb_list != None:
        context['arb_list'] = arb_list
    return render(request,template_name,context)

@login_required(login_url='accounts:index')
def uniswapV3(request):
    uniswap_s3_obj = bucket.Object('static/arb/json/structured_pairs.json').get()
    byte_array = uniswap_s3_obj['Body'].read()
    data = json.loads(byte_array)
    arb_list = uniswap1(data)

    template_name = 'arb/detail.html'
    context = {'title':'uniswapV3-surface-R'}
    if arb_list != None:
        context['arb_list'] = arb_list
    return render(request,template_name,context)
