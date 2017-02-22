from __future__ import division
import numpy as np
import math


#inisialisasi data

data = np.array([(2,0,0,4,5,0),
                 (5,0,4,0,0,1),
                 (0,0,5,0,2,0),
                 (0,1,0,5,0,4),
                 (0,0,4,0,0,2),
                 (4,5,0,1,0,0)])

user_yang_dicari = 5 #user yang dicari dikurang 1

#========================code============================================================

rata2 = {}
sim = {}
raw = {}
predicted = {}
listtetangga = []
jumsim = 0
selecteduser = data[[user_yang_dicari],:]

def hitungrata(row):
    tot = 0
    jum = 0
    for d in row:
        if d != 0:
            jum+=1
            tot+=d
    return tot / jum

def carirata2user(data):
    i = 0
    for row in data:
        rata2['user '+str(i)] = hitungrata(row)
        i += 1

def cariygsama(ke):
    for index, row in enumerate(data):
        if row[ke] != 0:
            if not (cekisilist(index,listtetangga)) and index != user_yang_dicari:
                listtetangga.append(index)


def cekisilist (index, list1):
    if len(list1) != 0:
        for i in list1:
            if index == i:
                return True
        else:
            return False
    else:
        return False;

def caritetangga(user):
    for cari in user:
        for index, isi in enumerate(cari):
            if isi != 0:
                cariygsama(index)


def similiarity(pilih,user):
    rowselected = data[[pilih],:]
    rowuser = data[[user],:]
    totkes = 0
    tot3 = 0
    tot5 = 0
    totkes1 = 0
    for angka in rowselected:
        for index, isi in enumerate(angka):
            if isi != 0:
                tot = 0
                tot1 = 0
                tot2 = 0
                tot4 = 0
                for angka1 in rowuser:
                    if angka1[index] != 0:
                        tot = isi - rata2['user ' + str(pilih)]
                        tot1 = angka1[index] - rata2['user '+str(user)]
                        tot = tot * tot1
                        tot2 = (isi - rata2['user ' + str(pilih)])**2
                        tot3 = tot3 + tot2
                        tot4 = (angka1[index] - rata2['user ' + str(user)])**2
                        tot5 = tot5 + tot4
                totkes = totkes + tot
                totkes1 = tot3 * tot5
    sim['sim('+str(pilih)+','+str(user)+')'] = totkes / math.sqrt(totkes1)

def carisimiliarity():
    for i in listtetangga:
        similiarity(user_yang_dicari,i)

def sigmasim(similiar):
    tot = 0
    for key in similiar:
        if similiar[key] < 0:
            tot = tot + (similiar[key] * -1)
        else:
            tot = tot + similiar[key]
    return tot

def ybintang(pilih,index):
    for angka in listtetangga:
        totkes = 0
        tot = 0
        rowtetangga = data[[angka], :]
        for isi in rowtetangga:
            if isi[index] != 0:
                tot = isi[index] - rata2['user '+str(angka)]
                tot = sim['sim('+str(pilih)+','+str(angka)+')'] * tot
        totkes = totkes + tot
        if totkes != 0 :
            raw[str(index)] = rata2['user ' + str(pilih)] + (totkes / jumsim)
            predicted['y*(' + str(pilih) + ',' + str(index) + ')'] = rata2['user ' + str(pilih)] + (totkes / jumsim)


def predictedrating():
    for i in selecteduser:
        for index, d in enumerate(i):
            if d == 0:
                ybintang(user_yang_dicari,index)



carirata2user(data)
caritetangga(selecteduser)
carisimiliarity()
jumsim = sigmasim(sim)
predictedrating()
print 'list tetangga = %s' % (listtetangga)
print 'rata - rata = %s' % (rata2)
print 'similiarity = %s' % (sim)
print 'jumlah similiarity = %s' % (jumsim)
print 'predicted rating = %s' % (predicted)
print 'item yang direkomendasikan untuk user %s, adalah item ke %s' %(user_yang_dicari,max(raw, key = raw.get))
