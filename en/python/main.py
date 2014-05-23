import requests
import json
import operator

MAX = 14000

services = {"tap": 'standardid:"ivo://ivoa.net/std/TAP"',
            "sia": 'standardid:"ivo://ivoa.net/std/SIA"',
            "ssa": 'standardid:"ivo://ivoa.net/std/SSA"',
            "scs": 'standardid:"ivo://ivoa.net/std/ConeSearch"'}
URL = "http://voparis-registry.obspm.fr/vo/ivoa/1/voresources/search"

# Publishers dictionary of publisher. Key value: [type][pub_name]
# Each publisher contains
# Amount: amount of services
# Wavebands: list of wavebands
publishers = {}
publishersWW = {}

# Subjects dictionary
subjects = {}
subjectsDetails = {}

# Wavebands
wavebands = {}

# Try - Excepts counters
counter_1 = 0
counter_2 = 0

# Amount of type of resources
resources = {}
resources["tap"] = 0
resources["sia"] = 0
resources["ssa"] = 0
resources["scs"] = 0

# Try - Except by type
t = {}
t["tap"] = {"publisher":0, "waveband":0, "subjects":0}
t["sia"] = {"publisher":0, "waveband":0, "subjects":0}
t["scs"] = {"publisher":0, "waveband":0, "subjects":0}
t["ssa"] = {"publisher":0, "waveband":0, "subjects":0}

e = {}
e["tap"] = {"publisher":0, "waveband":0, "subjects":0}
e["sia"] = {"publisher":0, "waveband":0, "subjects":0}
e["scs"] = {"publisher":0, "waveband":0, "subjects":0}
e["ssa"] = {"publisher":0, "waveband":0, "subjects":0}

for types in services:
    parameters = {"keywords": services[types], "max": MAX}
    r = requests.get(URL, params=parameters)
    entries = json.loads(r.content)['resources']

    publishers[types] = {}
    publishersWW[types] = {}
    wavebands[types] = []

    for i in entries:
        resources[types] += 1
        # Creating an entry in publisher dictionary
        try:
            pub = i["publisher"]
            if(not (pub in publishers[types])):
                publishers[types][pub] = {}
                publishers[types][pub]["amount"] = 1
                publishers[types][pub]["wavebands"] = []

                publishersWW[types][pub] = {}
                publishersWW[types][pub]["amount"] = 1
                publishersWW[types][pub]["wavebands"] = []

            else:
                publishers[types][pub]["amount"] += 1
                publishersWW[types][pub]["amount"] += 1
            t[types]["publisher"] += 1 
        except:
            e[types]["publisher"] += 1 

        # Adding wavebands atribute
        try:
            wb = i["waveband"]
            for w in wb:
                if(not (w in publishers[types][pub]["wavebands"])):
                    publishers[types][pub]["wavebands"].append(w)
                if(not (w in wavebands[types])):
                    wavebands[types].append(w)
                if(not (w in publishersWW[types][pub]["wavebands"])):
                    publishersWW[types][pub]["wavebands"].append(w)
            t[types]["waveband"] += 1 
        except:
            if(pub in publishersWW[types]):
                if(publishersWW[types][pub]["amount"] > 1):
                    publishersWW[types][pub]["amount"] -= 1
                else:
                    if(pub in publishersWW[types]):
                        del publishersWW[types][pub]
                e[types]["waveband"] += 1
            else:
                pass
                #print "No key in publishersWW[types]"
        
        # Adding subjects
        try:
            for sb in i["subjects"]:
                if(not (sb in subjects)):
                    subjects[sb] = 1
                    subjectsDetails[sb] = {}
                    try:
                        for wb in i["waveband"]:
                            subjectsDetails[sb][wb] = 1
                    except:
                        pass
                        #print "Problems in if"
                else:
                    subjects[sb] += 1
                    try:
                        for wb in i["waveband"]:
                            subjectsDetails[sb][wb] += 1
                    except:
                        pass
                        #print "Problems in else"
            t[types]["subjects"] += 1
        except:
            e[types]["subjects"] += 1

# Complete list of publishers
others = 0
print "##################################################"
print "Publishers complete list"
for i in publishers:
    print "##################################################"
    print "Elements in publishers[", i, "]"
    for j in publishers[i]:
        if i == "scs":
            if publishers[i][j]["amount"] >= 100:
                print "Publisher: ", j.encode('ascii', 'ignore'), " ", publishers[i][j]
            else:
                others += publishers[i][j]["amount"]      
        else:
            print "Publisher: ", j.encode('ascii', 'ignore'), " ", publishers[i][j]
    print ""
print "Others publishers[scs]: ", others
print ""

others = 0
# Publishers without wavebands
print "##################################################"
print "Publishers with wavebands"
for i in publishersWW:
    print "##################################################"
    print "Elements in publishers[", i, "]"
    for j in publishersWW[i]:
        if i == "scs":
            if publishersWW[i][j]["amount"] >= 100:
                print "Publisher: ", j.encode('ascii', 'ignore'), publishersWW[i][j]
            else:
                others += publishersWW[i][j]["amount"]      
        else:
            print "Publisher: ", j.encode('ascii', 'ignore'), publishersWW[i][j]
    print ""
print "Others publishers[scs]: ", others
print ""

# Try and Except by types
print "##################################################"
for i in t:
    for j in t[i]:
        print "Type: ", i, " ", j, " Try: ", t[i][j], " Except: ", e[i][j]
print ""

# Waveband resume
print "##################################################"
print "Waveband resume per each type of resource"
for i in wavebands:
    waves = ''
    for j in wavebands[i]:
        waves +=  j + " "
    print "Wavebands & ", i, " & ", waves, " \\\\"
print ""

print "##################################################"
print "Ranking by subjects (from all type of resources)"
ranking = sorted(subjects.iteritems(), key=operator.itemgetter(1))
ranking = ranking[::-1]
top = 0
s_total = 0
s_types = 0
for i in ranking:
    top += 1
    if top < 10:
        print "Subject: & ", i[0], " & ", i[1], " \\\\"
    else:
        s_types += 1
        s_total += i[1]
print "Others subjects types: & ", s_types, " & total amount: ", s_total, " \\\\"
print ""

print "##################################################"
top = 0
for sb in subjectsDetails:
    print "Subject: ", sb
    for wb in subjectsDetails[sb]:
        print "\t", wb, ": ", subjectsDetails[sb][wb]
print ""

# There are subjects without wavebands details, so it's not possible 
# to cross the information of the subjectsDetails with the ranking
# print "##################################################"
# print "Details of ranked subjects"
# for i in ranking:
#     print "Subject: ", i
#     for wb in subjectsDetails[i[0]]:
#         print "\t", wb, " total: ", subjectsDetails[sb][wb]
# print ""

print "##################################################"
print "Ranking by amount of type of resources"
ranking = sorted(resources.iteritems(), key=operator.itemgetter(1))
ranking = ranking[::-1]
for i in ranking:
    print "Resource: & ", i[0], " & ", i[1], " \\\\"
