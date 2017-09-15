# -*- coding: utf-8 -*-
"""
Created on Tue May 16 19:48:15 2017

@author: Unknow
"""

import numpy as np
from numpy import array
import seaborn as sns
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from matplotlib import pylab
import matplotlib.cm as cm

# Part 1
def initialCondition(x):
    return 4.0*(1.0-x)*x

xArray = np.linspace(0,1.0,50)
yArray = array(list(map(initialCondition,xArray)))
pylab.figure(figsize=(12,6))
pylab.plot(xArray,yArray)
pylab.xlabel('$x$', fontsize = 15)
pylab.ylabel('$f(x)$', fontsize = 15)
pylab.title(u'一维热传导方程初值条件', fontproperties = 'SimHei')


# Part2
N = 25   # x方向网格数
M = 2500  # t方向网格数
T = 1.0
X = 1.0
xArray = np.linspace(0,X,N+1)
yArray = array(list(map(initialCondition, xArray)))
starValues = yArray
U = np.zeros((N+1,M+1))
U[:,0] = starValues
dx = X / N
dt = T / M
kappa = 1.0
rho = kappa * dt / dx / dx
for k in range(0, M):
    for j in range(1, N):
        U[j][k+1] = rho * U[j-1][k] + (1. - 2*rho) * U[j][k] + rho * U[j+1][k]
    U[0][k+1] = 0.
    U[N][k+1] = 0.
pylab.figure(figsize = (12,6))
pylab.plot(xArray, U[:,0])
pylab.plot(xArray, U[:, int(0.10/ dt)])
pylab.plot(xArray, U[:, int(0.20/ dt)])
pylab.plot(xArray, U[:, int(0.50/ dt)])
pylab.xlabel('$x$', fontsize = 15)
pylab.ylabel(r'$U(\dot, \tau)$', fontsize = 15)
pylab.title(u'一维热传导方程', fontproperties = 'SimHei')
pylab.legend([r'$\tau = 0.$', r'$\tau = 0.10$', r'$\tau = 0.20$', r'$\tau = 0.50$'],fontsize = 15)



# Part 3
"""
N 空间方向的网格数
M 时间方向的网格数
T 最大时间期限
X 最大空间范围
U 用来存储差分网格点上值的矩阵
"""
class HeatEquation:
    def __init__(self,kappa,X,T,initialConstion=lambda x:4.0*x*(1.0-x),boundaryConditionL=lambda x:0,
                 boundaryConditionR=lambda x:0):
        self.kappa = kappa
        self.ic    = initialConstion
        self.bcl   = boundaryConditionL  
        self.bcr   = boundaryConditionR 
        self.X     = X
        self.T     = T
  
class ExplicitEulerScheme:
    def __init__(self,M,N,equation):
        self.eq  = equation
        self.dt  = self.eq.T/M
        self.dx  = self.eq.X/N
        self.U   = np.zeros((N+1,M+1))
        self.xArray = np.linspace(0,self.eq.X,N+1)
        self.U[:,0] = array(list(map(self.eq.ic,self.xArray)))
        self.rho = self.eq.kappa*self.dt/self.dx/self.dx
        self.M   = M
        self.N   = N
        
    def roll_back(self):
        for k in range(0,self.M):
            for j in range(0,self.N):
                self.U[j][k+1] = self.rho*self.U[j-1][k]+(1.-2*self.rho)*self.U[j][k]+self.rho*self.U[j+1][k]
        self.U[0][k+1] = self.eq.bcl(self.xArray[0])
        self.U[self.N][k+1] = self.eq.bcr(self.xArray[-1])
        
    def mesh_grids(self):
        tArray = np.linspace(0,self.eq.T,self.M+1)
        tGrids,xGrids = np.meshgrid(tArray,self.xArray)
        return tGrids,xGrids
        
ht = HeatEquation(1.,1.,1.)
scheme = ExplicitEulerScheme(2500,25,ht)
scheme.roll_back()
tGrids, xGrids = scheme.mesh_grids()
fig= plt.figure(figsize = (16,10))
ax = fig.add_subplot(1, 1, 1, projection='3d')
cutoff = int(0.2 / scheme.dt) + 1
surface = ax.plot_surface(xGrids[:,:cutoff], tGrids[:,:cutoff], scheme.U[:,:cutoff], cmap=cm.coolwarm)
ax.set_xlabel("$x$", fontdict={"size":18})
ax.set_ylabel(r"$\tau$", fontdict={"size":18})
ax.set_zlabel(r"$U$", fontdict={"size":18})
ax.set_title(u"热传导方程 $u_\\tau = u_{xx}$",fontproperties='SimHei')
fig.colorbar(surface,shrink=0.75)