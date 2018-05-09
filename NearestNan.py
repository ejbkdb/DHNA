import numpy as np
# a = pd.to_numeric(beamDia, errors = 'coerce')

def NearestNan(data):
    ind = np.where(np.isnan(data))[0]
    for i in range(ind.size):
        print("i=",  i)
        x = 0
        while np.isnan(data[ind[i]-x]) == True:
            x += 1
            print('x=', x)
            print(data[ind[i]-x])

            if np.isnan(data[ind[i]-x]) == False:
                data[ind[i]] = data[ind[i]-x]
                print('this X worked', x)
                break


    return data



