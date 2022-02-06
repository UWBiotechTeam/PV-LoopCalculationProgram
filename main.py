import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import json
import numpy as np
from tabulate import tabulate

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

    plt.margins(0)
    plt.grid(True, which='both')

    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')

    xpoints = np.array(xValues)
    ypoints = np.array(yValues)

    plt.xlim()
    plt.ylim([-1, 0])


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

def createDic():
    theDictionary = {'Pressure': [], 'Volume': [], 'Flow': [], 'Compliance': [], 'Peak Inspiration Pressure': [], 'Positive End Expiratory': []}
    for x in range(len(pressure)):
        theDictionary['Pressure'][x] = pressure[x]
    for x in range(len(volume)):
        theDictionary['volume'][x] = volume[x]
    for x in range(len(flow)):
        theDictionary['Flow'][x] = flow[x]
    for x in range(len(pressure) - 2):
        theDictionary['Compliance'][x] = 'N/A'
    theDictionary['Compliance'][len(pressure) - 1] = compliance(pressure, volume)
    for x in range(len(pressure) - 2):
        theDictionary['Peak Inspiration Pressure'][x] = 'N/A'
    theDictionary['Peak Inspiration Pressure'][len(pressure) - 1] = peakInspirationPressure(pressure)
    for x in range(len(pressure) - 2):
        theDictionary['Positive End Expiratory'][x] = 'N/A'
    theDictionary['Positive End Expiratory'][len(pressure) - 1] = positiveEndExpiratory(pressure)
    return theDictionary

def createTable(dict):
    print(tabulate(dict, headers='keys', tablefmt='fancy_grid', showIndex=True))

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
    global time, pressure, volume, flow
    result = loadJson(jsonFile)
    time = result[0]
    pressure = result[1]
    volume = result[2]
    flow = result[3]
    theDictionary = createDic()
    createTable(theDictionary)

    # Pressure flow graph
    # graph(time, pressure)
    plt.subplot(2, 3, 1)
    a = graph(time, pressure, "seconds", "cm_H2O")
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


    plt.suptitle("Ventilator Data Graphs")
    plt.tight_layout()

    plt.show()

<<<<<<< HEAD

# Running the code
graphOutput('view.json')
=======
main('view.json')
>>>>>>> 7abfafd13452d4eb1c8b51497e228309cb8c723b
