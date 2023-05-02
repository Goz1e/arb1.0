
from django.urls import path
from .views import dashboard, poloniex, binance, uniswapV3

app_name = "arb"
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('binance/', binance, name='binance'),
    path('poloniex/', poloniex, name='poloniex'),
    path('uniswapV3/', uniswapV3, name='uniswap'),
]
