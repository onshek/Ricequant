import talib
import numpy as np  
from sklearn import linear_model

def init(context):
    # 策略初始化运行
    logger.info('init')
    context.s1 = 'J88'
    # 分别拆分为 1、2、4、8、16、32 组
    context.list_num = [1, 2, 4, 8, 16]
    context.list_Hurst = []
    context.close = np.array([])
    context.Hurst_ema_3 = float()
    context.Hurst_ema_20 = float()
    context.Close_ema_3 = float()
    context.Close_ema_20 = float()
    context.buy = .0
    context.sell = .0
    subscribe(context.s1)
    scheduler.run_daily(handle_bar_daily)
    
def before_trading(context):
    # 每日开盘前运行
    pass

def calculate(context, bar_dict):
    # 取最近 81 个交易日的 J88 收盘点位
    close = history_bars(context.s1, 81, '1d', 'close')
    Close = close[-1]
    context.close = close
    # 计算最近 80 个交易日的收益率
    return_close = []
    for i in range(0, 80):
        r_close = 100 * ((close[i + 1] / close[i]) - 1)
        return_close.append(r_close)
    
    # 创建一个空 list 用于存放 ars_data
    list_ars_data = []
 
    # 对每一个对应的 list_num，都计算以下流程
    for obj_list_num in context.list_num:
        # 设置一个空 list 用于存储最后的 rs_data
        list_rs_data = []
        # 将 80 个交易日指数收盘点位按组数分割
        for i in range(0, obj_list_num):            
            # 每组对应的长度
            list_size = int(80 / obj_list_num)
            # 每组起始
            start = list_size * i
            # 每组结束
            end = list_size * (i + 1)
            # 取出片段
            data = return_close[start: end]
            #print('data: ', data)
            
            # 计算每个片段的均值(mean)
            mean_data = np.mean(data)
            #print('mean_data: ', mean_data)
            
            # 针对每个片段计算离差序列(deviation)
            dev_data = data - mean_data
            #print('dev_data: ', dev_data)
            
            # 计算离差序列的 cumsum
            cumsum_dev_data = dev_data.cumsum()
            #print('cumsum_dev_data: ', cumsum_dev_data)
            
            # 计算每个离差序列的 cumsum 的最大差距(widest difference)
            diff_data = max(cumsum_dev_data) - min(cumsum_dev_data)
            #print('diff_data: ', diff_data)
            
            # 计算每个片段的标准差(standard deviation)
            std_data = np.std(data)
            #print('std_data: ', std_data)
            
            # 计算每个片段的 R/S 值
            rs_data = np.array(diff_data) / std_data
            #print('rs_data: ', rs_data)
            
            # 将 R/S 值加入 list_rs_data 用于保存
            list_rs_data.append(rs_data)
            #print(list_rs_data)

        #print(len(list_rs_data))  
        #print(list_rs_data)
        
        # 将各个片段的 R/S 值求平均得到 Average R/S(ARS)
        ars_data = np.mean(list_rs_data)
        #print('ars_data: ', ars_data)
        
        # 将 ars_data 加入 list_ars_data
        list_ars_data.append(ars_data)
    
    #print(list_ars_data)
    
    # ARS 对 10 取对数
    lg_list_ars_data = np.log10(list_ars_data)
    #print('lg_list_ars_data: ', lg_list_ars_data)

    # 对片段大小（size）对 10 取对数
    lg_list_size = np.log10([80, 40, 20, 10, 5]) 
    lg_list_size = [[i] for i in lg_list_size]
    #print('lg_list_size: ', lg_list_size)
    
    # lg_list_ars_data 对 lg_list_num 回归，斜率是 Hurst 指数
    regr = linear_model.LinearRegression()
    regr.fit(lg_list_size, lg_list_ars_data)
    #HURST指数
    Hurst = regr.coef_  
    #print('H:', Hurst)
    return Hurst, Close
      
    
def handle_bar_daily(context, bar_dict):
    # 每个 bar 数据运行
    
    buy_qty=context.future_account.positions[context.s1].buy_quantity
    sell_qty=context.future_account.positions[context.s1].sell_quantity
    
    Hurst, Close = calculate(context, bar_dict)
    context.list_Hurst.append(float(Hurst))
    #print('list_Hurst: ', len(context.list_Hurst))
    if len(context.list_Hurst) >= 20:
        context.Hurst_ema_3 = talib.SMA(np.array(context.list_Hurst), 3)[-1]  
        context.Hurst_ema_20 = talib.SMA(np.array(context.list_Hurst), 20)[-1]  
        context.Close_ema_3 = talib.SMA(context.close, 3)[-1]  
        context.Close_ema_20 = talib.SMA(context.close, 20)[-1] 

        #plot('Hurst_ema_3', Hurst_ema_3)
        #plot('Hurst_ema_20', Hurst_ema_20)
        #plot('close_ema_3', close_ema_3)
        #plot('close_ema_20', close_ema_20)
        
    if (context.Hurst_ema_3 > context.Hurst_ema_20) and (context.Hurst_ema_3 > 0.5):
        #与市场趋势一致
        if context.Close_ema_3 > context.Close_ema_20:
            if sell_qty > 0:
                buy_close(context.s1,1)
            if buy_qty == 0:
                buy_open(context.s1,1)
                context.buy = context.future_account.positions[context.s1].buy_avg_holding_price
        if (context.Close_ema_3 < context.Close_ema_20):
            if (buy_qty > 0) and (Close < context.buy * 0.97):
                sell_close(context.s1,1)            
            if sell_qty == 0:
                sell_open(context.s1,1)  
                context.sell = context.future_account.positions[context.s1].sell_avg_holding_price
    elif (context.Hurst_ema_3 < context.Hurst_ema_20) and (context.Hurst_ema_3 < 0.5):
        #与市场趋势相反
        if context.Close_ema_3 > context.Close_ema_20:
            if buy_qty > 0:
                sell_close(context.s1,1)            
            if sell_qty == 0:
                sell_open(context.s1,1)
                context.sell = context.future_account.positions[context.s1].sell_avg_holding_price
        if (context.Close_ema_3 < context.Close_ema_20):
            if (sell_qty > 0) and (Close > context.sell * 1.03):
                buy_close(context.s1,1)
            if buy_qty == 0:
                buy_open(context.s1,1)
                context.buy = context.future_account.positions[context.s1].buy_avg_holding_price
 
def after_trading(context):
    # 每日收盘后运行
    pass