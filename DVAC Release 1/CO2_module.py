'''
Author:             Matthew McLaughlin
Contact:            mt217258@dal.ca
TODO List:          - Add outlier filtering
Version History: 
'''

#### MODULE VERSION ####
CONST_CO2MODULE_VERSION = "0.1.0" 

#### LIBRARIES ####
import csv
from time import strptime, mktime
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import StringVar

import numpy as np
import pwlf         #piecewise linear fits

#### GLOBAL VARIABLES ####
CO2_data = []               #store for when importing raw data
CO2_summary = {}
CONST_CO2_ROW_DATASTART = 4 #which row the data begins in the excel files

#### CLASSES ####
    #### Magic Methods
    #### Mangled Methods
    #### Muggle Methods
    
class CO2Sensor:
    #### Magic Methods
    def __init__(self, name, listVarNames):
        self.name = name
        self.data = self.__createKeys(listVarNames) #data format: {'Time':[...], 'CO2':[...], 'Temp':[...], etc}
    #### Mangled Methods
    def __createKeys(self, listVarNames):
        dictionary = {}
        for variable in listVarNames:
            dictionary[variable] = []
        return dictionary
    #### Muggle Methods
    def append(self, sample): #sample will be fed as dictionary to be sorted & appended
        for key in sample:
            self.data[key].append(sample[key])
        return True

#### VULGER METHODS #### (They have no class)
def loadCO2Data(filename):
    sensors = [] #list of all sensors        
            
    with open(filename) as csv_file:
        readData = csv.reader(csv_file, delimiter=',')
        for row_index, row in enumerate(readData):
            if row_index == 0:
                for cell in row:
                    if (cell != "Date") and (cell != "Time") and (cell != " "): 
                        sensors.append(CO2Sensor(cell, ["Time","CO2","Temp","Humidity"]))
            if row_index >= CONST_CO2_ROW_DATASTART: #read in data into sensors
                if row_index == CONST_CO2_ROW_DATASTART:
                    startTime = mktime(strptime(str(row[0]) + " " + str(row[1]), "%Y-%m-%d %H:%M:%S"))
                    time = 0
                else:
                    time = mktime(strptime(str(row[0]) + " " + str(row[1]), "%Y-%m-%d %H:%M:%S")) - startTime
                 
                for index, sensor in enumerate(sensors):
                    try:
                        sensor.append({"Time":time, "CO2": float(row[4*index+2]), "Temp": float(row[4*index+3]), "Humidity": float(row[4*index+4])})
                    except:
                        pass 
    
    return sensors

def windowed_mean(x, y, x0, x1):
    total = 0
    n = 0

    for i in range(0,len(x)):
        if x[i] > x0 and x[i] < x1:
            total += y[i]
            n += 1

    return total/n

def filterOutliers(x, y):   #TODO
    X = x
    Y = y
    return X, Y

def generateCO2Report(CO2_data):
    num_regions = 5

    dataSummary = []

    for sensor in CO2_data:
        
        print("Fitting to {name}.".format(name = sensor.name)) #TODO - add progress bar
        
        summary = {}
        summary["Name"] = sensor.name
        
        t = np.asarray(sensor.data["Time"])
        y = np.asarray(sensor.data["CO2"])
        
        T, Y = filterOutliers(t, y)
        
        my_pwlf = pwlf.PiecewiseLinFit(T, Y)
        my_pwlf.fit(num_regions)
        
        for fit_region in range(0, num_regions):
            summary["Fit Region " + str(fit_region+1) + " Start"] = my_pwlf.fit_breaks[fit_region]
            summary["Fit Region " + str(fit_region+1) + " Stop"] = my_pwlf.fit_breaks[fit_region + 1]
            summary["Fit Region " + str(fit_region+1) + " Slope"] = my_pwlf.slopes[fit_region]        
            summary["Fit Region " + str(fit_region+1) + " Intercept"] = my_pwlf.intercepts[fit_region]
            
        summary["Baseline 1"] = windowed_mean(T, Y, my_pwlf.fit_breaks[0], my_pwlf.fit_breaks[1])
        summary["Baseline 2"] = windowed_mean(T, Y, my_pwlf.fit_breaks[4], my_pwlf.fit_breaks[5])    
        summary["R^2"] = my_pwlf.r_squared()
        
        dataSummary.append(summary)
                 
    return dataSummary
    
def saveCO2Report(dataSummary, filename):
    print("Saving down report")
    
    default_savefilename = filename.split("/")[-1].split(".")[0] + "_CO2ReportSummary"
    
    summary_filename = asksaveasfilename(   initialfile=default_savefilename, defaultextension='.csv', 
                                            filetypes=[("csv files", '*.csv')], title="Choose filename to save as:")
    
    saveFile = open(summary_filename, 'w')
    
    header = ','.join(dataSummary[0].keys())
    saveFile.write(header + '\n')
    
    for sensor in dataSummary:
        saveFile.write(','.join(map(str, sensor.values())) + '\n')
        
    saveFile.close()    
    
    print("Save complete!")
    
    return True
        
#### MAIN ####
def main():  
    CO2_filename = askopenfilename(defaultextension='.csv', filetypes=[("csv files", '*.csv')], title="Choose file to load:")
    
    CO2_data = loadCO2Data(CO2_filename)
    dataSummary = generateCO2Report(CO2_data) 
    saveCO2Report(dataSummary, CO2_filename)
    
if __name__ == '__main__':
    main()