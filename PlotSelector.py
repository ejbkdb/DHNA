import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
from FindNearest import find_nearest

def returnXrange(DownholeTime, DownholeData, UpholeTime, UpholeData):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(211)



    x = DownholeTime
    x2 = UpholeTime
    y = DownholeData
    y2 =UpholeData

    ax.plot(x, y, x2, y2,  '-')
    #ax.set_ylim(-2, 2)
    ax.set_title('Press left mouse button and drag to test')

    ax2 = fig.add_subplot(212)
    ax2.plot(x, y, x2, y2, '-')


    def onselect(xmin, xmax):
        indmin, indmax = np.searchsorted(x, (xmin, xmax))
        indmax = min(len(x) - 1, indmax)
        global thisx
        thisx = x[indmin:indmax]
        thisy = y[indmin:indmax]
        #line2.set_data(thisx, thisy)
        ax2.set_xlim(thisx[0], thisx[-1])
        #ax2.set_ylim(thisy.min(), thisy.max())
        fig.canvas.draw_idle()
        # save
        np.savetxt("text.out", np.c_[thisx, thisy])


    # set useblit True on gtkagg for enhanced performance
    span = SpanSelector(ax, onselect, 'horizontal', useblit=True,
                        rectprops=dict(alpha=0.5, facecolor='red'))

    plt.show(block = True)

    XposD = slice(x.index(thisx[0]),x.index(thisx[-1]))
    XposU = slice(find_nearest(np.asarray(x2),thisx[0]),find_nearest(np.asarray(x2),thisx[-1]))

    return XposD, XposU
