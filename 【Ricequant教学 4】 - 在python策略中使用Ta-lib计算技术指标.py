'''
疑问：
1 TEMA、DEMA不能输出
2 
'''

import pandas as pd
import numpy as np
import talib
import statsmodels

def init(context):
	context.s1 = '000001.XSHE'
	context.slippage = 0.05
	context.commission = .08	# 和默认数值相同，可以省略代码
	update_universe([context.s1])

def handle_bar(context, bar_dict):
	closematrix = history(30, '1d','close') 
	close = closematrix[context.s1].values
	MA_short = bar_dict[context.s1].mavg(20, frequency= 'day')
	MA_long = bar_dict[context.s1].mavg(50, frequency= 'day')

	# 计算现在portfolio中股票的仓位
	current_position = context.portfolio.positions[context.s1].quantity

	# 计算现在portfolio中的现金可以购买多少股票
	shares = context.portfolio.cash / bar_dict[context.s1].close

	if MA_short > MA_long and current_position == 0:
	#	order_shares(context.s1, shares)
		order_target_percent(context.s1, 1)

	if MA_short < MA_long and current_position != 0:
		order_target_percent(context.s1, 0)

#	avg = talib.SMA(close, timeperiod = 30)

#	today_mavg = avg[-1]
#	ystd_mavg = avg[-2]

	#MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)

	SMA = talib.MA(close, 30, matype=0)[-1]
	EMA = talib.MA(close, 30, matype=1)[-1]
	WMA = talib.MA(close, 30, matype=2)[-1]
	DEMA = talib.MA(close, 30, matype=3)[-1]
	TEMA = talib.MA(close, 30, matype=4)[-1]

	plot('SMA', SMA)
	plot('EMA', EMA)
	plot('WMA', WMA)
	plot('DEMA', DEMA)
	plot('TEMA', TEMA)