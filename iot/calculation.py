import os
import math
import csv
from os.path import exists
import pandas as pd
from matplotlib import pyplot as plt
from numpy import diff
import numpy as np


results_path = os.path.join(".." ,"figures", "results", "results.csv")



#Calculating the Root-Mean-Square Error of the measurement vs real values
def calculate_error(real, measured):
    #Interpolating the samples
    diff = (len(real)-1) / (len(measured)-1)
    interp_measured = np.interp(range(len(real)),
            [x*diff for x in range(len(measured))],
            measured)

    summ = 0
    for i in range(len(real)):
        summ += pow(real[i] - interp_measured[i], 2)
    error = math.sqrt(summ/len(real))
    return(error)



#Save results in csv file
def save_results(newline):    
    if exists(results_path) == False:
        with open(results_path, "a+", newline = "") as file:
            writer = csv.writer(file, delimiter = ";")
            writer.writerow(["Cost", "Sensor distance","Number of sensors", "Static", "Sampling time", "Simulation time", "Error", "Accuracy"])
            writer.writerow(newline)
    else:
        with open(results_path, "a+", newline = "") as file:
            writer = csv.writer(file, delimiter = ";")
            writer.writerow(newline)
            
#Evaluation of Root-Mean-Square Error against Total system cost
def evaluate():
    number = []
    acc_900 = []
    acc_3600 = []
    acc_14400 = []
    cost_900 = []
    cost_3600 = []
    cost_14400 = []
    
    df = pd.read_csv(results_path, delimiter=';')
    rows = [tuple(x) for x in df.values]
    for i in rows:
        if i[4] == 900:
           acc_900.append(round(i[7], 3))
           cost_900.append(i[0]) 
        elif i[4] == 3600:
           acc_3600.append(round(i[7], 3))
           cost_3600.append(i[0])
        elif i[4] == 14400:
           acc_14400.append(round(i[7], 3))
           cost_14400.append(i[0])
        

       
        
    #Plotting accuracy vs error
    plt.figure()
    plt.scatter(cost_900, acc_900, s = 300, c = "red")    
    plt.scatter(cost_3600, acc_3600, s = 300, c = "orange")   
    plt.scatter(cost_14400, acc_14400, s = 300, c = "yellow")
    
    
    # plt.plot(cost, error10, 'ro')
    # plt.plot(cost, error30, 'bo')
    # plt.plot(cost, error60, 'go')
    # plt.plot(cost, error120, 'yo')
    
    plt.ylabel("Accuracy [%]", fontsize = 30)
    plt.title("Effect of different sampling periods", fontsize = 30)
    plt.xlabel("Total system cost [€]", fontsize = 30)
    plt.legend(["15 min", "1 hour", "4 hours"], fontsize = 20)
    plt.xticks(fontsize = 30)
    plt.yticks(fontsize = 30)
    plt.show()
      
def accuracy(real, measured):
    values = []
    
    #Interpolate the samples
    diff = (len(real)-1) / (len(measured)-1)
    interp_measured = np.interp(range(len(real)),
            [x*diff for x in range(len(measured))],
            measured)
    
    
    #Calculating accuracy
    for i in range(len(interp_measured)):
        if (real[i] > 0):
            acc = 1 - abs(real[i] - interp_measured[i])/real[i]
            values.append(acc)
            
    
    accuracy = sum(values)/len(values)
    return(accuracy)
    
def accuracy_per_cost():
    cost = []
    accuracy = []
    df = pd.read_csv(results_path, delimiter=';')
    rows = [tuple(x) for x in df.values]
    for i in rows:
        cost.append(i[0])
        accuracy.append(i[7])
    
    #Normalize error
    acc_norm = []
    added_value = []
    for i in accuracy:
        acc_norm.append((i - min(accuracy)) / (max(accuracy) - min(accuracy)))

    for i in range(len(acc_norm)):
        added_value.append(acc_norm[i] / cost[i])
    
       
    #Plotting cost vs error
    plt.figure()
    plt.plot(cost, acc_norm, 'ro')
    #plt.plot(cost, added_value, 'go')
    plt.ylabel("Accuracy / cost")
    plt.xlabel("Total system cost [€]")
    plt.title("Value of price")
    plt.show()
    
    print("Highest value: ", max(added_value), " at the price of: ", cost[added_value.index(max(added_value))])
    

    
# real = [1, 1, 1, 2]
# mes = [1, 1.9, 1.9, 2]
# print(accuracy(real, mes))
# plt.plot(range(len(real)), real)
# plt.plot(range(len(mes)), mes)
# plt.show()
#evaluate()
#accuracy_per_cost()
        
evaluate()
        
