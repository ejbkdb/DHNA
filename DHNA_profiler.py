import pandas as pd
import dateutil.parser
import numpy as np
import matplotlib.pyplot as plt
from EqualDataStep import EqualDataStep
from NearestNan import NearestNan


import time

def dhnaProfiler(filename):
    df = pd.read_csv(filename, header = 0, skipfooter = 10, delimiter = ',', encoding='utf_8_sig', engine = 'python')
    #df = pd.read_csv(r"C:\Users\eric.borcherding\Documents\LBP2 Series\Data\20180409_power_sweep\20180409_power_sweep_results.csv", header = 0, skipfooter = 5, delimiter = ',', encoding='utf_8_sig', engine= 'python')


    DateTime = []
    ET_original = []
    df['DateTime'] = df.Date + ' ' + df.Time # creates DateTime dataframe by merging df.Date and df.Time into a new dataframe column
    for i in range(df.DateTime.size):
        DateTime.append(dateutil.parser.parse(df.DateTime[i])) #perform date manipulation operation on df.DateTime and puts the values into a list
        ET_original.append(DateTime[i].timestamp()) # store elapsed time ET in epoch form before converting to an even time step

    beamDia = df['D%t mm'] # variable for beam diameter pulled from dataframe df
    beamDia = pd.to_numeric(beamDia, errors = 'coerce')
    beamDia = NearestNan(beamDia)
    Power = df['Total Power mW']    # variable for power pulled from dataframe df
    #pattern = '%m/%d/%Y %H:%M:%S.%f'   # DateTime format, not currently used

    DateTimeArray = np.asarray(DateTime)    #Converts DateTime from a list to an Array, will be used in step below to reorder multiple variables into a list. Required to create even time step data
    powerArray = np.asarray(Power)          #Converts Power from a list to an Array, will be used in step below to reorder multiple variables into a list. Required to create even time step data
    beamDiaArray = np.asarray(beamDia)      #Converts beamDia from a list to an Array, will be used in step below to reorder multiple variables into a list. Required to create even time step data

    power_array = np.asarray(EqualDataStep(DateTimeArray,powerArray,0.25))  # creates dataset with equal time array. Specify Date, Y-Data you want to modify, time step for new array
    beam_array = np.asarray(EqualDataStep(DateTimeArray, beamDiaArray,0.25))


    ET = beam_array[:,0]                                                # Converts new regularized time step into epoch Time
    epochET = []
    for i in range(ET.size):
        epochET.append(ET[i].timestamp())

    # plt.plot(ET_original,Power, label='Uneven Time Series')
    # plt.plot(epochET, power_array[:,1],label='Even Time Series')
    # plt.xlabel('Time')
    # plt.ylabel('Power mW')
    # plt.title('Downhole Power: Overlay Uneven vs. Even Time Series')
    # plt.legend()
    # plt.show(block=True)
    #
    # plt.plot(ET_original,beamDia,label='Uneven Time Series')
    # plt.plot(epochET, beam_array[:,1],label='Even Time Series' )
    # plt.xlabel('Time')
    # plt.ylabel('Beam Diameter (mm)')
    # plt.title('Downhole Beam Dia: Overlay Uneven vs. Even Time Series')
    # plt.legend()
    # plt.show(block=True)
    # plt.show(block = True)


    return (epochET,beam_array[:,1],power_array[:,1])


a = dhnaProfiler(r"C:\Users\eric.borcherding\Documents\LBP2 Series\Data\20180409_power_sweep\20180409_power_sweep_results.csv")