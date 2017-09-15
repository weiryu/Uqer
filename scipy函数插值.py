# -*- coding: utf-8 -*-
"""
Created on Fri May 12 19:15:13 2017

@author: Unknow
"""

from scipy import interpolate
import numpy as np
from matplotlib import pylab
import seaborn as sns
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\font\simsun.tcc",size=14)

x = np.linspace(1.0,13.0,7)
y = np.sin(x)

pylab.figure(figsize=(12,6))
pylab.scatter(x,y,s=85,marker='x',color='r')
pylab.title(u"$f(x)$离散点分布")
pylab.grid(True)

xnew = np.linspace(1.0,13.0,500)
# 线性插值 order=1
ynewLinear = interpolate.spline(x,y,xnew,order=1)
print(ynewLinear)
# 样条插值 order=3
ynewCubicSpline = interpolate.spline(x,y,xnew,order=3)
print(ynewCubicSpline)
# 真实值
ynewReal = np.sin(xnew)

pylab.figure(figsize = (16,8))
pylab.plot(xnew,ynewReal)
pylab.plot(xnew,ynewLinear)
pylab.plot(xnew,ynewCubicSpline)
pylab.scatter(x,y, s = 160, marker='x', color = 'k')
pylab.legend([u'真实曲线', u'线性插值', u'样条插值', u'$f(x)$离散点'],prop={'family':'SimHei','size':15})
pylab.title(u'$f(x)$不同插值方法拟合效果：线性插值 v.s 样条插值',fontproperties='SimHei')
