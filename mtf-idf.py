from math import *

dokumen = open('datalatih.csv','r')
baca = dokumen.read().lower()

#step 1 〖𝑡𝑓〗_(𝑡,𝑑)×log⁡〖√(𝑇_𝑐 )/𝑇_𝑡 〗
def step1 (array):
    stp1=[]
    log=[]
    Tf,Tc,Tt=[]
    for x in range (0,len(array)):
     stp1.append([])
     log.append([])
     for y in range (len(array[x])):
         if array [x][y] == 0:
             stp1[x].append(0)
         else:
             z = Tf * log(sqrt(Tc)/Tt)
    return step1

#step 2 ∑2_(𝑡=1)^𝑛▒〖〖𝑡𝑓〗_(𝑡,𝑑)〗^2 (mengambil dari raw term)
def step2(array):
    stp2=[]
    for x in range(len(array[0])):
        temp = 0
        for y in range(len(array)):
            temp= array[x]^2[y]^2
            stp2.append(temp)
    return stp2

#step 3 (〖〖𝑙𝑒𝑛𝑔𝑡ℎ〗_𝑑〗^2/√(𝑇_𝑐 ))
def step3 (array):
    stp3=[]
    for x in range (len(array[0])):
      temp=0
      for y in range(len(array)):
          temp= (array[x]^2 sqrt[y])
    return stp3

#step 4 (∑2_(𝑡=1)^𝑛▒〖〖𝑡𝑓〗_(𝑡,𝑑)〗^2 )×(〖〖𝑙𝑒𝑛𝑔𝑡ℎ〗_𝑑〗^2/√(𝑇_𝑐 ))
# (gabungan step 2 dan step 3)
def step4 (stp2,stp3):
    stp4=[]
    for x in range(len(stp2)):
        temp= len(stp3)*(stp2)[x]
        stp4.append(temp)
    return stp4

#step 5 log⁡[(∑2_(𝑡=1)^𝑛▒〖〖𝑡𝑓〗_(𝑡,𝑑)〗^2 )×(〖〖𝑙𝑒𝑛𝑔𝑡ℎ〗_𝑑〗^2/√(𝑇_𝑐 ))]
# (gabungan step 3 dan step 4 lalu di log)
def step5 (stp3,stp4):
    stp5=[]
    for x in range(len(stp3)):
        stp5.append([])
    for y in range(len(stp3[x])):
        stp5[x].append(math.log(stp3*stp4))
    return stp5

#step 6 〖𝑚𝑇𝐹〗_(𝑡,𝑑)=(〖𝑡𝑓〗_(𝑡,𝑑)×log⁡〖√(𝑇_𝑐 )/𝑇_𝑡 〗)/log⁡[(∑2_(𝑡=1)^𝑛▒〖〖𝑡𝑓〗_(𝑡,𝑑)〗^2 )×(〖〖𝑙𝑒𝑛𝑔𝑡ℎ〗_𝑑〗^2/√(𝑇_𝑐 ))]
#(gabungan step 1 dan step 5)
def step6 (stp1,stp5):
    stp6=[]
    for x in range(len(stp1)):
        stp6.append([])
        for y in range(len(stp1[x])):
            stp6.append(stp1/stp5)
    return stp6

print("\n====== Hasil Pembobotan ======")
array_hasil = baca('datalatih.csv')

print("\n\n====== Membaca Term yang ada Per Kalimat(dokumen) ======")
null_filled=stem_filter(array_hasil)

print("\n============== Hasil Step 1 ==============")
print(step1(null_filled))

print("\n============== Hasil Step 2 ==============")
print(step2(null_filled))

print("\n============== Hasil Step 3 ==============")
print(step3(null_filled))

print("\n============== Hasil Step 4 ==============")
hasilstep3 = step3(null_filled)
print(step4(hasilstep3))

print("\n============== Hasil Step 5 ==============")
hasilstep4 = step4(null_filled)
print(step5(hasilstep4,array_hasil))

print("\n============== Hasil Step 6 ==============")
hasilstep1 = step1(null_filled)
hasilstep5 = step5(hasilstep3,hasilstep4)
print(step5(hasilstep1,hasilstep5))