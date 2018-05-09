import DHNAdataRead as dh
import DHNA_profiler as dp
import matplotlib.pyplot as plt
from PlotSelector import returnXrange
import numpy as np
from scipy import stats
import pandas as pd


p_time, beamdia, total_power = dp.dhnaProfiler(r"C:\Users\eric.borcherding\Desktop\DHNA\Test Data\Thursday\2_No_N2\thursday_no_n2.results.csv")
u_time_original, u_power = dh.dhnaPower(r"C:\Users\eric.borcherding\Documents\LBP2 Series\Data\New folder\addweights 3\DATA06.CSV")

u_time = np.asarray(u_time_original)


u_power_corr = 2.6*u_power - 0.013

measuredNA = 0.135
nominalBeamdia = 2.29 #mm
naCalc = (nominalBeamdia/beamdia*measuredNA)*1.1


XposD, XposU = returnXrange(p_time,total_power,u_time,u_power)
# print(XposD)
# print(XposU)
#
# def minimal_slope(p_time,total_power,u_time,u_power,zz):
#     ux_time = np.asarray(u_time) + zz
#     XposD, XposU = returnXrange(p_time,total_power,ux_time,u_power)
#     u_power_corr = 3.6799 * u_power - 0.0081
#     # m, b = np.polyfit((pd.to_numeric(u_power_corr[XposU])), (pd.to_numeric(total_power[XposD])), 1)
#     a = pd.to_numeric(u_power_corr[XposU])
#     b = (pd.to_numeric(total_power[XposD]))
#     slope, intercept, r_value, p_value, std_err = stats.linregress(a,b)
#     return r_value
#
# zz = np.array([3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8])
# for i in range(zz.size):
#     minimal_slope(p_time, total_power, u_time, u_power, zz[i])
#
#     print('offset = ', zz[i])
#     print(minimal_slope(p_time, total_power, u_time, u_power, zz[i]))


#####
#Plot of Uphole vs Downhole Power Raw signal
#####
plt.plot(p_time,total_power,'b', label='Downhole Power (mW)')
plt.plot(u_time,u_power,'r', label='Uphole Power (mW)')
plt.xlabel('Time')
plt.ylabel('Power mW')
plt.title('Overlay Uphole vs. Downhole Power Raw')
plt.legend()
plt.show(block=True)
#####
#Plot of Uphole vs Downhole Power Corrected signal
#####
plt.plot(p_time[XposD],total_power[XposD],'b', label='Downhole Power (mW)')
plt.plot(u_time[XposU],u_power_corr[XposU],'r', label='Uphole Power (mW)')
plt.xlabel('Time')
plt.ylabel('Power mW')
plt.title('Overlay Uphole vs. Downhole Power Corrected')
plt.legend()
plt.show(block=True)
#####
#Plot of Downhole Power vs. Beam Diameter
#####

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.plot(p_time,total_power, 'g-')
ax2.plot(p_time,beamdia, 'b-')


fig.suptitle('Overlay Power (mW) & Beam Diameter (mm)', fontsize=18)
ax1.set_xlabel('X data')
ax1.set_ylabel('Downhole Power (mW)', color='g')
ax2.set_ylabel('Beam Diameter (mm)', color='b')

plt.show(block = True)
#############


#####
#Correlation Plot Uphole vs Downhole Power Corrected signal
#####
x = pd.to_numeric(u_power_corr[XposU])
y = pd.to_numeric(total_power[XposD])
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
print(stats.linregress(x,y))
plt.plot(u_power_corr[XposU],total_power[XposD],'bo', label='Downhole Power (mW)')
plt.plot(x, intercept + slope*x, 'r', label='fitted line')
plt.xlabel('Uphole Power Corrected (mW')
plt.ylabel('DownHole Power (mW)')
d = { 'slope': round(slope,3), 'intercept': round(intercept,3), 'R2':round(r_value,3) }
s = "Correlation Uphole vs. Downhole Power Corrected \n {slope}x+{intercept}   R2= {R2}"
s.format(**d)
plt.title(s.format(**d))
plt.legend()
plt.show(block=True)
#####






## need to incorporate NA calculation
## normalzie epoch time so chart isn't so crazy looking

import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# Filter requirements.
order = 3
fs = 4       # sample rate, Hz
cutoff = .05 # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# # Plot the frequency response.
# w, h = freqz(b, a, worN=8000)
# plt.subplot(2, 1, 1)
# plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
# plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
# plt.axvline(cutoff, color='k')
# plt.xlim(0, 0.5*fs)
# plt.title("Lowpass Filter Frequency Response")
# plt.xlabel('Frequency [Hz]')
# plt.grid()

#
# # Demonstrate the use of the filter.
# # First make some data to be filtered.
# T = 5.0         # seconds
# n = int(T * fs) # total number of samples
# t = np.linspace(0, T, n, endpoint=False)
# # "Noisy" data.  We want to recover the 1.2 Hz signal from this.
# data = np.sin(1.2*2*np.pi*t) + 1.5*np.cos(9*2*np.pi*t) + 0.5*np.sin(12.0*2*np.pi*t)

# Filter the data, and plot both the original and filtered signals.
# y = butter_lowpass_filter(data, cutoff, fs, order)
filtbeam = butter_lowpass_filter(beamdia[XposD],cutoff,fs,order)
# filtUpower = butter_lowpass_filter(u_power_corr[XposU],cutoff,fs,order)
filtDpower = butter_lowpass_filter(total_power[XposD],cutoff,fs,order)
filtNA = butter_lowpass_filter(naCalc[XposD],cutoff,fs,order)
# plt.subplot(2, 1, 2)
# plt.plot(t, data, 'b-', label='data')
# plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
# plt.xlabel('Time [sec]')
# plt.grid()
# plt.legend()
#
# plt.subplots_adjust(hspace=0.35)
# plt.show(block = True)


filtTimeD = (np.asarray(p_time[XposD]) - np.asarray(p_time[XposD][0]))/60
filtTimeU = (np.asarray(u_time[XposU]) - np.asarray(u_time[XposU][0]))/60

plt.plot(p_time[XposD], filtbeam, 'g-', linewidth=2, label='filtered data')
# plt.plot(p_time, beamdia, 'b-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.show(block = True)

plt.plot(u_time[XposU], filtUpower, 'g-', linewidth=2, label='filtered data')
# plt.plot(p_time, beamdia, 'b-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.show(block = True)

plt.plot(p_time[XposD], filtDpower, 'g-', linewidth=2, label='filtered data')
plt.plot(u_time[XposU], filtUpower, 'r-', linewidth=2, label='filtered data')
# plt.plot(p_time, beamdia, 'b-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()
plt.show(block = True)

plt.plot(filtTimeD, filtDpower, 'b-', linewidth=2, label='Downhole Power [mW]')
plt.plot(filtTimeU, filtUpower, 'r-', linewidth=2, label='Uphole Power [mW]')
# plt.plot(p_time, beamdia, 'b-', linewidth=2, label='filtered data')
plt.xlabel('Time [min]')
plt.ylabel('Power [mW]')
plt.title('Uphole vs. Downhole Power')
plt.grid()
plt.legend()
plt.show(block = True)

#####
#Correlation Plot Uphole vs Downhole Power Corrected signal
#####
x = pd.to_numeric(filtUpower)
y = pd.to_numeric(filtDpower)
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
print(stats.linregress(x,y))
plt.plot(u_power_corr[XposU],total_power[XposD],'bo', label='Downhole Power (mW)')
plt.plot(x, intercept + slope*x, 'r', label='fitted line')
plt.xlabel('Uphole Power Corrected (mW')
plt.ylabel('DownHole Power (mW)')
d = { 'slope': round(slope,3), 'intercept': round(intercept,3), 'R2':round(r_value,3) }
s = "Correlation Uphole vs. Downhole Power Corrected \n {slope}x+{intercept}   R2= {R2}"
s.format(**d)
plt.title(s.format(**d))
plt.legend()
plt.show(block=True)
#####

#####
#Plot of Downhole Power vs. Beam Diameter
#####

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.plot(p_time[XposD],filtDpower, 'b-')
ax2.plot(p_time[XposD],filtNA-0, 'g-')


fig.suptitle('Overlay Power (mW) & Beam Diameter (mm)', fontsize=18)
ax1.set_xlabel('Epoch Time')
ax1.set_ylabel('Downhole Power (mW)', color='b')
ax2.set_ylabel('Beam Diameter (mm)', color='g')

plt.show(block = True)
#############