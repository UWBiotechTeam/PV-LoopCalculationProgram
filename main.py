import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate
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

    plt.margins(0.005)
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')

    xpoints = np.array(xValues)
    ypoints = np.array(yValues)

    plt.plot(xpoints, ypoints)
    
# pre: Takes in JsonFile for input:
# Parses through and seperates the 
# time, pressure, volume, and flow values. 
# post: creates a dictionary with those and 
# converts it into a csv file.
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
    df.to_csv('DataTable.csv', index=False)

# same concept as create table
# post: Prints out a table
# instead of a downloadable csv file.
def printTable(jsonFile):
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
    print(tabulate(df, headers='keys', tablefmt='pretty'))

# Pre: Takes in pressure and volume arrays
# These hold the values of the pressure and volume,
# in chronological order
# Post: calculates the compliance value
def compliance(pressure, volume):
    deltaV = peakVolume(volume) - volume[0]
    deltaP = peakInspirationPressure(pressure) - pressure[0]
    compliance = deltaV / deltaP
    return compliance

# Pre: takes in pressure array
# Post: returns the highest value in that array,
# corresponding to the Peak Inspiration Pressure.
def peakInspirationPressure(pressure):
    maxValue = 0
    for x in range(len(pressure)):
        if pressure[x] > maxValue:
            maxValue = pressure[x]
    return maxValue

# Pre: takes in pressure arrays 
# Post: returns the min value for the pressure, 
# or the Positive End Expiratory value.
def positiveEndExpiratory(pressure):
    minValue = 999999999
    for x in range(len(pressure)):
        if pressure[x] < minValue:
            minValue = pressure[x]
    return minValue

# Pre: takes in a volume array
# Post: returns the max volume value.
def peakVolume(volume):
    maxValue = 0
    for x in range(len(volume)):
        if volume[x] > maxValue:
            maxValue = volume[x]
    return maxValue

# Pre: takes in a pressure arary
# Post: returns the plateau pressure.
# Does this by finding the second occurance at which
# two consecutive pressure values are equal.
def platPressure(pressure):
    equalValue = -15
    begValue = pressure[0]
    for x in range(len(pressure)):
        if pressure[x] != begValue:
            if pressure[x] == equalValue:
                return pressure[x]
            else:
                equalValue = pressure[x]

# Pre: takes in pressure and volume arrays.
# Post: returns the resistence based on the 
# given data from the arrays.
def resistence(pressure, volume):
    deltaV = peakVolume(volume) / 60 - volume[0]
    resistence = (peakInspirationPressure(pressure) - platPressure(pressure)) / deltaV
    return resistence

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

# Pre: JsonFile with data
# Post: creates graph for flow versus volume
def flowVVolume(jsonFile):
    result = loadJson(jsonFile)
    volume = result[2]
    flow = result[3]

    graph(volume, flow,"mL", "L/min")
    plt.title("Flow/Volume Graph")

# setting values after loading
def graphOutput(jsonFile):
    # Pressure flow graph
    # graph(time, pressure)
    result = loadJson(jsonFile)
    time = result[0]
    pressure = result[1]
    volume = result[2]
    flow = result[3]

    compliance1 = compliance(pressure, volume)
    positiveEndExpiratory1 = positiveEndExpiratory(pressure)
    resistence1 = resistence(pressure, volume)
    peakInspirationPressure1 = peakInspirationPressure(pressure)


    plt.subplot(2, 3, 1)
    graph(time, pressure, "seconds", "cm_H2O")
    plt.title("Pressure/Time Graph")

    plt.subplot(2, 3, 2)
    graph(time, volume, "seconds", "mL" )
    plt.title("Volume/Time Graph")

    plt.subplot(2, 3, 3)
    graph(time, flow,"seconds", "L/min" )
    plt.title("Flow/Time Graph")

    plt.subplot(2, 3, 4)
    graph(volume, flow,"mL", "L/min")
    plt.title("Flow/Volume Graph")

    plt.subplot(2, 3, 5)
    graph(volume, pressure, "mL", "cm_H2O")

    plt.title("Pressure/Volume Graph")


    plt.suptitle("Ventilator Data Graphs")
    plt.tight_layout()

    plt.figtext(.72, .35, "Peak Inspiration Pressure = " + str(peakInspirationPressure1) + " cm H2O", fontsize='small', fontname=  'monospace')
    plt.figtext(.72, .4, "Positive End-Expiratory: " + str(positiveEndExpiratory1) + " cm H2O", fontsize='small', fontname=  'monospace')
    plt.figtext(.72, .3, "Compliance = " + str(compliance1) + " mL/ cm H2O", fontsize='small', fontname=  'monospace')
    plt.figtext(.72, .25, "Resistence = " + str(resistence1) + " cm H2O / L/s", fontsize='small', fontname=  'monospace')

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
graphOutput('view.json')

# createTable('view.json')
# printTable('view.json')
