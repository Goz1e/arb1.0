from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework import permissions


app_name = "api"
urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('binance/', views.BinanceArbs.as_view(), name='binance'),
    path('poloniex/', views.PoloniexArbs.as_view(), name='poloniex'),
    path('uniswapV3/', views.UniswapV3Arbs.as_view(), name='uniswapV3'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
