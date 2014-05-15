import requests
import json
import operator

MAX = 1000000

services = {"tap": 'standardid:"ivo://ivoa.net/std/TAP"',
            "sia": 'standardid:"ivo://ivoa.net/std/SIA"',
            "ssa": 'standardid:"ivo://ivoa.net/std/SSA"',
            "scs": 'standardid:"ivo://ivoa.net/std/ConeSearch"'}
URL = "http://voparis-registry.obspm.fr/vo/ivoa/1/voresources/search"

# Publishers diccionario de publisher. La key es type:nombre
# Cada publisher contiene
# Amount: cantidad de servicios
# Wavebands: lista con wavebands
publishers = {}

# Subjects dictionary
subjects = {}

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

for types in services:
    parameters = {"keywords": services[types], "max": MAX}
    r = requests.get(URL, params=parameters)
    entries = json.loads(r.content)['resources']

    publishers[types] = {}
    wavebands[types] = []

    for i in entries:
        resources[types] += 1
        try:
            pub = i["publisher"]
            if(not (pub in publishers[types])):
                publishers[types][pub] = {}
                publishers[types][pub]["amount"] = 1
                publishers[types][pub]["wavebands"] = []
            else:
                publishers[types][pub]["amount"] += 1

            wb = i["waveband"]
            for w in wb:
                if(not (w in publishers[types][pub]["wavebands"])):
                    publishers[types][pub]["wavebands"].append(w)
                if(not (w in wavebands[types])):
                    wavebands[types].append(w)

            counter_1 += 1
        except:
            # print "No trae esos parametros"
            counter_2 += 1

        try:
            for sb in i["subjects"]:
                if(not (sb in subjects)):
                    subjects[sb] = 1
                else:
                    subjects[sb] += 1
        except:
            pass

for i in publishers:
    print "##################################################"
    print "Elements in publishers[", i, "]"
    for j in publishers[i]:
        print "Publisher: ", j, publishers[i][j]
    print ""


print "##################################################"
print "Try: ", counter_1, " Except: ", counter_2
print ""

print "##################################################"
print "Waveband resume per each type of resource"
for i in wavebands:
    print "Wavebands in: ", i, " ", wavebands[i]
print ""

print "##################################################"
print "Ranking by subjects (from all type of resources)"
ranking = sorted(subjects.iteritems(), key=operator.itemgetter(1))
ranking = ranking[::-1]
for i in ranking:
    print "Subject: ", i[0], " ", i[1]
print ""

print "##################################################"
print "Ranking by amount of type of resources"
ranking = sorted(resources.iteritems(), key=operator.itemgetter(1))
ranking = ranking[::-1]
for i in ranking:
    print "Resource: ", i[0], " ", i[1]
