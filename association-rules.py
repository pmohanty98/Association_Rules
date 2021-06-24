import pandas as pd
import copy
import sys
import itertools

Training = pd.read_csv(sys.argv[1])
Training = pd.get_dummies(Training.astype(str))

minsup = float((sys.argv[2]))
minconf = float((sys.argv[3]))
freqlist=[0]*152
ruleslist=[]
fruleslist=[0]*152

maxlist=[]
def Rulecalcuator(setlist,intsup):
    for i in range(0, len(setlist)):
        listphi = setlist[i]
        dummy=copy.deepcopy(setlist)
        dummy.remove(listphi)
        for n in range(1, len(dummy)+1):
            for z in itertools.combinations(dummy, n):
                new=list(z)
                new.append(listphi)

                if (z == ()):
                    continue
                else:
                    intconf = (Training[new].eq(1.00).all(axis=1).sum()) / (Training[list(z)].eq(1.00).all(axis=1).sum())
                    if(intconf>minconf):

                        tuple=(z,listphi)
                        if tuple not in ruleslist:
                            if(len(z)+1==len(setlist)):
                                rulesitemset_tracker(tuple, len(setlist))

                            #if((str(listphi)=="goodForGroups_1")| (str(listphi)=="goodForGroups_0")):
                            #if(len(setlist)==4):
                                #print(setlist)
                                #print(str(z) + "->" + listphi)
                                #duplet=(setlist,intsup,str(z)+"->" + listphi,intconf)

                                #maxlist.append(duplet)


def freqitemset_tracker(sset):

    freqlist[len(sset)]=freqlist[len(sset)]+1

def rulesitemset_tracker(tuple,size):

    fruleslist[size]=fruleslist[size]+1
    ruleslist.append(tuple)

def subsetchecker(sset):
    if (len(sset) != 1):
        for k in range(0, len(reject_list)):
            if (set(reject_list[k]).issubset(sset)):
                return True

    return False

candidate_list = []
reject_list=[]
dummy_reject_list=[]
L = Training.columns

sset = ()
for n in range(1, len(L) + 1):
    flag = 0
    for sset in (itertools.combinations(L, n)):
        if (sset == ()):
            flag = 1
            continue

        if(subsetchecker(sset)):
            continue

        instsup = (Training[list(sset)].eq(1.00).all(axis=1).sum()) / Training.shape[0]

        if (instsup > minsup):
            list1 = list(sset)

            freqitemset_tracker(sset)
            #print("Set:"+str(list1))
            Rulecalcuator(list1,instsup)
            for i in range(len(list1)):
                if (candidate_list.count(list1[i]) <= 0):
                     candidate_list.append(list1[i])
        else:
            dummy_reject_list.append(sset)

    if (flag != 1):
        L = copy.deepcopy(candidate_list)
        candidate_list.clear()
        reject_list=copy.deepcopy(dummy_reject_list)
        dummy_reject_list.clear()
        #ruleslist.clear()
'''''''''
maxlist.sort(key=lambda tup: tup[1], reverse=True)

df = pd.DataFrame(maxlist, columns=['Original Set', 'Support', 'Rule','Confidence'])

pd.set_option('display.max_columns', None)
pd.options.display.max_colwidth = 80
print((df.iloc[:20]).to_string())
'''''
for i in range(2,len(freqlist)):
    if(freqlist[i]==0):
        continue

    print("FREQUENT - ITEMS " + str(i)+ " "+str(freqlist[i]))

for i in range(len(fruleslist)):
    if (fruleslist[i] == 0):
        continue

    print("ASSOCIATION-RULES " + str(i) + " " + str(fruleslist[i]))
