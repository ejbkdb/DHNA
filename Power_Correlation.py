import DHNAdataRead as dh
import DHNA_profiler as dp
import matplotlib.pyplot as plt
from PlotSelector import returnXrange
import numpy as np
from scipy import stats
import pandas as pd


uh_time, uh_power = dh.dhnaPower(r"C:\Users\eric.borcherding\Desktop\DHNA\Test Data\Tuesday\4_PMD_Power_Cal_loss\DATA05_UH.CSV")

dh_time, dh_power = dh.dhnaPower(r"C:\Users\eric.borcherding\Desktop\DHNA\Test Data\Tuesday\4_PMD_Power_Cal_loss\DATA05_DH.CSV")

uh_time = np.asarray(uh_time)+.4

XposD, XposU = returnXrange(dh_time,dh_power,uh_time,uh_power)

x = pd.to_numeric(uh_power[XposU])
y = pd.to_numeric(dh_power[XposD])*1.14
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
print(stats.linregress(x,y))
plt.plot(x,y,'bo', label='Downhole Power (mW)')
plt.plot(x, intercept + slope*x, 'r', label='fitted line')
plt.xlabel('Uphole Power Corrected (mW')
plt.ylabel('DownHole Power (mW)')
d = { 'slope': round(slope,3), 'intercept': round(intercept,3), 'R2':round(r_value,3) }
s = "Correlation Uphole vs. Downhole Power Corrected \n {slope}x+{intercept}   R2= {R2}"
s.format(**d)
plt.title(s.format(**d))
plt.legend()
plt.show(block=True)