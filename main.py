import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import json
import numpy as np

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

    xpoints = np.array(xValues)
    ypoints = np.array(yValues)

    plt.plot(xpoints, ypoints)



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

    time = []
    PList = [] # value of value1
    VList = []
    FList = []

    for x in range(len(data['Data1'][0]['Flow'])):
        time.append(float(data['Data1'][0]['Pressure'][x]['x']))
        PList.append(float(data['Data1'][0]['Pressure'][x]['y']))
        VList.append(float(data['Data1'][0]['Volume'][x]['y']))
        FList.append(float(data['Data1'][0]['Flow'][x]['y']))

    return time, PList, VList, FList


# setting values after loading
def main(jsonFile):
    result = loadJson(jsonFile)
    time = result[0]
    pressure = result[1]
    volume = result[2]
    flow = result[3]

    # Pressure flow graph
    # graph(time, pressure)
    plt.subplot(2, 3, 1)
    graph(time, pressure, "seconds", "cm_H2O")
    plt.title("Pressure/Time Graph")

    plt.subplot(2, 3, 2)
    graph(time, volume, "seconds", "mL" )
    plt.title("Volume/Time Graph")

    plt.subplot(2, 3, 3)
    graph(time, pressure,"seconds", "L/min" )
    plt.title("Pressure/Time Graph")

    plt.subplot(2, 3, 4)
    graph(volume, flow,"mL", "L/min")
    plt.title("Flow/Volume Graph")

    plt.subplot(2, 3, 5)
    graph(volume, pressure, "mL", "cm_H2O")
    plt.title("Pressure/Volume Graph")
    plt.show()

    plt.suptitle("Ventilator Data Graphs")

main('view.json')