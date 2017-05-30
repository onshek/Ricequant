import talib

def init(context):
    
    context.SHORTPERIOD = 12
    context.LONGPERIOD = 26
    context.SMOOTHPERIOD = 9
    context.OBSERVATION = 100
    
    scheduler.run_daily(rebalance, 8)
    
def before_trading(context):
    fundamental_df = get_fundamentals(
        query(
            fundamentals.eod_derivative_indicator.market_cap
        ).order_by(
            fundamentals.eod_derivative_indicator.market_cap.desc()
        ).limit(
            10
        )
    )

    context.fundamental_df = fundamental_df

    # 对于每一个股票按照平均现金买入：
    context.stocks = context.fundamental_df.columns.values
    stocksNumber = len(context.stocks)
    context.average_percent = 0.99 / stocksNumber
    logger.info("Calculated average percent for each stock is: %f" % context.average_percent)
    context.fired = False

    update_universe(context.fundamental_df.columns.values)

        
def handle_bar(context, bar_dict):
    pass

def rebalance(context, bar_dict):
    for stock in context.portfolio.positions:
        if stock not in context.stocks:
            order_target_percent(stock, 0)
            
    for stock in context.stocks:            
    # 对于选择出来的股票按照平均比例买入：
        prices = history_bars(stock,context.OBSERVATION,'1d','close')
        macd, signal, hist = talib.MACD(prices, context.SHORTPERIOD,
                            context.LONGPERIOD, context.SMOOTHPERIOD)
        if macd[-1] - signal[-1] < 0 and macd[-2] - signal[-2] > 0:
            # 计算现在portfolio中股票的仓位
            curPosition = context.portfolio.positions[stock].quantity
            #进行清仓
            if curPosition > 0:
                order_target_value(stock, 0)
            # 如果短均线从下往上突破长均线，为入场信号
        if macd[-1] - signal[-1] > 0 and macd[-2] - signal[-2] < 0:
            # 满仓入股
            order_target_percent(stock, context.average_percent)
        logger.info("Bought: " + str(context.average_percent) + " % for stock: " + str(stock))
        context.fired = True