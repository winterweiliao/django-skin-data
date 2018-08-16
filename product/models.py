# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    market_hash_name = models.CharField(max_length=255, null=True)
    market_name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    app_code = models.PositiveIntegerField(default=0)
    create_time = models.DateTimeField(auto_now=True, editable=False, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)


class PriceFlow(models.Model):
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=255, default='')
    app_code = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    open_price = models.DecimalField(max_digits=13, decimal_places=2)
    close_price = models.DecimalField(max_digits=13, decimal_places=2)
    lowest_price = models.DecimalField(max_digits=13, decimal_places=2)
    highest_price = models.DecimalField(max_digits=13, decimal_places=2)
    trade_date = models.DateTimeField(null=True, help_text='')
    note = models.CharField(max_length=255, null=True, help_text="")
    create_time = models.DateTimeField(auto_now=True, editable=False, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'product_price_flow'


class DayLine(models.Model):
    product = models.ForeignKey(Product, db_constraint=False)
    name = models.CharField(max_length=255, default='')
    app_code = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    open_price = models.DecimalField(max_digits=13, decimal_places=2)
    close_price = models.DecimalField(max_digits=13, decimal_places=2)
    lowest_price = models.DecimalField(max_digits=13, decimal_places=2)
    highest_price = models.DecimalField(max_digits=13, decimal_places=2)
    trade_date = models.DateTimeField(null=True, help_text='')
    note = models.CharField(max_length=255, null=True, help_text="")
    create_time = models.DateTimeField(auto_now=True, editable=False, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'product_day_line'


class TradeFlow(models.Model):
    product = models.ForeignKey(Product, db_constraint=False, default=0)
    name = models.CharField(max_length=255, null=True)
    market_name = models.CharField(max_length=255, null=True)
    market_hash_name = models.CharField(max_length=255, null=True)
    app_code = models.PositiveIntegerField(default=0)
    trade_price = models.DecimalField(max_digits=13, decimal_places=2, help_text='成交价格')
    trade_time = models.DateTimeField(null=True, help_text='成交时间')
    create_time = models.DateTimeField(auto_now=True, editable=False, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'product_trade_flow'
