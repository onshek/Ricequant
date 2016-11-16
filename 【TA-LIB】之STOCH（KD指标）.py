import talib

def init(context):
	# 定义一个全局变量, 保存要操作的证券
	context.stocks = ['000001.XSHG','000002.XSHE','000004.XSHE','000005.XSHE','000006.XSHE']
	# 设置我们要操作的股票池
	update_universe(context.stocks)

def handle_bar(context, bar_dict):

	cash = context.portfolio.cash

	for stock in context.stocks:
		hhigh = history(30, '1d', 'high')[stock]
		hlow = history(30, '1d', 'low')[stock]
		hclose = history(30, '1d', 'close')[stock]

		# 注意：STOCH函数使用的price必须是narray
		slowk, slowd = talib.STOCH(hhigh.values, hlow.values, hclose.values, 
									fastk_period=9, slowk_period=3, slowk_matype=0,
									slowd_period=3, slowd_matype=0)

		slowk = slowk[-1]
		slowd = slowd[-1]

		current_position = context.portfolio.positions[stock].quantity

		current_price = bar_dict[stock].close

		if slowk > 90 or slowd > 90 and current_position >= 0:
			order_target_percent(stock, 0)

		if slowk < 10 or slowd < 10 and current_position <= 0:
			number_of_shares = int(cash / current_price)

			if number_of_shares > 0:

				order_shares(stock, number_of_shares)