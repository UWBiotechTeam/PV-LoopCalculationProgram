import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import json
import numpy as np
from IPython.display import display, HTML
import tabulate

# Output a graph based on values
# pre: numpy arrays that represent x and y data points
# post: plots the data

# Allows graphing PV and FV
# PV-plot -> graph(volume, pressure)
# FV-plot -> graph(volume, flow)
def graph(xValues, yValues, xLabel, yLabel):
    plt.grid(True, which='both')

    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

    plt.margins(0.005)
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')

    xpoints = np.array(xValues)
    ypoints = np.array(yValues)

    plt.plot(xpoints, ypoints)

def createTable(jsonFile):
    result = loadJson(jsonFile)
    time = result[0]
    pressure = result[1]
    volume = result[2]
    flow = result[3]

    dict = {'Time': time,
            'Flow': flow,
            'Volume': volume,
            'Pressure': pressure}

    df = pd.DataFrame(dict)
    df.to_csv('DataTable', sep='\t')
def compliance(pressure, volume):
    deltaV = volume[len(volume) - 1] - volume[0]
    deltaP = pressure[len(pressure) - 1] - pressure[0]
    compliance = deltaV / deltaP
    return compliance

def peakInspirationPressure(pressure):
    maxValue = 0
    for x in range(len(pressure)):
        if pressure[x] > maxValue:
            maxValue = pressure[x]
    return maxValue

def positiveEndExpiratory(pressure):
    minValue = 999999999
    for x in range(len(pressure)):
        if pressure[x] < minValue:
            minValue = pressure[x]
    return minValue
# Residual volume is for Flow V Volume
# pre: a NumPy array (x axis) of Volume(t)
#      a NumPy array (y-axis) of Flow
# def residualVolume(volume, flow):
#     for (x, y) in zip(volume, flow):
#         if x != 0 and y == 0 :
#             return x
#
#     return "no data found"
#
# # Total Lung Capacity
# # pre: a numpy array (x-axis) of Time
# #      a numpy array (y-axis) of volume
# def totalLungCapacity(volume):
#     return max(volume)

# pressure volume code

# Testing
def loadJson(jsonFile):

    f = open(jsonFile)
    data = json.load(f)

    first_key = next(iter(data))

    time = []
    PList = [] # value of value1
    VList = []
    FList = []

    for x in range(len(data[first_key][0]['Flow'])):
        time.append(float(data[first_key][0]['Pressure'][x]['x']))
        PList.append(float(data[first_key][0]['Pressure'][x]['y']))
        VList.append(float(data[first_key][0]['Volume'][x]['y']))
        FList.append(float(data[first_key][0]['Flow'][x]['y']))

    return time, PList, VList, FList


# setting values after loading
def graphOutput(jsonFile):
    # Pressure flow graph
    # graph(time, pressure)
    result = loadJson(jsonFile)
    time = result[0]
    pressure = result[1]
    volume = result[2]
    flow = result[3]

    plt.subplot(2, 3, 1)
    graph(time, pressure, "seconds", "cm_H2O")
    plt.title("Pressure/Time Graph")

    plt.subplot(2, 3, 2)
    graph(time, volume, "seconds", "mL" )
    plt.title("Volume/Time Graph")

    plt.subplot(2, 3, 3)
    graph(time, flow,"seconds", "L/min" )
    plt.title("Pressure/Time Graph")

    plt.subplot(2, 3, 4)
    graph(volume, flow,"mL", "L/min")
    plt.title("Flow/Volume Graph")

    plt.subplot(2, 3, 6)
    graph(volume, pressure, "mL", "cm_H2O")
    plt.title("Pressure/Volume Graph")


    plt.suptitle("Ventilator Data Graphs")
    plt.tight_layout()

    plt.show()


def compareGraphs(jsonFile1, jsonFile2):
    result = loadJson(jsonFile1)
    volume = result[2]
    flow = result[3]

    result2 = loadJson(jsonFile2)
    volume2 = result2[2]
    flow2 = result2[3]

    plt.axhline(y=0, color='k')

    plt.plot(volume, flow, alpha = 0.5, label = jsonFile1)
    plt.plot(volume2, flow2, alpha=0.5, label = jsonFile2)
    plt.xlabel("Volume")
    plt.ylabel("Flow")


    plt.title("Comparison between " + jsonFile1 + " and " + jsonFile2)
    plt.legend(loc='upper right')

    plt.show()


# Running the code
# compareGraphs('view.json', 'diseased.json')
# Running the code
# graphOutput('view.json')

createTable('view.json')
