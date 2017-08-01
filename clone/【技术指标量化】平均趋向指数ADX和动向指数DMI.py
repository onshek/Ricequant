import talib 
import numpy as np 
import pandas
import math

def init(context):

    context.s1 = "000001.XSHE"
    context.benchmark = "00001.XSHE"

    context.SHORTMA = 5
    context.LONGMA = 20
    context.OBVERCATION = 100

    context.ADXPERIOD = 14

def handle_bar(context, bar_dict):

    high = history(context.OBVERCATION, '1d', 'high')[context.s1].values
    low = history(context.OBVERCATION, '1d', 'low')[context.s1].values
    close = history(context.OBVERCATION, '1d', 'close')[context.s1].values

    ADX = tab.ADX(high, low, close, context.ADXPERIOD)
    