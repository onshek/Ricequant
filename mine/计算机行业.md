import pandas as pd
import numpy as np


def init(context):
    context.counts = 0
    context.stocks = ['000021.XSHE',
					 '000034.XSHE',
					 '000066.XSHE',
					 '000158.XSHE',
					 '000555.XSHE',
					 '000606.XSHE',
					 '000662.XSHE',
					 '000938.XSHE',
					 '000948.XSHE',
					 '000977.XSHE',
					 '000997.XSHE',
					 '002063.XSHE',
					 '002065.XSHE',
					 '002072.XSHE',
					 '002152.XSHE',
					 '002153.XSHE',
					 '002177.XSHE',
					 '002195.XSHE',
					 '002197.XSHE',
					 '002230.XSHE',
					 '002232.XSHE',
					 '002253.XSHE',
					 '002268.XSHE',
					 '002279.XSHE',
					 '002280.XSHE',
					 '002296.XSHE',
					 '002308.XSHE',
					 '002312.XSHE',
					 '002331.XSHE',
					 '002362.XSHE',
					 '002368.XSHE',
					 '002373.XSHE',
					 '002376.XSHE',
					 '002380.XSHE',
					 '002383.XSHE',
					 '002401.XSHE',
					 '002405.XSHE',
					 '002410.XSHE',
					 '002421.XSHE',
					 '002439.XSHE',
					 '002474.XSHE',
					 '002512.XSHE',
					 '002528.XSHE',
					 '002577.XSHE',
					 '002609.XSHE',
					 '002642.XSHE',
					 '002649.XSHE',
					 '002657.XSHE',
					 '002766.XSHE',
					 '002771.XSHE',
					 '002777.XSHE',
					 '002835.XSHE',
					 '002869.XSHE',
					 '300002.XSHE',
					 '300010.XSHE',
					 '300020.XSHE',
					 '300033.XSHE',
					 '300036.XSHE',
					 '300042.XSHE',
					 '300044.XSHE',
					 '300045.XSHE',
					 '300047.XSHE',
					 '300065.XSHE',
					 '300074.XSHE',
					 '300075.XSHE',
					 '300079.XSHE',
					 '300085.XSHE',
					 '300096.XSHE',
					 '300130.XSHE',
					 '300150.XSHE',
					 '300155.XSHE',
					 '300166.XSHE',
					 '300167.XSHE',
					 '300168.XSHE',
					 '300170.XSHE',
					 '300177.XSHE',
					 '300182.XSHE',
					 '300188.XSHE',
					 '300202.XSHE',
					 '300209.XSHE',
					 '300212.XSHE',
					 '300229.XSHE',
					 '300231.XSHE',
					 '300235.XSHE',
					 '300245.XSHE',
					 '300248.XSHE',
					 '300253.XSHE',
					 '300264.XSHE',
					 '300270.XSHE',
					 '300271.XSHE',
					 '300277.XSHE',
					 '300287.XSHE',
					 '300288.XSHE',
					 '300290.XSHE',
					 '300297.XSHE',
					 '300300.XSHE',
					 '300302.XSHE',
					 '300311.XSHE',
					 '300324.XSHE',
					 '300330.XSHE',
					 '300333.XSHE',
					 '300339.XSHE',
					 '300348.XSHE',
					 '300352.XSHE',
					 '300365.XSHE',
					 '300366.XSHE',
					 '300367.XSHE',
					 '300368.XSHE',
					 '300369.XSHE',
					 '300377.XSHE',
					 '300378.XSHE',
					 '300379.XSHE',
					 '300380.XSHE',
					 '300384.XSHE',
					 '300386.XSHE',
					 '300399.XSHE',
					 '300419.XSHE',
					 '300440.XSHE',
					 '300448.XSHE',
					 '300449.XSHE',
					 '300451.XSHE',
					 '300455.XSHE',
					 '300462.XSHE',
					 '300465.XSHE',
					 '300468.XSHE',
					 '300469.XSHE',
					 '300479.XSHE',
					 '300496.XSHE',
					 '300508.XSHE',
					 '300513.XSHE',
					 '300520.XSHE',
					 '300523.XSHE',
					 '300525.XSHE',
					 '300532.XSHE',
					 '300541.XSHE',
					 '300542.XSHE',
					 '300546.XSHE',
					 '300550.XSHE',
					 '300552.XSHE',
					 '300556.XSHE',
					 '300559.XSHE',
					 '300561.XSHE',
					 '300579.XSHE',
					 '300588.XSHE',
					 '300598.XSHE',
					 '300605.XSHE',
					 '300608.XSHE',
					 '300609.XSHE',
					 '300627.XSHE',
					 '300645.XSHE',
					 '300659.XSHE',
					 '300663.XSHE',
					 '600100.XSHG',
					 '600271.XSHG',
					 '600410.XSHG',
					 '600446.XSHG',
					 '600476.XSHG',
					 '600536.XSHG',
					 '600570.XSHG',
					 '600571.XSHG',
					 '600588.XSHG',
					 '600601.XSHG',
					 '600602.XSHG',
					 '600654.XSHG',
					 '600701.XSHG',
					 '600718.XSHG',
					 '600728.XSHG',
					 '600756.XSHG',
					 '600764.XSHG',
					 '600797.XSHG',
					 '600800.XSHG',
					 '600845.XSHG',
					 '600850.XSHG',
					 '600855.XSHG',
					 '601519.XSHG',
					 '603019.XSHG',
					 '603039.XSHG',
					 '603138.XSHG',
					 '603189.XSHG',
					 '603232.XSHG',
					 '603383.XSHG',
					 '603496.XSHG',
					 '603508.XSHG',
					 '603636.XSHG',
					 '603660.XSHG',
					 '603881.XSHG',
					 '603918.XSHG',
					 '603990.XSHG']
					 
def before_trading(context):
    context.counts +=1
    if context.counts%5 == 0:
        logger.info(len(context.stocks))
        universe = filter_listed_date_stock(context.stocks)
        logger.info(len(universe))
        universe = filter_paused_stock(universe)
        logger.info(len(universe))
        universe = get_total_turnover(universe)
        logger.info(len(universe))
        context.stk_list = get_turnover(universe)
        logger.info(len(context.stk_list))
    


def get_turnover(stk_list):
    df = get_turnover_rate(stk_list , count=1 ,fields='today').T
    df.columns = ['turnover']
    df = df.sort_values(by = 'turnover',ascending = False).dropna()
    return list(df.index[:10])
    
# 过滤停牌股票
def filter_paused_stock(stock_list):
    return [stock for stock in stock_list if not is_suspended(stock)]
    
# 过滤上市不满180天的股票
def filter_listed_date_stock(stock_list):
    return [stock for stock in stock_list if instruments(stock).days_from_listed()>180] 
    
def get_total_turnover(stk_list):
    return [stock for stock in stk_list if history_bars(stock,1,'1d','total_turnover')[0]>10000000]    



def handle_bar(context, bar_dict):
    if context.counts%5 == 0:
        for stk in context.portfolio.positions.keys():
            if stk not in context.stk_list:
                order_target_percent(stk,0)
    
        for stk in context.stk_list:
            order_target_percent(stk,0.095)


def after_trading(context):
    pass					 
					 
					 