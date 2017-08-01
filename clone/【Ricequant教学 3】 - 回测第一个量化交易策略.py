def init(context):
	context.s1 = '000001.XSHE'
	context.slippage = 0.05
	context.commission = .08	# 和默认数值相同，可以省略代码
	update_universe([context.s1])

def handle_bar(context, bar_dict):
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

	plot('close', bar_dict[context.s1].close)
	plot('short_avg', MA_short)
	plot('long_avg', MA_long)