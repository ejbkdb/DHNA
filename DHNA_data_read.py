
import pandas as pd
import time
from EqualDataStep import EqualDataStep

def dhnaPower(filename):

    df = pd.read_csv(filename, delimiter = '\t', header = 3)
    header = pd.read_csv(filename, engine = 'python',  delimiter = '\t', skipfooter = df.shape[0]+2)



    #df = pd.read_csv(r"C:\Users\eric.borcherding\Desktop\Data1\DATA03.CSV", delimiter = '\t', header = 3)

    #header = pd.read_csv(r"C:\Users\eric.borcherding\Desktop\Data1\DATA03.CSV", engine = 'python',  delimiter = '\t', skipfooter = df.shape[0]+2)

    upholePower = df.range*1000 # coverts from W to mw to match profiler

    df = df.values
    ###########################################################################
    startTime = header.columns[1]

    pattern = '%Y-%m-%d %H:%M:%S'
    startEpoch = int(time.mktime(time.strptime(startTime, pattern)))

    ET = df[:,1]/1000
    epochOriginal = startEpoch + ET
    ###########################################################################
    DateTimeList = []
    for i in range(epochOriginal.size):
        DateTimeList.append(datetime.datetime.fromtimestamp(epochOriginal[i]))

    DateTimeArray = np.asarray(DateTimeList)

    upholePower1 = np.asarray(EqualDataStep(DateTimeArray, upholePower, 0.25))

    ET = upholePower1[:,0]                                                # Converts new regularized time step into epoch Time
    epochET = []
    for i in range(ET.size):
        epochET.append(ET[i].timestamp())

    # plt.plot(epochET,upholePower1[:,1],epochOriginal,upholePower)
    # plt.show(block=True)
    # plt.plot(epochOriginal,upholePower)
    # plt.show(block=True)


    return epochET,upholePower1[:,1]

    for i in range(ET.size):

dhnaPower(r"C:\Users\eric.borcherding\Documents\LBP2 Series\Data\New folder\DATA06.CSV")