def init(context):
	context.s1 = '000001.XSHE'
	update_universe([context.s1])

def handle_bar(context, bar_dict):
	MA_short = bar_dict[context.s1].magv(20, frequency= 'day')
	MA_long = bar_dict[context.s1].magv(50, frequency= 'day')

	# 计算现在portfolio中股票的仓位
	current_position = context.portfolio.positions[context.s1].quantity

	# 计算现在portfolio中的现金可以购买多少股票
	shares = context.portfolio.cash / bar_dict[context.s1].close