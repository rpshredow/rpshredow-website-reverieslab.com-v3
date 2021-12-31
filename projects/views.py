from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse

#from .models import Post
import json

from PIL import Image
import requests, math
from io import BytesIO


def terrain(request):
    return render(request, 'projects/terrain.html', {'title': '3D Terrain App'})


def cluster(request):
    return render(request, 'projects/cluster.html', {'title': 'Raspberry Pi Cluster'})


def thesis(request):
    return render(request, 'projects/thesis.html', {'title': 'Masters Thesis'})


def fpgann(request):
    return render(request, 'projects/fpgann.html', {'title': 'FPGA Neural Network'})


def stock(request):
    return render(request, 'projects/stock.html', {'title': 'Show stock price'})


def price(request):
    stock = request.GET['stock']

    stock = stock.upper()

    td_consumer_key = 'WBQGUZ4CQPRMK7HF2MXHGHUE5BNMW4P9'

    endpoint = 'https://api.tdameritrade.com/v1/marketdata/{stock_ticker}/quotes?'

    full_url = endpoint.format(stock_ticker=stock)

    page = requests.get(url=full_url, params={'apikey': td_consumer_key})

    content = json.loads(page.content)

    data = content[stock]

    symbol = data['symbol']
    description = data['description']
    bidPrice = data['bidPrice']
    askPrice = data['askPrice']
    lastPrice = data['lastPrice']
    openPrice = data['openPrice']
    highPrice = data['highPrice']
    lowPrice = data['lowPrice']
    closePrice = data['closePrice']
    totalVolume = data['totalVolume']
    fiftyTwoWkHigh = data['52WkHigh']
    fiftyTwoWkLow = data['52WkLow']
    peRatio = data['peRatio']
    divAmount = data['divAmount']
    divYield = data['divYield']
    divDate = data['divDate']

    return render(request, 'projects/price.html', {
        'symbol': symbol,
        'description': description,
        'bidPrice': bidPrice,
        'askPrice': askPrice,
        'lastPrice': lastPrice,
        'openPrice': openPrice,
        'highPrice': highPrice,
        'lowPrice': lowPrice,
        'closePrice': closePrice,
        'totalVolume': totalVolume,
        'fiftyTwoWkHigh': fiftyTwoWkHigh,
        'fiftyTwoWkLow': fiftyTwoWkLow,
        'peRatio': peRatio,
        'divAmount': divAmount,
        'divYield': divYield,
        'divDate': divDate,
    })


def terrainapp(request):

    latitude = float(request.GET.get('lat', None))
    longitude = float(request.GET.get('lon', None))
    zoom = int(request.GET.get('zoom', None))

    ytile = math.floor((1-math.log(math.tan(latitude*math.pi/180) + 1/math.cos(latitude*math.pi/180))/math.pi)/2 * math.pow(2,zoom))
    xtile = math.floor((longitude+180)/360*math.pow(2,zoom))

    endpoint = 'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'

    full_url = endpoint.format(z=zoom, x=xtile, y=ytile)

    response = requests.get(full_url)
    img = Image.open(BytesIO(response.content))

    pix = img.convert('RGB')

    heights = {}
    k = 0

    for i in range(256):
        for j in range(256):
            r, g, b = pix.getpixel((i,j))
            height = (r * 256 + g + b / 256) - 32768
            heights[k] = height
            # print(heights[k])
            k += 1

    # return render(request, 'projects/terrainapp.html', {'heights': heights})

    return JsonResponse({"heights":heights}, status = 200)
