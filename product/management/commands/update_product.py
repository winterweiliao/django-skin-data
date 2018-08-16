# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import random
import decimal

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Min, Max, Avg
from product.models import PriceFlow, TradeFlow, DayLine


def update_product(app_code=0):
    """

    :param app_code:
    :return:
    """
    start_time = datetime.datetime(2017, 6, 1)
    while start_time <= datetime.datetime.now() + datetime.timedelta(days=-1):
        end_time = start_time + datetime.timedelta(days=1)
        items = TradeFlow.objects.filter(
            app_code=app_code, trade_time__gte=start_time, trade_time__lt=end_time).values('name').annotate(
            highest_price=Max('trade_price'), lowest_price=Min('trade_price'), avg_price=Avg('trade_price'))

        for item in items:
            prices = [item.get('lowest_price'), item.get('highest_price'), item.get('avg_price')]
            data = dict()
            data['product_id'] = 0
            data['lowest_price'] = item.get('lowest_price')
            data['highest_price'] = item.get('highest_price')
            # data['open_price'] = (float(random.choice(prices)) + float(random.choice(prices))) / 2
            # data['close_price'] = data['price'] = (float(random.choice(prices)) + float(random.choice(prices))) / 2
            open_obj = TradeFlow.objects.filter(
                app_code=app_code, name=item.get('name'), trade_time__gte=start_time,
                trade_time__lt=start_time + datetime.timedelta(hours=2)).aggregate(avg_price=Avg('trade_price'))
            print open_obj
            data['open_price'] = open_obj.get('avg_price') if open_obj.get('avg_price') else item.get('lowest_price')
            close_obj = TradeFlow.objects.filter(
                app_code=app_code, name=item.get('name'), trade_time__lt=end_time,
                trade_time__gte=end_time - datetime.timedelta(hours=2)).aggregate(avg_price=Avg('trade_price'))
            data['close_price'] = close_obj.get('avg_price') if close_obj.get('avg_price') else item.get('highest_price')
            data['price'] = data['close_price']
            if DayLine.objects.filter(name=item.get('name'), app_code=app_code, trade_date=start_time).first():
                print ('exist', item)
            else:
                DayLine.objects.create(name=item.get('name'), app_code=app_code, trade_date=start_time, **data)
                print item

        start_time = end_time
    pass


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        update_product(app_code=730)
        self.stdout.write('Successfully')
        # items = PriceFlow.objects.all().values()
        # for item in items:
        #     self.stdout.write(repr(item))
