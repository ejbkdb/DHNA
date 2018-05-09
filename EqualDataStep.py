import traces

def EqualDataStep(DateTimeArray,DataArray, SamplePeriod):

    combinedArray = []

    for i in range(DateTimeArray.size):
        combinedArray.append([DateTimeArray[i], DataArray[i]])  # combinePower is a list that contains both DateTime time step data, and Power data. Required to cretae even time step data


    ts = traces.TimeSeries(data=combinedArray)                           # oonverts combinePower to TimeSeries using traces module
    Regularized = ts.moving_average(                               # Makes new dataset, sampling period is defined in seconds
        start=DateTimeArray[0],
        sampling_period=SamplePeriod,
        placement='left',
    )

    return Regularized


