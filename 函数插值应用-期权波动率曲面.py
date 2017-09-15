# -*- coding: utf-8 -*-
"""
Created on Tue May 16 09:50:25 2017

@author: Unknow
"""

import pandas as pd
import pylab
import numpy as np
from datetime import date
from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

pd.options.display.float_format = '{:,>.2f}'.format
dates = [date(2015,3,25), date(2015,4,25), date(2015,6,25), date(2015,9,25)]
# 行权价
strikes = [2.2, 2.3, 2.4, 2.5, 2.6]
# 波动率矩阵（Volatilitie Matrix)
blackVolMatrix = np.array([[ 0.32562851,  0.29746885,  0.29260648,  0.27679993],
                  [ 0.28841840,  0.29196629,  0.27385023,  0.26511898],
                  [ 0.27659511,  0.27350773,  0.25887604,  0.25283775],
                  [ 0.26969754,  0.25565971,  0.25803327,  0.25407669],
                  [ 0.27773032,  0.24823248,  0.27340796,  0.24814975]])
table = pd.DataFrame(blackVolMatrix * 100, index = strikes, columns = dates, )
table.index.name = u'行权价'
table.columns.name = u'到期时间'
print(u'2015年3月3日10时波动率矩阵')
print(table)

evaluationDate = date(2015,3,3)
ttm = np.array([(d-evaluationDate).days/365.0 for d in dates])
# 方差矩阵，列对应时间维度，行对应行权价维度
varianceMatrix = (blackVolMatrix**2)*ttm
print(varianceMatrix)

interp = interpolate.interp2d(ttm,strikes,varianceMatrix,kind='linear')

sMeshes = np.linspace(strikes[0],strikes[-1],400)
tMeshes = np.linspace(ttm[0],ttm[-1],200)
interpolatedVarianceSurface = np.zeros((len(sMeshes),len(tMeshes)))
for i,s in enumerate(sMeshes):
    for j,t in enumerate(tMeshes):
        interpolatedVarianceSurface[i][j] = interp(t,s)
        
interpolatedVolatilitySurface = np.sqrt(interpolatedVarianceSurface/tMeshes)
print(u"行权价方向网格数：",np.size(interpolatedVolatilitySurface,0))
print(u"到期时间方向网格数:",np.size(interpolatedVolatilitySurface,1))

maturityMesher,strikeMesher = np.meshgrid(tMeshes,sMeshes)
pylab.figure(figsize=(16,9))
ax = pylab.gca(projection='3d')
surface = ax.plot_surface(strikeMesher,maturityMesher,interpolatedVolatilitySurface*100,cmap=cm.jet)
pylab.colorbar(surface,shrink=0.75)
pylab.title(u"2015年3月3日10时波动率曲面",fontproperties='SimHei')
pylab.xlabel("strike")
pylab.ylabel("maturity")
ax.set_zlabel(r"volatility(%)")


