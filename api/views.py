from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
# from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from binance.main import step_1 as binance1
from poloniex.main import step_1 as poloniex1
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request):
    """
    Provides a list of basic url endpoints
    """
    return Response({
        'binance-arbs': reverse('api:binance', request=request, format=format),
        'poloniex-arbs': reverse('api:poloniex', request=request, format=format)
    })

class BinanceArbs(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Return a list of arbitrage opportunities on binance.
        """
        arb_list = binance1()
        return Response(arb_list)


class PoloniexArbs(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Return a list of arbitrage opportunities on poloniex
        """
        arb_list = poloniex1()
        return Response(arb_list)

