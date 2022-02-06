# PV-LoopCalculationProgram
Given a time series of flow of human respiration (such as shown on mechanical ventilators), produce a graph of the flow-volume loop.

Developed for the RICE RespiraCon II Hackathon <br> <br>
Contributors: 
<br> Derek Zhu - Software Developer/Engineer
<br> Rishi Bathina - Software Developer/Engineer
<br> Ziao Yin - Medical Researcher/Engineer
<br> Truc Mai - Medical Researcher/Engineer
<br>

<h1> Functions </h1> <br>
printTable(jsonFile) - Intakes a JSON file, prints out organzied data values
<br>
```python
printTable('data.json') # data.json is the inputted json file

<img src="https://user-images.githubusercontent.com/57535849/152704873-4549cf48-0253-4443-afc7-5e89999c69cb.png" width="300" height="250"> <br>

createTable(jsonFile) - Intakes a JSON file, creates a CSV file (downloads directly to user's computer) <br>
                        organized in terms of time, containing columns Volume, Pressure, and Flow <br>
```python
createTable('data.json') # data.json is the inputted json file
```
<br>
graphOutput(jsonFile) - Intakes JSON file, outputs GUI with 5 graphs: <br>
                        1) Pressure/Time <br>
                        2) Volume/Time <br>
                        3) Flow/Time <br>
                        4) Flow/Volume <br>
                        5) Pressure/Volume <br>
```python
graphOutput('data.json') # data.json is the inputted json file
```
