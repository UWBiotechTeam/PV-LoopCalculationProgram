import matplotlib.pyplot as plt
import seaborn as sns
import json
import numpy as np
 # open json file
 # pre: file name (in json)
 # Stirngs: value1 and value2, where value1/value2
 # is (pressure, volume, or flow)

# Output a graph based on values
# pre: numpy arrays that represent x and y data points
# post: plots the data

# Allows graphing PV and FV
# PV-plot -> graph(volume, pressure)
# FV-plot -> graph(volume, flow)
def graph(xValues, yValues):
    xpoints = np.array(xValues)
    ypoints = np.array(yValues)

    plt.plot(xpoints, ypoints)
    plt.show()

# def createDic(volume, time, flow, pressure, volTime):
#     if volume.length == time.length :
#         for x in range(0, volume.length - 1):
#             volTime[time[x]] = volume[x], flow[x], pressure[x]

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
result = loadJson('view.json')
time = result[0]
pressure = result[1]
volume = result[2]
flow = result[3]

# Pressure flow graph
graph(time, pressure)
#graph(volume, pressure)
# graph(volume, flow)
