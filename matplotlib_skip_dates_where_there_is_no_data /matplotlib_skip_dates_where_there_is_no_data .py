import math
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
df = get_price('000016.XSHE', start_date='2017-07-10', end_date='2017-07-20', frequency='10m')['close']
x = math.floor(len(df.index) / 5)
ax.set_xticklabels(df.index[::x], rotation=30)
ax.plot(df.values, alpha=0.9)