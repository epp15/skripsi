from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import math
import csv
import numpy as np
import string
import pandas as pd
#stopword
file_sw = open('tala.txt','r')
stopword = file_sw.read()
array_sw = stopword.split()

#stemming
factory = StemmerFactory()
stemmer = factory.create_stemmer()


# prepocessing
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


def lexicalAnalysis(data):
    sentence = []
    words = []
    token = []

    # case folding
    for row in data:
        sentence.append(row.lower())

    # get word per sentence
    for i in range(len(sentence)):
        sentence[i] = sentence[i].split()

    # get all words
    for row in sentence:
        for row2 in row:
            temp = row2.split().pop()
            words.append(temp)

    # deleting link
    for n, row in enumerate(words):
        if re.match(r"\w+(?:\.me)(?:.*)", str(row)) or re.match(r"\w+(?:\.com)", str(row)) or re.match(
                r"(?:(https?|s?ftp):\/\/)(?:.*)?", str(row)) or re.match(r"(?:www\.)(?:.*)?", str(row)):
            del words[n]

    # deleting punctuation
    for i in range(len(words)):
        temp = re.sub(r'[^\w\s]', ' ', str(words[i]))
        words[i] = temp

    # deleting number
    for i in range(len(words)):
        temp = re.sub(r'\d', ' ', str(words[i]))
        words[i] = temp

    # clean the space
    for row in words:
        temp = row.split()
        token += temp

    for i in range(len(token)):
        for n, row in enumerate(token):
            if len(
                    row) < 2 or row == "xxx" or row == "gb" or row == "ff" or row == "rp" or row == "bb" or row == "dll" or row == "ii" or row == "rb" or row == "mb":
                del token[n]

    return token


def stopwordRemoval(data):
    # filtered by sastrawi
    for i in range(len(data)):
        for n, row in enumerate(data):
            if row in array_sw:
                del data[n]
    return data


def stemming(data):
    sentence = ' '.join(data)
    output = stemmer.stem(sentence)
    hasil_stem = output.split()
    array_stem = []
    for row in hasil_stem:
        array_stem.append(row)
    return array_stem


def getTerm(data):
    term = []
    for row in data:
        if row not in term:
            term.append(row)
    return term

#print(getTerm)

# term weighting
def getTermInDoc(dataTeks):
    termInDoc = []
    temp = []
    temp4 = ' '
    for i in range(len(dataTeks)):
        temp5 = []
        temp5.append(dataTeks[i]["Teks"])
        temp5.append(temp4)
        temp.append(temp5)

    temp6 = []
    for row in temp:
        temp3 = stemming(stopwordRemoval(lexicalAnalysis(row)))
        temp6.append(temp3)
    return temp6


def rawWeight(dataTeks, term):
    jum = []
    print("cek")
    for cek in dataTeks:
        print(cek)
    for k in range(0, len(dataTeks)):
        jum.append([])
        for l in term:
            if l not in dataTeks[k]:
                jum[k].append(0)
            elif l in dataTeks[k]:
                x = dataTeks[k].count(l)
                jum[k].append(x)
    return jum


# Likelihood atau Conditional probability
def getKelasRawData(data, raw):
    cek = pd.DataFrame(data)
    print(cek.head())
    result = []
    for i in range(len(data)):
        temp = {}
        temp["raw"] = raw[i]
        temp["kelas"] = data[i]["label"]
        result.append(temp.copy())
    return result


def getTotalTermInKelas(data):
    result = {}
    for row in data:
        if row["kelas"] in result:
            result[row["kelas"]] += sum(row["raw"])
        else:
            result[row["kelas"]] = sum(row["raw"])
    return result


def getRawPerKelas(data):
    result = {}
    for row in data:
        if row["kelas"] not in result:
            result[row["kelas"]] = []
        result[row["kelas"]].append(row["raw"])
    return result






# fase training
def Likelihood(data, totalTermPerKelas, totalTerm):
    totalPerTermPerKelas = {}
    hasilLikelihood = {}
    for row in data:
        if row in totalPerTermPerKelas:
            totalPerTermPerKelas[row] = [sum(x) for x in zip(*data[row])]
        else:
            totalPerTermPerKelas[row] = [sum(x) for x in zip(*data[row])]

    for row in totalPerTermPerKelas:  # 3 index
        if row in hasilLikelihood:
            temp = []
            for row2 in totalPerTermPerKelas[row]:
                temp2 = (row2 + 1) / (totalTermPerKelas[row] + totalTerm)
                temp.append(temp2)
            hasilLikelihood[row] = temp
        else:
            temp = []
            for row2 in totalPerTermPerKelas[row]:
                temp2 = (row2 + 1) / (totalTermPerKelas[row] + totalTerm)
                temp.append(temp2)
            hasilLikelihood[row] = temp
    return hasilLikelihood


# fase testing
def prior(dataTraining):
    result = {}
    for row in dataTraining:
        if row["label"] in result:
            result[row["label"]] += 1
        else:
            result[row["label"]] = 1

    for row in result:
        result[row] = result[row] / len(dataTraining)

    return result


def findMatchTerm(termInDocTesting, term):
    indexTerm = []
    for i in range(len(termInDocTesting)):
        # print(termInDocTesting[i])
        indexTerm.append([])
        for row2 in termInDocTesting[i]:
            if row2 in term:
                indexTerm[i].append(term.index(row2))
            else:
                indexTerm[i].append("null")

    return indexTerm


def posterior(indexTerm, hslLikelihood, hslprior):
    result = {}
    indexTerms = []

    for row in indexTerm:
        if row not in indexTerms and row != "null":
            indexTerms.append(row)

    # print(indexTerms)

    for row in hslprior:
        if row in result:
            for index in indexTerms:
                temp = 1
                temp *= hslLikelihood[row][int(float(index))]
            result[row] = temp
        else:
            for index in indexTerms:
                temp = 1
                temp *= hslLikelihood[row][int(float(index))]
            result[row] = temp

    # print(result)

    temp3 = []
    for row in result:
        temp3.append(result[row])

    temp4 = max(temp3)
    # print(temp4)

    label = ''

    for x, row in result.items():
        if row == temp4:
            label = x

    return label


# main menu
kondisi = True
while(kondisi):
    print("Menu : ")
    print("1. data latih ulasan dengan data uji ulasan")
    print("2. hasil naive bayes")
    print("3. selesai")
    menu = int(input("Masukan pilihan : "))
    datalatih = readMyFile('datalatih.csv')
    datauji = readMyFile('datauji.csv')

    if menu == 1:

        # HASIL PRE-PROCESSING DATA LATIH
        teksLatih = getTeks(datalatih)
        tokenLatih = stemming(stopwordRemoval(lexicalAnalysis(teksLatih)))
        termInDoc = getTermInDoc(datalatih)
        print("===============================")
        print("hasil term data latih ")
        for data in termInDoc:
            print(data)
        print("===============================")
        print("hasil term akhir data latih")
        termLatih = getTerm(tokenLatih)
        totalTerm = len(termLatih)
        print(termLatih)
        result = {}
        result['tekslatih'] = teksLatih
        result['tokenlatih'] = tokenLatih
        result['term'] = termInDoc
        result['lenterm'] = totalTerm
        with open('tekslatih.json','w',encoding='utf-8') as f:
            json.dump(result,f)


        #HASIL PRE-PROCESSING DATA UJI
        teksUji = getTeks(datauji)
        tokenUji = stemming(stopwordRemoval(lexicalAnalysis(teksUji)))
        print("===============================")
        print("hasil term data uji")
        termInDocTesting = getTermInDoc(datauji)
        for data in termInDocTesting:
            print(data)
        print("===============================")
        print("hasil term akhir data uji")
        termUji = getTerm(tokenUji)
        print(termUji)

    elif menu == 2 :
        #NAIVE DATA LATIH
        teks = getTeks(datalatih)

        token = stemming(stopwordRemoval(lexicalAnalysis(teks)))
        term = getTerm(token)
        totalTerm = len(term)
        termInDoc = getTermInDoc(datalatih)
        print("raw")
        raw = rawWeight(termInDoc, term)
        print(raw)
        print("raw dengan kelasnya")
        raw = getKelasRawData(datalatih, raw)
        print(raw)
        totalTermPerKelas = getTotalTermInKelas(raw)
        print("total term per kelas")
        print(totalTermPerKelas)
        print("Raw dengan kelas yang sama")
        rawPerKelas = getRawPerKelas(raw)
        print(rawPerKelas)
        print("likelihood")
        hasilLikelihood = Likelihood(rawPerKelas, totalTermPerKelas, totalTerm)

        print(hasilLikelihood)
        # NAIVE BAYES DATA UJI
        termInDocTesting = getTermInDoc(datauji)
        # print("term in doc data uji")
        # for data in termInDocTesting:
        #     print(data)
        # print(termInDocTesting)
        print("PRIOR")
        hasilPrior = prior(datalatih)
        print(hasilPrior)
        print("FIND MATCH TERM")
        indexMacthTerm = findMatchTerm(termInDocTesting, term)
        print(indexMacthTerm)
        hasilPosterior = []
        for i in range(len(indexMacthTerm)):
            temp = {}
            temp["data ulasan"] = i
            temp["label"] = posterior(indexMacthTerm[i], hasilLikelihood, hasilPrior)
            hasilPosterior.append(temp)
        print("Hasil Klasifikasi")
        print(hasilPosterior)
        print(list(hasilPosterior[0].keys()))
        for data in hasilPosterior:
            print(list(data.values()))

    elif menu == 3:
        kondisi = False

    else:
        print("Pilihan yang dimasukan salah")