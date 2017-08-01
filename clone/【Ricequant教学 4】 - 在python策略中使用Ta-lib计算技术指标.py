'''
疑问：

1 已解决：TEMA、DEMA不能输出
close 所取天数应大于平均数所取的天数

2 已解决：close 怎么用
close = history(bar_count, frequency, field)	DataFrame

3 bar_dict
WARN   [Deprecated]在before_trading函数中，第二个参数bar_dict已经不再使用了
'''

import pandas as pd 
import numpy as np
import talib
import statsmodels

def init(context):
	context.s1 = '000001.XSHE'
	context.slippage = 0.05
#	和默认数值相同，可以省略代码	
	context.commission = 0.08	
	update_universe([context.s1])

def handle_bar(context, bar_dict): 
#   取100天数据，最后给出71天的移动平均
# 	返回一个pandas中的dataframe结构,Series
#	close = history(100, '1d','close')[context.s1]
#	convert Series to array
	close = history(100, '1d','close')[context.s1].values
	MA_short = bar_dict[context.s1].mavg(20, frequency= 'day')
	MA_long = bar_dict[context.s1].mavg(50, frequency= 'day')

#	计算现在portfolio中股票的仓位
	current_position = context.portfolio.positions[context.s1].quantity

#	计算现在portfolio中的现金可以购买多少股票
	shares = context.portfolio.cash / bar_dict[context.s1].close

	if MA_short > MA_long and current_position == 0:
#	order_shares(context.s1, shares)
		order_target_percent(context.s1, 1)

	if MA_short < MA_long and current_position != 0:
		order_target_percent(context.s1, 0)

#	avg = talib.SMA(close, timeperiod = 30)

#	today_mavg = avg[-1]
#	ystd_mavg = avg[-2]

#	MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
#	返回的是 array
#	只要取平均数的最后一天
#	handle_bar(context, bar_dict)是每一天调用一次

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
#	只要最后一天
	plot('close', close[-1])	



#	用Ta-lib来写一个MACD策略

#	普通的MACD运算公式如下，默认均线为EMA不可选
#	macd, macdsignal, macdhist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

#	可以使用其他均线的扩展版本如下，这时候你就可以随便选不同的均线
#	macd, macdsignal, macdhist = MACDEXT(close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)

#	另外同样是以均线为基础扩展的常见指标bollinger bands, 也可以选择matype
#	upperband, middleband, lowerband = BBANDS(close, timeperiod=5, nbdevup=2, nbdecdn=2, matype=0)

	close = history(26, '1d', 'close')[context.s1].values
	macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
	plot('MACD', macd[-1])
	plot('MACD SIGNAL', macdsignal[-1])
	plot('MACD HIST', macdhist[-1])


import talib
import numpy
import pandas

def init(context):
	context.s1 = '000023.XSHE'

def handle_bar(context, bar_dict):

	close = history(50, '1d', 'close')[context.s1].values
	macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)

	curPosition = context.portfolio.positions[context.s1].quantity

	if macd[-1]>0 and curPosition== 0 :
		order_target_percent(context.s1, 1)

	if macd[-1]<0 and curPosition != 0:
		order_target_percent(context.s1, 0)

	if macd[-1]>macdsignal[-1] and curPosition == 0:
		order_target_percent(context.s1, 1)

	if macd[-1]<macdsignal[-1] and curPosition != 0:
		order_target_percent(context.s1, 0)