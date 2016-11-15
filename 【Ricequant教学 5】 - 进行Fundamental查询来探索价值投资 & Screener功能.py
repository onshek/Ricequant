#会在策略开始前触发一次，我们可以从get_fundamentals函数中更新我们的股票池并且保存查询获得的数据以作之后使用。
def init(context):
	# 查询revenue前十名的公司的股票并且他们的pe_ratio在25和30之间。打fundamentals的时候会有auto-complete方便写查询代码。
	fundamental_df = get_fundamentals(
		query(
			fundamentals.income_statement.revenue, fundamentals.eod_derivative_indicator.pe_ratio
		).filter(
			fundamentals.eod_derivative_indicator.pe_ratio > 55
		).filter(
			fundamentals.eod_derivative_indicator.pe_ratio < 60
		).order_by(
			fundamentals.income_statement.revenue.desc()
		).limit(
			10
		)
	)

	# 将查询结果dataframe的fundamental_df存放在context里面以备后面只需：
	context.fundamental_df = fundamental_df

	# 实时打印日志看下查询结果，会有我们精心处理的数据表格显示：
	logger.info(context.fundamental_df)

	# 对于每一个股票按照平均现金买入：
	context.stocks = context.fundamental_df.columns.values
	stockNumber = len(context.stocks)
	context.average_percent = 0.99 / stockNumber
	logger.info("Calculated average percent for each stock is: %f" % context.average_percent)
	context.field = False

	# 把这些查询出来的股票加入股票池，并非强制要求做。
	update_universe(context.fundamental_df.columns.values)

#	原代码中有问题
#	field 写成了 fired
def handle_bar(context, dict_bar):
	if not context.field:
		for stock in context.stocks:
			order_target_percent(stock, context.average_percent)
			logger.info("Bought: " + str(context.average_percent) + "% for stock: " + str(stock))
		context.field = True