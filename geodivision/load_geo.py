import re
import json

data = {}
data['departement']= []
data['mairie']= []
data['Arrondissement']= []
data['quartier'] = []

with open('test_dep.csv', encoding = "ISO-8859-1") as f:
    c_dep = list("00")
    c_com = list('00')
    c_arr= list('00')
    c_qua=  list('00')
    arron = 0
    counter_dep = 0
    counter_com = 0
    counter_arron = 0
    counter_qua = 0
    decalage_code_commune = 0
    decalage_code_arron = 0

    for line in f:
        if not line.isspace():
            line = line.split()
            if len(line) > 1:
                if re.match(r"DEPT", line[0]):  # On enregistre le département
                    c_com = list('00')
                    #line_of_commune = 0
                    if c_dep[1] == '9':
                        c_dep[0] = str(int(c_dep[0])+1)
                        c_dep[1] = '0' 
                    else:
                        c_dep[1] = str(int(c_dep[1])+1)

                    c_com = c_dep+c_com                                 # Initialisation du code commune
                    counter_dep += 1
                    word = " ".join(line[1:])
                    data['departement'].append({
                        "model": "geodivision.departement",
                        'pk': counter_dep,
                        "fields": {
                                    'c_dep': "".join(c_dep),
                                    'nom':"".join(line[1:])
                                    }
                        })
                elif re.match(r"COMMUNE", line[0]):
                    c_arr = list('00')
                    if c_com[3] == '9':
                        c_com[2] = str(int(c_com[2])+1)
                        c_com[3] = '0' 
                    else:
                        c_com[3] = str(int(c_com[3])+1)
                    
                    c_arr = c_com+c_arr                      # On recompose le code arrondissement
                    counter_com += 1
                    commune = " ".join(line[1:])
                    data['mairie'].append({
                        "model": "geodivision.mairie",
                        'pk': counter_com,
                        "fields": {
                                    'c_com': "".join(c_com),
                                    'departement': counter_dep,
                                    'nom':commune,
                                    'adresse': 'null',
                                    'is_default': 'false'
                                    }
                        })

                elif re.match(r"ARROND", line[0]):
                    c_qua = list('00')
                    if c_arr[5] == '9':
                        c_arr[4] = str(int(c_arr[4])+1)
                        c_arr[5] = '0' 
                    else:
                        c_arr[5] =  str(int(c_arr[5])+1)

                    counter_arron += 1
                    c_qua = c_arr+c_qua                      # On recompose le code arrondissement
                    arrondissement = " ".join(line[1:])
                    data['Arrondissement'].append({
                        "model": "geodivision.arrondissement",
                        'pk': counter_arron,
                        "fields": {
                                    'c_arr': "".join(c_arr),
                                    'mairie': counter_com,
                                    'nom':arrondissement,
                                    'adresse': 'null'
                                    }
                        })


                else:
                    if c_qua[7] == '9':
                        c_qua[6] = str(int(c_qua[6])+1)
                        c_qua[7] = '0' 
                    else:
                        c_qua[7] = str(int(c_qua[7])+1)

                    if c_qua[7] == '9' and c_qua[6] == 9:
                        c_qua[5] = str(int(c_qua(5)+1))
                        c_qua[6] = c_qua[7]=0

                    if len("".join(line)) >= 30:
                        print("Le quartier : {} ----->  Longueur : {} ".format("".join(line), len("".join(line[1:]))))
                    counter_qua += 1
                    data['quartier'].append({
                        "model": "geodivision.quartier",
                        'pk': counter_qua,
                        "fields": {
                                    'c_qua': "".join(c_qua),
                                    'arrondissement': counter_arron,
                                    'nom':" ".join(line[0:]),
                                    'adresse': 'null'
                                    }
                        })

            else:
                    if c_qua[7] == '9':
                        c_qua[6] = str(int(c_qua[6])+1)
                        c_qua[7] = '0' 
                    else:
                        c_qua[7] = str(int(c_qua[7])+1)

                    if c_qua[7] == '9' and c_qua[6] == 9:
                        c_qua[5] = str(int(c_arr(5)+1))
                        c_qua[6]=c_qua[7]=0

                    counter_qua += 1
                    if len("".join(line)) >= 30:
                        print("Le quartier : {} ----->  Longueur : {} ".format("".join(line), len("".join(line))))
                    data['quartier'].append({
                        "model": "geodivision.quartier",
                        'pk': counter_qua,
                        "fields": {
                                    'c_qua': "".join(c_qua),
                                    'arrondissement': counter_arron,
                                    'nom':" ".join(line[0:]),
                                    'adresse': 'null'
                                    }
                        })
                    #c_qua += 1

with open('data.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
