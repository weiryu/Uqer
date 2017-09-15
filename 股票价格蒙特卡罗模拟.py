# -*- coding: utf-8 -*-
"""
Created on Fri May 12 17:24:26 2017

@author: Unknow
"""

import scipy
from matplotlib import pylab 
import numpy as np 
from matplotlib import pyplot as plt


pylab.figure(figsize=(12,8))
# 获得标准正态分布的随机数
randomSeries = scipy.random.randn(1000)
pylab.plot(randomSeries)
print("均值：%.4f"%randomSeries.mean())
print("标准差：%.4f"%randomSeries.std())

#参数
spot = 2.45
strike = 2.50
maturity = 0.25
r = 0.05
vol = 0.25
portfolioSize = range(1, 10000, 500)

def call_option_pricer_monte_carlo(spot,strike,maturity,r,vol,num=5000):
    randomSeries = scipy.random.randn(num)
    s_t = spot*np.exp((r-0.5*vol*vol)*maturity+randomSeries*vol*np.sqrt(maturity))
    sumValue = np.maximum(s_t-strike,0.0).sum()
    price = np.exp(-r*maturity)*sumValue/num
    return price
print('期权价格（蒙特卡洛）: %.4f' % call_option_pricer_monte_carlo(spot, strike,maturity,r,vol))   
    
# 实验从1000次模拟到50000次模拟的结果，每次同样次数的模拟运行100遍。
pathScenario = range(1000,50000,1000)
numOfTrials = 100
confidenceIntervalUpper = []
confidenceIntervalLower = []
means = []
for scenario in pathScenario:
    res = np.zeros(numOfTrials)
    for i in range(numOfTrials):
        res[i] = call_option_pricer_monte_carlo(spot,strike,maturity,r,vol,num=scenario)
    means.append(res.mean())
    confidenceIntervalUpper.append(res.mean()+1.96*res.std())
    confidenceIntervalLower.append(res.mean()-1.96*res.std())

plt.figure(figsize=(12,8))
table = np.array([means,confidenceIntervalUpper,confidenceIntervalLower]).T
plt.plot(pathScenario,table)
plt.title(u'期权计算蒙特卡洛模拟',fontproperties='SimHei')
# prop参数解决标签输出中文问题
plt.legend([u'均值', u'95%置信区间上界', u'95%置信区间下界'],loc='upper center',ncol=1,prop={'family':'SimHei','size':15})
plt.ylabel('价格',fontproperties='SimHei')
plt.xlabel('模拟次数',fontproperties='SimHei')
plt.grid(True)
plt.show()
