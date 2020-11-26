# import numpy as np
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import math
#stopword
file_sw=open('tala.txt','r')
stopword= file_sw.read()
array_sw = stopword.split()

#tokenisasi
dokumen = open('dokumen.txt','r')
baca = dokumen.read().lower()

dokumen2 = baca.replace(".", "")
array_dok = dokumen2.split()
print("\nHasil Tokenisasi:")
print(array_dok)

filtered=[]
for e in array_dok:
    if not e in array_sw:
        filtered.append(e)
print("\nHasil Filtering:")
print(filtered)

#stemming
factory = StemmerFactory()
stemmer = factory.create_stemmer()
sentence = ' '.join(filtered)
output   = stemmer.stem(sentence)
hasil_stem = output.split()
array_stem = []

for a in hasil_stem:
    array_stem.append(a)
print("\nHasil Stemming:")
print(array_stem)

#akhir term
term=[]
for kata in array_stem:
  if kata not in term:
      term.append(kata)
print("\nHasil Akhir Term:")
print(term)

def filter_kalimat(kalimat):
    arr_kata = kalimat.split()
    kalimat_filtered=[]
    for i in arr_kata:
        if i not in array_sw:
            kalimat_filtered.append(i)
        elif i in array_sw:
            kalimat_filtered.append("null")
    kalimat_baru = ' '.join(kalimat_filtered)
    return kalimat_baru

def stem_kalimat(kalimat):
    kal_stem = stemmer.stem(kalimat)
    kal_after = kal_stem.split()
    return kal_after

def baca(nama_file):
    buka_dok = open(nama_file,'r')
    baca_dok = buka_dok.read().lower()
    dokumen3 = baca_dok.split(".");
    dokumen3.pop()
#    print("\n====== Membaca Dokumen Per Kalimat ======")
    print(dokumen3)
    return dokumen3
    
def stem_filter(file_utuh):
    dokumen_baru=[]
    for x in file_utuh:
        x = stem_kalimat(filter_kalimat(x))
        dokumen_baru.append(x)
    print(dokumen_baru)
    return dokumen_baru

def binaryWeight(array):
    biner=[]
    for k in range(0,len(array)):
        biner.append([])
        for l in term:
            if l not in array[k]:
                biner[k].append(0)
            elif l in array[k]:
                biner[k].append(1)
    #print("\n============== Binary Weighting ==============")
    return biner

def raw(array):
    jum=[]
    for k in range(0,len(array)):
        jum.append([])
        for l in term:
            if l not in array[k]:
                jum[k].append(0)
            elif l in array[k]:
                x = array[k].count(l)
                jum[k].append(x)    
    return jum

def logFrequency(array):
    log=[]
    for x in range(len(array)):
        log.append([])
        for y in range(len(array[x])):
            if array[x][y] == 0:
                log[x].append(0)
            else:
                z = 1 + math.log(array[x][y], 10);
                log[x].append(z)
    return(log)
    
def df(array):
    dfw=[]
    for x in range(len(array[0])):
        temp=0
        for y in range(len(array)):
            temp+=array[y][x]
        #print(temp)
        dfw.append(temp)
    return dfw

def idf(hasilBinary, array_hasil):
    idf=[]
    for x in range(len(hasilBinary)):
        temp=len(array_hasil)/hasilBinary[x]
        temp2=math.log(temp, 10)
        idf.append(temp2)
    return idf

def tfidf(log, idf):
    tfidf=[]
    for x in range(len(log)):
        tfidf.append([])
        for y in range(len(log[x])):
            tfidf[x].append(log[x][y]*idf[y])
    return tfidf
        
    

print("\n====== Membaca Dokumen Per Kalimat ======")    
array_hasil = baca('dokumen.txt')
print("\n\n====== Membaca Term yang ada Per Kalimat(dokumen) ======")
null_filled=stem_filter(array_hasil)
print("\n============== Binary Weighting ==============")
print(binaryWeight(null_filled))
print("\n============== Raw Term Weighting ==============")
print(raw(null_filled))
print("\n============== Log Frequency Weighting ==============")
hasilRaw = raw(null_filled)
print(logFrequency(hasilRaw))
print("\n============== Document Frequency Weight ==============")
hasilBinary = binaryWeight(null_filled)
print(df(hasilBinary))
print("\n============== Inverse Document Frequency Weight ==============")
hasilDf=df(hasilBinary)
print(idf(hasilDf,array_hasil))
print("\n============== tf-idf Weighting ==============")
hasilLog=logFrequency(hasilRaw)
hasilIdf=idf(hasilDf,array_hasil)
print(tfidf(hasilLog, hasilIdf))




#print("\n")
#print("tf idf")
#tfidf=[]
#for xxxx in range(len(log)):
#    tfidf.append([])
#    for yyyy in range(len(log[xxxx])):
#        tfidf[xxxx].append(log[xxxx][yyyy]*idf[yyyy])
#        
#print(tfidf)



#idf=[]
#
#for xxx in range(len(df)):
#    zz=len(bb)/df[xxx]
#    zzz=math.log(zz, 10)
#    idf.append(zzz)
#    
#print(idf)

#print(bb)
#print(len(bb[1]))

#print("\n")
#print("log frequency");
#def logFrequency(array):
#    log=[]
#    for x in range(len(array)):
#        log.append([])
#        for y in range(len(array[x])):
#            if array[x][y] == 0:
#                log[x].append(0)
#            else:
#                z = 1 + math.log(bb[x][y], 10);
#                log[x].append(z)
#    return(log)


#log=[]
#print("\n")
#print("log frequency");
#for x in range(len(bb)):
#    log.append([])
#    for y in range(len(bb[x])):
#        if bb[x][y] == 0:
#            log[x].append(0)
#        else:
#            z = 1 + math.log(bb[x][y], 10);
#            log[x].append(z)
#
#print(log)
#
#
#print("\n")
#print("df")
#bbb = binaryWeight(null_filled)
#df=[]
#for xx in range(len(bbb[0])):
#    temp=0
#    for yy in range(len(bbb)):
#        temp+=bbb[yy][xx]
#    #print(temp)
#    df.append(temp)
#
#print(df)
#
#print("\n")
#print("idf")
#idf=[]
#
#for xxx in range(len(df)):
#    zz=len(bb)/df[xxx]
#    zzz=math.log(zz, 10)
#    idf.append(zzz)
#    
#print(idf)
#
#print("\n")
#print("tf idf")
#tfidf=[]
#for xxxx in range(len(log)):
#    tfidf.append([])
#    for yyyy in range(len(log[xxxx])):
#        tfidf[xxxx].append(log[xxxx][yyyy]*idf[yyyy])
#        
#print(tfidf)
#    
    

    









