'''
本篇可直接在 rq 的 notebook 运行，无需回测
取最近 80 个交易日的 沪深主力连续收盘点位收益率  
分别分为 [1, 2, 4, 8, 16] 组
单独画图
'''

close_data = get_price('IF88', frequency='1d', start_date='2016-01-01', end_date='2017-06-30')['close']
print('len(close_data): ', len(close_data))

revenue_close_data = 100 * close_data.pct_change().dropna()
print('len(revenue_close_data): ', len(revenue_close_data))

Hurst = [] 
def test_calculate_hurst():
    # 存放所有 H 值
    global Hurst    
    
    # 计算最近 80 个交易日的收益率
    return_close = piece_revenue_close_data
    
    # 创建一个空 list 用于存放 ars_data
    list_ars_data = []
 
    # 对每一个对应的 list_num，都计算以下流程
    for obj_list_num in list_num:
        #print('obj_list_num: ', obj_list_num)
        # 设置一个空 list 用于存储最后的 rs_data
        list_rs_data = []
        # 将 80 个交易日指数收盘点位按组数分割
        for i in range(0, obj_list_num):            
            # 每组对应的长度
            list_size = int(80 / obj_list_num)
            # 每组起始
            start = -(list_size * (i + 1))  -1
            # 每组结束
            end = -(list_size * i) - 1
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
    beta = regr.coef_ 
    Hurst.append(float(beta))
    return beta, Hurst

def finish_hurst():
    global piece_revenue_close_data
    global list_num 
    
    list_num = [1, 2, 4, 8, 16]
    for i in range(0, len(revenue_close_data) - 80):
        start_num = i 
        end_num = (i + 1) + 80
        piece_revenue_close_data =  revenue_close_data[start_num: end_num]
        
        #print('start: ', i)
        test_calculate_hurst()


import numpy as np  
from sklearn import linear_model
finish_hurst()



import matplotlib.pyplot as plt
import talib

Hurst_ema_3 = talib.EMA(np.array(Hurst), 3)
Hurst_ema_20 = talib.EMA(np.array(Hurst), 20)
Revenue_close_data_ema_3 = talib.EMA(revenue_close_data[80:].values, 3) 
Revenue_close_data_ema_20 = talib.EMA(revenue_close_data[80:].values, 20)    
Close_data_ema_3 = talib.EMA(close_data[81:].values, 3) 
Close_data_ema_20 = talib.EMA(close_data[81:].values, 20)   
    
fig = plt.figure(figsize=(22, 8))
ax1 = fig.add_subplot(2, 2, 3)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 1)
plt.subplots_adjust(hspace=0.5)
                         
ax1.plot(Hurst_ema_3, label='Hurst_ema_3', alpha=0.9)
ax1.plot(Hurst_ema_20, label='Hurst_ema_20', alpha=0.9)
ax1.set_title('Hurst Exponent')
ax1.set_xlabel('trading date, starting from 2016-05-06')
ax1.set_ylabel('value')
ax1.legend(loc='best')

ax2.plot(Revenue_close_data_ema_3, label='Revenue_close_data_ema_3', alpha=0.9)
ax2.plot(Revenue_close_data_ema_20, label='Revenue_close_data_ema_20', alpha=0.9)
ax2.set_title('Revenue')
ax2.set_xlabel('trading date, starting from 2016-05-06')
ax2.set_ylabel('value(%)')
ax2.legend(loc='best')

ax3.plot(Close_data_ema_3, label='Close_data_ema_3', alpha=0.9)
ax3.plot(Close_data_ema_20, label='Close_data_ema_20', alpha=0.9)
ax3.set_title('Close')
ax3.set_xlabel('trading date, starting from 2016-05-06')
ax3.set_ylabel('value')
ax3.legend(loc='best')

plt.grid(True)
plt.show()
