from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
# from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from binance.main import step_1 as binance1
from poloniex.main import step_1 as poloniex1
from uniswapV3.main import step_1 as uniswap1
from rest_framework.reverse import reverse
import os,json, boto3


# Intatntitating s3 bucket 
s3 = boto3.resource('s3',
aws_access_key_id = os.environ["AWS_ACCESS_KEY_ID"],
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'])
bucket = s3.Bucket('arby1.0')

@api_view(['GET'])
def api_root(request, format=None):
    """
    Provides a list of basic url endpoints
    """
    return Response({
        'binance-arbs': reverse('api:binance', request=request, format=format),
        'poloniex-arbs': reverse('api:poloniex', request=request, format=format),
        'uniswapV3-arbs': reverse('api:uniswapV3', request=request, format=format)
    })

class BinanceArbs(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of arbitrage opportunities on binance.
        """
        binance_obj = bucket.Object('static/arb/json/binance_tpairs_list.json').get()
        byte_array = binance_obj['Body'].read()
        data = json.loads(byte_array)
        arb_list = binance1(data)
        return Response(arb_list)


class PoloniexArbs(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of arbitrage opportunities on poloniex
        """
        poloniex_s3_obj = bucket.Object('static/arb/json/poloniex_tpair_list.json').get()
        byte_array = poloniex_s3_obj['Body'].read()
        data = json.loads(byte_array)
        arb_list = poloniex1(data)
        return Response(arb_list)

class UniswapV3Arbs(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of arbitrage opportunities on poloniex
        """
        uniswap_s3_obj = bucket.Object('static/arb/json/structured_pairs.json').get()
        byte_array = uniswap_s3_obj['Body'].read()
        data = json.loads(byte_array)
        arb_list = uniswap1(data)

        return Response(arb_list)

