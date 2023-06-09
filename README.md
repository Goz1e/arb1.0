![image](https://user-images.githubusercontent.com/80681802/236701616-1532eede-644c-48de-b599-d31bd2a41eca.png)

__Arby 1.0 is a Triangular Arbitrage aggregator with support for crypto exchanges(surface arbitrage opportunities)__

__THE ALGORITHM (high level):__

- STEP 0: The Algorithm sorts the price ticker to compile a list of unique arbitrage pairs
then goes on to save this data. the output is an array of unique pairs similar to the data below
[{BTCETH, BTCUSDT, USDT_ETH},...].

- STEP 1: Get the latest prices for each pair in the returned array from step-0 and pretend-trade the orderbook of pairs checking for positive
values which are returned to the user.

Triangular Arbitrage explained ==> https://academy.binance.com/en/articles/what-is-triangular-arbitrage-and-how-to-use-it

__DESIGN CHOICES:__ 

-  I opted to skip the STEP-0 by hosting the the returned data for each exchange on AWS S3, this enables the Arby focus 
    on getting latest prices and calculating arbitrage opportunities
    
-  I implementated 0Auth authentication for an easy onboarding process

-  I chose Redoc API over swagger UI documentatin just because it looks better 😎

-  Implemented a throttle of 50 API calls /day just because i can 💪


__LESSONS FROM PROJECT:__

-  Better my understanding of working with APIs

-  Enhance my knowledge of django Rest Framework and it's API documentation processes

-  Utilization of AWS s3 buckets

![image](https://user-images.githubusercontent.com/80681802/236693433-c39fe82b-afb1-4c83-a863-11f9b37e8545.png)
