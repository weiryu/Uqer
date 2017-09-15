# -*- coding: utf-8 -*-
"""
Created on Fri May 12 10:39:32 2017

@author: Unknow
我们想知道下面的一只期权的价格：
当前价 spot : 2.45
行权价 strike : 2.50
到期期限 maturity : 0.25
无风险利率 r : 0.05
波动率 vol : 0.25
根据Black - Scholes期权定价公式：
C=S·N(d1)-X·exp(-r·T)·N(d2)
其中:
d1=[ln(S/X)+(r+0.5σ^2)T]/(σ√T)
d2=d1-σ·√T
C—期权初始合理价格
X—期权执行价格
S—所交易金融资产现价
T—期权有效期
r—连续复利计无风险利率
σ—股票连续复利（对数）回报率的年度波动率（标准差）
N(d1)，N(d2）—正态分布变量的累积概率分布函数

使用Numpy将大大加速
"""

from math import log,sqrt,exp
from scipy.stats import norm
from matplotlib import pylab
# 控制刻度标签显示的Formatter 类
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import numpy as np
import time
# 解决图像中文不输出问题
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\font\simsun.tcc",size=14)

#参数
spot = 2.45
strike = 2.50
maturity = 0.25
r = 0.05
vol = 0.25
portfolioSize = range(1, 10000, 500)
timeSpent = []
timeSpentNumpy = []

# 使用math函数计算Black - Scholes期权定价公式函数
def call_option_pricer(spot,strike,maturity,r,vol):
    d1 = (log(spot/strike)+(r+0.5*vol*vol)*maturity)/(vol*sqrt(maturity))
    d2 = d1-(vol*sqrt(maturity))
    price = spot*norm.cdf(d1)-strike*(exp(-r*maturity)*norm.cdf(d2))
    return price 
# print('期权价格 : %.4f' % call_option_pricer(spot, strike, maturity, r, vol))

# 统计不同计算量的耗时
for size in portfolioSize:
    now = time.time()
    # numpy.linspace(start, stop, num=size, endpoint=True, retstep=False, dtype=None)
    strikes = np.linspace(2.0,3.0,size)
    # print(strikes)
    for i in range(size):
        res = call_option_pricer(spot,strikes[i],maturity,r,vol)
    timeSpent.append(time.time()-now)
  
# 输出计算量-时间图像
sns.set(style='ticks')
pylab.mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
pylab.mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
pylab.figure(figsize=(12,8))
pylab.bar(portfolioSize,timeSpent,color='r',width=300)
pylab.grid(True)
pylab.title(u"期权计算时间耗时（单位：秒）")
pylab.ylabel("time(second)")
pylab.xlabel(u"组合数量")

# 使用numpy函数计算Black - Scholes期权定价公式函数
def call_option_pricer_numpy(spot,strike,maturity,r,vol):
    d1 = (np.log(spot/strike)+(r+0.5*vol*vol)*maturity)/(vol*np.sqrt(maturity))
    d2 = d1-(vol*np.sqrt(maturity))
    price = spot*norm.cdf(d1)-strike*np.exp(-r*maturity)*norm.cdf(d2)
    return price 
    
# 统计不同计算量的耗时
for size in portfolioSize:
    now = time.time()
    # numpy.linspace(start, stop, num=size, endpoint=True, retstep=False, dtype=None)
    strikes = np.linspace(2.0,3.0,size)
    # print(strikes)
    res = call_option_pricer_numpy(spot,strikes,maturity,r,vol)
    timeSpentNumpy.append(time.time()-now)

print(timeSpentNumpy)
# 输出计算量-时间图像
sns.set(style='ticks')
pylab.mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
pylab.mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
pylab.figure(figsize=(12,8))
pylab.bar(portfolioSize,timeSpentNumpy,color='r',width=300)
pylab.grid(True)
pylab.title(u"期权计算时间耗时（单位：秒）-Numpy加速版")
pylab.ylabel("time(second)")
pylab.xlabel(u"组合数量")

# 两种计算方式的时间比较
fig = pylab.figure(figsize=(12,8))
pylab.mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
pylab.mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
ax  = fig.gca()
pylab.plot(portfolioSize,np.log10(timeSpent),portfolioSize,np.log(timeSpentNumpy))
pylab.grid(True)
def millions(x, pos):
    'The two args are the value and tick position'
    return '$10^{%.0f}$' % (x)
#  FuncFormatter可以以指定值的整数倍为刻度放置主、副刻度线。
formatter = FuncFormatter(millions)
ax.yaxis.set_major_formatter(formatter)
pylab.title(u"期权计算时间耗时（单位：秒）对比图")
pylab.legend([u"simple-calculate",u"numpy-calculate"],loc='upper center',ncol=2)
pylab.ylabel("time(second)")
