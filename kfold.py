import pandas as pd
import numpy as np
import csv

#baca data latih
def readMyFile(filecsv):
    data = []
    with open(filecsv, mode='r', encoding='ISO-8859-1') as csvFile:
        csvReader = csv.DictReader(csvFile, delimiter=';')
        for row in csvReader:
            data.append(row)
    return data

def getTeks(data):
    dataTeks = []
    for row in data:
        dataTeks.append(row["Teks"])
    return dataTeks
datalatih = readMyFile('datalatih.csv')
teksLatih = getTeks(datalatih)
kfold = n_split=5, random_state=42, shuffle=True)
for train_index, test_index in kfold.split(teksLatih):
    print("train index", train_index, "\n")
    print("test index",test_index)


