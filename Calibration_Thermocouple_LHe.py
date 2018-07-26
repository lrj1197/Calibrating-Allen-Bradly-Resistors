#data AB_18
###########
#Mixture: True Temperature, Measured Resistance
#LN2: 77.36 K, 165.67
#Freezing pt of Methanol: 175.55 K, 138.25
#LHe: 4.5 K, ?
#Freezing pt of CO2: 194.7 K, 137.6
#Freezing pt of Acetone: 178.15 K, 139.8
#Resistance of wires at room temp: 133.35 Ohms
################################################
from matplotlib import pyplot as plt
from scipy import optimize
import numpy as np
from decimal import Decimal
from datetime import datetime as d
from sklearn.metrics import r2_score
import time

def func(r,a,b,c): #define the general function
    return a + b*np.exp(c*(1000/r))

def opt(xdata, ydata, coef_guess, func, Resistor_num, r_min, r_max):
    ydata_1 = np.array(ydata) # Temperature in kelvin, matching the corresponding index in xdata
    xdata_1= np.array(xdata)  #resistance in Ohms
    (a,b,c) = coef_guess #initial guess
    #optimize:
    pop, pcov = optimize.curve_fit(func, xdata_1, ydata_1)
    #show fit
    (a,b,c) = pop
    #get the r^2 value
    print('a =',a,'b =',b,'c =',c)
    temp_pred_1 = func(xdata_1, a, b, c)
    r2 = r2_score(ydata_1, temp_pred_1)
    print('The r^2 value for this model is:', r2)
    x = np.linspace(r_min,r_max,1000) #space of temp range.
    f = func(x,a,b,c) #run the function over all space to get a smooth curve.
    plt.figure()
    plt.scatter(xdata_1, ydata_1, s=10, c='r') #plot data
    plt.plot(x, f) #plot smooth curve
    plt.xlabel('Resitance in Ohms')
    plt.ylabel('Temp in K')
    plt.title('Calibration Curve for Resistor {:s}'.format(Resistor_num))
    plt.text(800, 290, 'a: ' + str(a))
    plt.text(800, 260, 'b: ' + str(b))
    plt.text(800, 230, 'c: ' + str(c))
    plt.text(800, 320, 'r^2: ' + str(r2))
    plt.savefig('Calibration Curve for Resistor {:s}'.format(Resistor_num))
    plt.show()


#sample data
ydata = [77.36, 175.55, 4.5, 194.7, 178.15]
xdata = [165.67, 138.84, 1275 , 137.60, 139.8]
coef_guess = (0,0,0)
f = func
Resistor_num = 'AB_18_LHe_Thermometry'
r_min = 120
r_max = 1300

opt(xdata,ydata,coef_guess, f, Resistor_num, r_min, r_max)
