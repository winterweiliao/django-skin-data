# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
firstone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from . import views


urlpatterns = [
    # url(r'^product/view_one$', views.view_one, name='product_view_one'),
    # url(r'^product/view_two$', views.view_two, name='product_view_two'),
    url(r'^$', views.home_page, name='home_page'),
    url(r'^product/$', views.index, name='product_index'),
    url(r'^product/quotes$', views.quotes, name='product_quotes'),
    url(r'^product/candlestick-steam-skins$', views.candlestick, name='product_candlestick'),
    url(r'^product/candlestick-steam-skins-data$', views.candlestick_data, name='product_candlestick_data'),
    url(r'^product/dashboard-igv-(?P<app_code>\d+)$', views.dashboard_igv, name='product_dashboard_igv'),
    url(r'^product/spider_write_trade_flow$', views.spider_write_trade_flow, name='spider_write_trade_flow'),
    url(r'^product/spider_write$', views.spider_write, name='product_spider_write'),
    url(r'^product/spider_write_trade_flow$', views.spider_write_trade_flow, name='spider_write_trade_flow'),
    url(r'^product/spider_write_day_line$', views.spider_write_day_line, name='product_spider_write_day_line'),
]
