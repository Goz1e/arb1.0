from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,
    TokenRefreshView,TokenVerifyView,)
from rest_framework.schemas import get_schema_view
from django.views.generic.base import TemplateView

app_name = "api"
urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('binance/', views.BinanceArbs.as_view(), name='binance'),
    path('poloniex/', views.PoloniexArbs.as_view(), name='poloniex'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('schema/', get_schema_view(
        title = 'Arby',
        description = "API for arby",
        version='1.0.0'), name='openapi-schema'
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)