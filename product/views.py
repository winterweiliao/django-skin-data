# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import time

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Min, Max, Sum, Count
from product.models import Product, PriceFlow, TradeFlow, DayLine


# Create your views here.
def view_one(request):
    items = Product.objects.values()
    html = '<h1>Product</h1><br><br><br>'
    for item in items:
        html += item.get('name') + '&nbsp;&nbsp;&nbsp;&nbsp;' + str(item.get('price')) + '<br>'

    return HttpResponse(html)


def view_two(request):
    items = PriceFlow.objects.all()
    html = '<h1>Product<h1><br><br>'
    html += 'name' + '&nbsp;&nbsp;&nbsp;&nbsp;' + 'price' + '&nbsp;&nbsp;&nbsp;&nbsp;'
    html += '开盘价' + '&nbsp;&nbsp;&nbsp;&nbsp;' + '收盘价' + '&nbsp;&nbsp;&nbsp;&nbsp;'
    html += '最低价' + '&nbsp;&nbsp;&nbsp;&nbsp;' + '最高价' + '&nbsp;&nbsp;&nbsp;&nbsp;'
    html += '<br>'
    for item in items:
        html += item.name + '&nbsp;&nbsp;&nbsp;&nbsp;' + str(item.price) + '&nbsp;&nbsp;&nbsp;&nbsp;'
        html += str(item.open_price) + '&nbsp;&nbsp;&nbsp;&nbsp;' + str(item.close_price) + '&nbsp;&nbsp;&nbsp;&nbsp;'
        html += str(item.lowest_price) + '&nbsp;&nbsp;&nbsp;&nbsp;' + str(item.highest_price) + '&nbsp;&nbsp;&nbsp;&nbsp;'
        html += '<br>'

    return render(request, 'test2/index_v2.html', locals())


def home_page(request):
    """
    主页
    :param request:
    :return:
    """
    return index(request)


def index(request):
    """

    :param request:
    :return:
    """
    return render(request, 'product/index.html', locals())


def quotes(request):
    """

    :param request:
    :return:
    """
    return render(request, 'product/quotes-from-famous-people.html', locals())


def candlestick(request):
    """

    :param request:
    :return:
    """
    return render(request, 'product/candlestick-steam-skins.html', locals())


def candlestick_data(request):
    """

    :param request:
    :return:
    """
    app_code = request.GET.get('app_code')
    name = request.GET.get('name')
    items = DayLine.objects.filter(name=name, app_code=app_code).values()
    result = {'data': []}
    for item in items:
        list0 = list()
        list0.append(item.get('trade_date').strftime('%Y-%m-%d'))
        list0.append(float(item.get('open_price')))
        list0.append(float(item.get('close_price')))
        list0.append(float(item.get('lowest_price')))
        list0.append(float(item.get('highest_price')))
        result['data'].append(list0)
    return JsonResponse(result)


def dashboard_igv(request, app_code=730):
    """
    数据分析仪表盘-igv销售记录
    :param request:
    :param app_code:
    :return:
    """
    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days=-1)

    # 今日数据分析
    items = TradeFlow.objects.filter(
        app_code=app_code, trade_time__gte=today).values('name').annotate(
        lowest_price=Min('trade_price'), volume=Count('id'), amount=Sum('trade_price'),
        latest_time=Max('trade_time')).order_by('-volume')
    total_volume = 0
    total_amount = 0
    for item in items:
        total_volume += item.get('volume')
        total_amount += item.get('amount')
    # 昨日数据分析
    items_for_yesterday = TradeFlow.objects.filter(
        app_code=app_code, trade_time__gte=yesterday, trade_time__lt=today).values('name').annotate(
        lowest_price=Min('trade_price'), volume=Count('id'), amount=Sum('trade_price'),
        latest_time=Max('trade_time')).order_by('-volume')
    total_volume_for_yesterday = 0
    total_amount_for_yesterday = 0
    for item in items_for_yesterday:
        total_volume_for_yesterday += item.get('volume')
        total_amount_for_yesterday += item.get('amount')

    return render(request, 'product/dashboard-igv.html', locals())


def spider_write(request):
    """
    爬虫写入请求
    :param request:
    :return:
    """
    market_hash_name = request.GET.get('market_hash_name')
    name = request.GET.get('name')
    price = request.GET.get('price')
    Product.objects.create(market_hash_name=market_hash_name, price=price, app_code=433850)
    count = Product.objects.filter(market_hash_name=market_hash_name, app_code=433850).count()
    if count == 10:
        p_list = Product.objects.filter(market_hash_name=market_hash_name, app_code=433850).order_by('price')[0:2]
        discount = (p_list[1].price - p_list[0].price) / p_list[1].price
        if discount >= 0.03:
            print(market_hash_name, p_list[0].price)
        Product.objects.filter(market_hash_name=market_hash_name, app_code=433850).delete()

    return HttpResponse('successfully')


def spider_write_trade_flow(request):
    """
    爬虫写入请求
    :param request:
    :return:
    """
    name = request.GET.get('name')
    market_name = request.GET.get('market_name')
    # market_hash_name = request.GET.get('market_hash_name')
    price = request.GET.get('price')
    trade_time = request.GET.get('trade_time')
    app_code = request.GET.get('app_code')

    TradeFlow.objects.get_or_create(name=name, app_code=app_code, trade_time=trade_time, trade_price=price,
                                    market_name=market_name)
    # time.sleep(1)

    return HttpResponse('successfully')


def spider_write_day_line(request):
    """
    爬虫写入请求
    :param request:
    :return:
    """
    name = request.GET.get('name')
    # market_hash_name = request.GET.get('market_hash_name')
    price = request.GET.get('price')
    lowest_price = request.GET.get('lowest_price')
    highest_price = request.GET.get('highest_price')
    open_price = request.GET.get('open_price')
    close_price = request.GET.get('close_price')
    trade_date = request.GET.get('trade_date')
    app_code = request.GET.get('app_code')

    data = dict()
    data['product_id'] = 0
    data['price'] = price
    data['lowest_price'] = lowest_price
    data['highest_price'] = highest_price
    data['open_price'] = open_price
    data['close_price'] = close_price

    DayLine.objects.get_or_create(name=name, app_code=app_code, trade_date=trade_date, **data)
    print(request.GET)

    return HttpResponse('successfully')
