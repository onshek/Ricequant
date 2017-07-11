def init(context):
    context.count_1 = 0
    context.count_2 = 0
    scheduler.run_daily(rebalance, 10)
    logger.info("RunInfo: {}".format(context.run_info))

def before_trading(context):

    stocks_number = len(pick_stocks_1().columns.values)
    if stocks_number > 42:
        number_more_than_42 = int(stocks_number * 0.5882) + 1
        return number_more_than_42

    #print(stocks_number)
    #print(number_more_than_42)

    # 获取最近 16 个交易日的沪深 300 指数信息
    data = history_bars('沪深300', 16, '1d', 'close')
    #print(data)
    # 当天沪深 300 指数信息
    data_today = data[-1]
    #print(data_today)
    # 16 天前沪深 300 指数信息
    data_16_day_ago = data[0]
    #print(data_16_day_ago)
    print("data_today - data_16_day_ago:", data_today - data_16_day_ago)

    if data_today <= data_16_day_ago:
        if stocks_number <= 25:
            context.fundamental_df = pick_stocks_1() 
            #context.stocks = context.fundamental_df.columns.values
            #real_stocks_number = len(context.stocks)              
        elif 25< stocks_number <= 42:
            context.fundamental_df = pick_stocks_3
            #context.stocks = context.fundamental_df.columns.values
            #real_stocks_number = len(context.stocks)              
        elif stocks_number > 42:
            context.fundamental_df = pick_stocks_2()
            #context.stocks = context.fundamental_df.columns.values
            #real_stocks_number = len(context.stocks)              
    elif data_today > data_16_day_ago:
        if stocks_number <= 25:
            context.fundamental_df = pick_stocks_1()
            #context.stocks = context.fundamental_df.columns.values
            #real_stocks_number = len(context.stocks)              
        elif 25< stocks_number <= 42:
            context.fundamental_df = pick_stocks_3()
            #context.stocks = context.fundamental_df.columns.values
            #real_stocks_number = len(context.stocks)              
        elif stocks_number > 42:
            context.fundamental_df = pick_stocks_2()
            #context.stocks = context.fundamental_df.columns.values
            #real_stocks_number = len(context.stocks)              

    #print(context.fundamental_df)
    context.stocks = context.fundamental_df.columns.values
    stocks_number = len(context.stocks)
    update_universe(context.fundamental_df.columns.values)
    #print('验证 stocks_number', stocks_number)
    #logger.info(context.stocks)


# 通过彼得林奇基层选股法前三条筛选出符合的A股股票
def pick_stocks_1():
    fundamental_df_1 = get_fundamentals(
        query(
        ).filter(
            fundamentals.financial_indicator.debt_to_asset_ratio <= 25 # 资产负债率小于等于25%
        ).filter(
            fundamentals.financial_indicator.cash_flow_from_operations_per_share > 0 # 每股净现金大于0
        ).filter(
            fundamentals.eod_derivative_indicator.pcf_ratio_1 < 11 # 当前股价与每股自由现金流量比小于11
        )
    )
    return fundamental_df_1

    #logger.info(context.fundamental_df)
    #update_universe(context.fundamental_df.columns.values)

# 当剩下的股票大于42支时，筛选其中资产负债率最小的58.82%的股票，再从其中选取经营现金流与价格比最小的25支股票
def pick_stocks_2():

    fundamental_df = pick_stocks_1()
    context.stocks = context.fundamental_df.columns.values
    stocks_number = len(context.stocks)
    number_more_than_42 = int(stocks_number * 0.5882) + 1

    fundamental_df_2 = get_fundamentals(
        query(
            fundamentals.financial_indicator.debt_to_asset_ratio, # 资产负债率
            fundamentals.feod_derivative_indicator.pcf_ratio # 市现率
        ).filter(
            fundamentals.financial_indicator.debt_to_asset_ratio <= 25 # 资产负债率小于等于25%
        ).filter(
            fundamentals.financial_indicator.cash_flow_from_operations_per_share > 0 # 每股净现金大于0
        ).filter(
            fundamentals.eod_derivative_indicator.pcf_ratio_1 < 11 # 当前股价与每股自由现金流量比小于11
        ).order_by(
            fundamentals.financial_indicator.debt_to_asset_ratio.asc()
        ).limit(
            number_more_than_42,
            25
        )
    )
    return fundamental_df_2


# 当剩下的股票大于25支但小于42支时，筛选经营现金流与价格比最小的25支股票
def pick_stocks_3():
    fundamental_df_3 = get_fundamentals(
        query(
            fundamentals.feod_derivative_indicator.pcf_ratio # 市现率
        ).filter(
            fundamentals.financial_indicator.debt_to_asset_ratio <= 25 # 资产负债率小于等于25%
        ).filter(
            fundamentals.financial_indicator.cash_flow_from_operations_per_share > 0 # 每股净现金大于0
        ).filter(
            fundamentals.eod_derivative_indicator.pcf_ratio_1 < 11 # 当前股价与每股自由现金流量比小于11
        ).order_by(
            fundamentals.feod_derivative_indicator.pcf_ratio.asc()
        ).limit(
            25
        )
    )
    return fundamental_df_3


def handle_bar(context, bar_dict):
    pass


def rebalance(context, bar_dict):
    
    # 获取最近 16 个交易日的沪深 300 指数信息
    data = history_bars('沪深300', 16, '1d', 'close')
    #print(data)
    # 当天沪深 300 指数信息
    data_today = data[-1]
    #print(data_today)
    # 16 天前沪深 300 指数信息
    data_16_day_ago = data[0]
    #print(data_16_day_ago)
    
    context.stocks = context.fundamental_df.columns.values
    stocks_number = len(context.stocks)
    if stocks_number == 0:
        context.average_percent = 0
    else:
        context.average_percent = 0.99 / stocks_number
    print("context.stocks:", context.stocks)
    print('stocks_number:', stocks_number)
    #print("context.average_percent:", context.average_percent)
        
    # 对不在更新后股票池内的股票除名
    if stocks_number != 0:
        for stock in context.portfolio.positions:
            if stock not in context.stocks:
                order_target_percent(stock, 0)
    
    if data_today < data_16_day_ago:
        if context.count_1 == 2:
            context.count_1 = 0

            if stocks_number >= 25:  
                for stock in context.stocks:     
                    order_target_percent(stock, context.average_percent)
                    logger.info("Bought: " + str(100 * context.average_percent) + " % for stock: " + str(stock))

            elif 0 < stocks_number <25:
                context.fundamental_df = get_fundamentals(
                    query(
                        fundamentals.eod_derivative_indicator.pcf_ratio_1
                    ).filter(
                        fundamentals.income_statement.stockcode.in_(context.stocks)
                    )
                )

                sum = 0
                for i in range(0, stocks_number):
                    sum = sum + (1 / context.fundamental_df.T.pcf_ratio_1[i])

                #print("sum:", sum)

                for i in range(0, stocks_number):
                    percent = (1 / context.fundamental_df.T.pcf_ratio_1[i]) / sum
                    order_target_percent(context.stocks[i], percent)
                    logger.info("Bought: " + str(100 * percent) + " % for stock: " + str(context.stocks[i]))

            else:
                pass        
        else:
            context.count_1 += 1


    else:
        if context.count_2 == 14:
            context.count_2 = 0

            if stocks_number >= 25:  
                for stock in context.stocks:     
                    order_target_percent(stock, context.average_percent)
                    logger.info("Bought: " + str(100 * context.average_percent) + " % for stock: " + str(stock))

            elif 0 < stocks_number <25:
                for stock in context.stocks: 
                    #print(stock)
                    order_target_percent(stock, context.average_percent)
                    logger.info("Bought: " + str(100 * context.average_percent) + " % for stock: " + str(stock))

            else:
                pass

        else:
            context.count_2 += 1


def after_trading(context):
    pass

