# -*- coding: utf-8 -*-
"""
Created on Tue May 16 11:28:36 2017
一个基本的二叉树机构由以下三个参数决定：
up 标的资产价格向上跳升的比例， up必然大于1 
down 标的资产价格向下跳升的比例， down必然小于1 
upProbability 标的资产价格向上跳升的概率
@author: Unknow
"""

import numpy as np
import seaborn as sns
import math
from matplotlib import pylab
# 解决图像中文不输出问题
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\font\simsun.tcc",size=14)

# 设置基本参数
ttm = 3.0    # 到期时间，单位年 
tSteps = 25  # 时间方向步数
r = 0.03     # 无风险利率
d = 0.02     # 标的股息率
sigma = 0.2  # 波动率
strike = 100.0  # 期权行权价
spot = 100.0  # 标的现价

# Jarrow - Rudd 树
# 这个树的深度为16层（时间节点数+1）
dt = ttm/tSteps
up = math.exp((r-d-0.5*sigma*sigma)*dt+sigma*math.sqrt(dt))
down = math.exp((r-d-0.5*sigma*sigma)*dt-sigma*math.sqrt(dt))
discount = math.exp(-r*dt)

lattice = np.zeros((tSteps+1,tSteps+1))
lattice[0][0] = spot
for i in range(tSteps):
    for j in range(i+1):
        lattice[i+1][j+1] = up*lattice[i][j]
    lattice[i+1][0] = down*lattice[i][0]

pylab.figure(figsize=(12,8))
pylab.plot(lattice[tSteps])
pylab.title(u"二叉树到期时刻标的价格分布",fontproperties='SimHei')

def call_payoff(spot):
    global strike
    return max(spot-strike,0.0)
"""
pylab.figure(figsize=(12,8))
pylab.plot(map(call_payoff,lattice[tSteps]))
pylab.title(u"二叉树到期时刻标的Pay off分布",fontproperties='SimHei')
"""
for i in range(tSteps,0,-1):
    for j in range(i,0,-1):
        if i == tSteps:
            lattice[i-1][j-1] = 0.5 * discount * (call_payoff(lattice[i][j]) + call_payoff(lattice[i][j-1]))
        else:
            lattice[i-1][j-1] = 0.5 * discount * (lattice[i][j] + lattice[i][j-1])
            
print( u'二叉树价格： %.4f' % lattice[0][0])