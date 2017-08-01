import talib
import numpy as np 
import math
import pandas

def init(context):

	context.s1 = "招商证券"
	context.OBSERVATION = 20
	context.SMA = 10

def handle_bar(context, bar_dict):

	high = history(context.OBSERVATION, '1d', 'high')[context.s1].values
	low = history(context.OBSERVATION, '1d', 'low')[context.s1].values
	close = history(context.OBSERVATION, '1d', 'close')[context.s1].values
	MIX = (high + low + close) / 3

	SMA = talib.SMA(MIX, context.SMA)

	currentPrice = bar_dict[context.s1].close

	curPosition = context.portfolio.positions[context.s1].quantity

	shares = context.portfolio.cash / bar_dict[context.s1].close

	plot('currentPrice', currentPrice)
	plot('SMA', SMA[-1])

	if currentPrice > SMA[-1] and curPosition == 0:
		order_target_percent(context.s1, 0.99)

	if currentPrice < SMA[-1] and curPosition != 0:
		order_target_percent(context.s1, 0)