# -*- coding: utf-8 -*-
"""
Created on Tue May 16 16:00:45 2017

@author: Unknow
"""

import numpy as np
import seaborn as sns
import math
from matplotlib import pyplot as plt

# 设置基本参数
ttm = 3.0    # 到期时间，单位年 
tSteps = 25  # 时间方向步数
r = 0.03     # 无风险利率
d = 0.02     # 标的股息率
sigma = 0.2  # 波动率
strike = 100.0  # 期权行权价
spot = 100.0  # 标的现价

# 二叉树框架（可以通过传入不同的treeTraits类型，设计不同的二叉树结构）
class BinomialTree:
    def __init__(self,spot,riskFree,dividend,tSteps,maturity,sigma,treeTraits):
        self.dt   = maturity/tSteps
        self.spot = spot
        self.r    = riskFree
        self.d    = dividend
        self.tSteps   = tSteps
        self.discount = math.exp(-self.r*self.dt)
        self.v    = sigma
        self.up   = treeTraits.up(self)
        self.down = treeTraits.down(self)
        self.upProbability = treeTraits.upProbability(self)
        self.downProbability = 1.0 - self.upProbability
        self._build_lattice()
        
    def _build_lattice(self):
        # 完成构造二叉树的工作
        self.lattice = np.zeros((self.tSteps+1,self.tSteps+1))
        self.lattice[0][0] = self.spot
        for i in range(self.tSteps):
            for j in range(i+1):
                self.lattice[i+1][j+1] = self.up*self.lattice[i][j]
            self.lattice[i+1][0] = self.down*self.lattice[i][0]

    # 处理欧式期权
    def roll_back(self,payOff):
        for i in range(self.tSteps,0,-1):
            for j in range(i,0,-1):
                if i == self.tSteps:
                    self.lattice[i-1][j-1] = self.discount*(self.upProbability*payOff(self.lattice[i][j])+self.downProbability*payOff(self.lattice[i][j-1]))
                else:
                    self.lattice[i-1][j-1] = self.discount*(self.upProbability*self.lattice[i][j]+self.downProbability*self.lattice[i][j-1])
   
    # 处理美式期权
    def roll_back_american(self,payOff):
        for i in range(self.tSteps,0,-1):
            for j in range(i,0,-1):
                if i == self.tSteps:
                    europeanValue = self.discount*(self.upProbability*payOff(self.lattice[i][j])+self.downProbability*payOff(self.lattice[i][j-1]))
                else:
                    europeanValue = self.discount*(self.upProbability*self.lattice[i][j]+self.downProbability*self.lattice[i][j-1])
                exerciseValue = payOff(self.lattice[i-1][j-1])
                # ExerciseValue 就是立即行权的价值，EuropeanValue为对应节点的欧式价值。
                self.lattice[i-1][j-1] = max(europeanValue,exerciseValue)
                    
# JarrowRudd二叉树描述         
class JarrowRuddTraits:
    def up(tree):
        return math.exp((tree.r-tree.d-0.5*tree.v*tree.v)*tree.dt+tree.v*math.sqrt(tree.dt))
    def down(tree):
        return math.exp((tree.r-tree.d-0.5*tree.v*tree.v)*tree.dt-tree.v*math.sqrt(tree.dt))
    def upProbability(tree):
        return 0.5            

# Cox-Ross-Rubinstein二叉树描述  
class CRRTraits:
    def up(tree):
        return math.exp(tree.v*math.sqrt(tree.dt))
    def down(tree):
        return math.exp(-tree.v*math.sqrt(tree.dt))
    def upProbability(tree):
        return 0.5+0.5*(tree.r-tree.d-0.5*tree.v*tree.v)*tree.dt/(tree.v*math.sqrt(tree.dt))      

# 偿付函数               
def pay_off(spot):
    global strike
    return max(spot-strike,0.0)
    
testTree = BinomialTree(spot,r,d,tSteps,ttm,sigma,JarrowRuddTraits)
testTree.roll_back(pay_off)
print(u"二叉树价格：%.4f"%testTree.lattice[0][0])

stepSizes = range(25,500,25)
jrRes  = []
crrRes = []
for tSteps in stepSizes:
    testTree = BinomialTree(spot,r,d,tSteps,ttm,sigma,JarrowRuddTraits)
    testTree.roll_back(pay_off)
    jrRes.append(testTree.lattice[0][0])
    testTree = BinomialTree(spot,r,d,tSteps,ttm,sigma,CRRTraits)
    testTree.roll_back(pay_off)
    crrRes.append(testTree.lattice[0][0])

plt.figure(figsize = (16,8))
plt.plot(stepSizes, jrRes, '-.', marker = 'o', markersize = 10)
plt.plot(stepSizes, crrRes, '-.', marker = 'd', markersize = 10)
plt.legend(['Jarrow - Rudd', 'Cox - Ross - Rubinstein', u'解析解'],prop={'family':'SimHei','size':15})
plt.xlabel(u'二叉树步数',fontproperties='SimHei')
plt.title(u'二叉树算法欧式期权收敛性测试',fontproperties='SimHei')    
plt.grid(True)
plt.show()

stepSizes = range(25,500,25)
jrRes  = []
crrRes = []
for tSteps in stepSizes:
    testTree = BinomialTree(spot,r,d,tSteps,ttm,sigma,JarrowRuddTraits)
    testTree.roll_back_american(pay_off)
    jrRes.append(testTree.lattice[0][0])
    testTree = BinomialTree(spot,r,d,tSteps,ttm,sigma,CRRTraits)
    testTree.roll_back_american(pay_off)
    crrRes.append(testTree.lattice[0][0])

plt.figure(figsize = (16,8))
plt.plot(stepSizes, jrRes, '-.', marker = 'o', markersize = 10)
plt.plot(stepSizes, crrRes, '-.', marker = 'd', markersize = 10)
plt.legend(['Jarrow - Rudd（美式）', 'Cox - Ross - Rubinstein（美式）', u'解析解'],prop={'family':'SimHei','size':15})
plt.xlabel(u'二叉树步数',fontproperties='SimHei')
plt.title(u'二叉树算法美式期权收敛性测试',fontproperties='SimHei')    
plt.grid(True)
plt.show()