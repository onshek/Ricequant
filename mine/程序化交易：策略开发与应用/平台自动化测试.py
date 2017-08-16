def init(context):
    context.s1 = "000001.XSHE"
    logger.info("RunInfo: {}".format(context.run_info))

    scheduler.run_daily(test)
    print('1.scheduler.run_daily pass')
    
    scheduler.run_weekly(test, tradingday=1)
    print('2.scheduler.run_weekly pass')

    scheduler.run_monthly(test, tradingday=1, time_rule=market_open(minute=10))
    print('3.scheduler.run_monthly pass')
    print('4.time_rule pass')
    
    get_fundamentals(query, entry_date=None, interval='1d', report_quarter=False)
    print('5.get_fundamentals pass')
    
    all_instruments(type=None)
    print('6.all_instruments pass')
    
    instruments(context.s1)
    print('7.instruments pass')
    
    
def before_trading(context):
    get_price(context.s1, start_date='2016-01-04', end_date='2016-01-04')
    print('8.get_pric pass')

def test(context, bar_dict):
    pass

def handle_bar(context, bar_dict):
    
    order_shares(context.s1, 1000)
    print('9.order_shares pass')
    
    order_lots(context.s1, 20)
    print('10.order_lots pass')

    order_value(context.s1, 10000)
    print('11.order_value pass')
    
    order_percent(context.s1, 0.05)
    print('12.order_percent pass')
    
    order_target_percent(context.s1, 0.05)
    print('13.order_target_percent pass')
    
    get_open_orders()
    print('14.get_open_orders pass')

    context.now
    print('15.context.now pass')
    
    context.stock_account
    print('16.context.stock_account pass')
    
    context.run_info
    print('17.context.run_info pass')
    
    context.universe
    print('18.context.universe pass')
    
    history_bars(context.s1, 5, '1d', 'close')
    print('19.history_bars pass')
    
    current_snapshot(context.s1)
    print('20.current_snapshot pass')
    
    get_securities_margin(context.s1, count=5)
    print('21.get_securities_margin pass')
    
    get_shares(context.s1, count=5, fields='total')
    print('22.get_shares pass')
    
    get_turnover_rate(context.s1, count=5)
    print('23.get_turnover_rate pass')
    
    industry('A01')
    print('24.industry pass')
    
    sector("consumer discretionary")
    print('25.sector pass')
    
    concept('民营医院')
    print('26.concept pass')
    
    index_components('000001.XSHG')
    print('27.index_components pass')
    
    get_dividend(context.s1, start_date='2016-01-04')
    print('28.get_dividend pass')
    
    get_split(context.s1, start_date='2016-01-04')
    print('29.get_split pass')
    
    get_trading_dates(start_date='2016-01-04', end_date='2016-01-04')
    print('30.get_trading_dates pass')
    
    get_previous_trading_date(date='2016-01-04')
    print('31.get_previous_trading_date pass')
    
    get_next_trading_date(date='2016-01-04')
    print('32.get_next_trading_date pass')
    
    get_price_change_rate(context.s1, 1)
    print('33.get_price_change_rate pass')
    
    get_yield_curve('2016-01-04')
    print('34.get_yield_curve pass')
    
    is_suspended(context.s1, count=1)
    print('35.is_suspended pass')
    
    is_st_stock(context.s1, count=1)
    print('36.is_st_stock pass')
    
    fenji.get_a_by_yield(4)
    print('37.fenji.get_a_by_yield pass')
    
    xueqiu.top_stocks('new_comments')
    print('38.xueqiu.top_stocks pass')
    
    print('平台自动化测试完成')
    print('*' * 9)
    
def after_trading(context):
    pass