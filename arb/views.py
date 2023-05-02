from django.shortcuts import render
from django.contrib import messages
from poloniex.main import step_1
from binance.main import step_1 as binance1
from uniswapV3.main import step_1 as uniswap1
# Create your views here.
def dashboard(request):
    template_name = 'arb/dashboard.html'
    context = {'title':'dashboard'}
    return render(request,template_name,context)

def poloniex(request):
    arb_list = step_1()
    template_name = 'arb/detail.html'
    context = {'title':'poloniex'}
    if arb_list != None:
        context['arb_list'] = arb_list
    # messages.info(request, "constantly refresh this page to get latest data!")
    return render(request,template_name,context)

def binance(request):
    arb_list = binance1()
    template_name = 'arb/detail.html'
    context = {'title':'binance'}
    if arb_list != None:
        context['arb_list'] = arb_list
    return render(request,template_name,context)

def uniswapV3(request):
    arb_list = uniswap1()
    print("++==",len(arb_list))
    template_name = 'arb/detail.html'
    context = {'title':'uniswapV3-surface-R'}
    if arb_list != None:
        context['arb_list'] = arb_list
    return render(request,template_name,context)
