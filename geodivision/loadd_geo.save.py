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
    c_arr= '00' 
    c_qua=  '00'
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
                    line_of_commune = 0
                    if c_dep[1] == '9':
                        c_dep[0] = str(int(c_dep[0])+1)
                        c_dep[1] = '0' 

                    
                    c_dep[1] = str(int(c_dep[1])+1)
                    print("c_dep : {} ".format("".join(c_dep)))
                    #code = 0        # On réinistialise le code mairie
                    if decalage_code_commune >= 10:
                        code = code + 1

                    c_com = c_dep+c_com
                    print("c_com : {}".format("".join(c_com)))
                    
                    decalage_code_commune = 0
                    counter_dep += 1
                    word = " ".join(line[1:])

                    data['departement'].append({
                        "model": "geodivision.departement",
                        'pk': counter_dep,
                        "fields": {
                                    'c_dep': c_dep,
                                    'nom':"".join(line[1:])
                                    }
                        })
                elif re.match(r"COMMUNE", line[0]):
                    line_of_arron = 0

                    if line_of_commune >= 10:
                        decalage_code_commune += 1
#                        code = code + decalage_code_commune 
                        #decalage_code_commune = 0
                    code += 1 
                    line_of_bloc = 0
                    c_arr = 0   # On réinitialise le code arrondissement
                    if decalage_code_arron >= 10:
                        c_arr += 1
                    c_arr = int(str(code)+str(c_arr)) # On recompose le code arrondissement
                    decalage_code_arron = 0

                    counter_com += 1
                    commune = " ".join(line[1:])
                    data['mairie'].append({
                        "model": "geodivision.mairie",
                        'pk': counter_com,
                        "fields": {
                                    'code': code,
                                    'departement': c_dep,
                                    'nom':commune,
                                    'adresse':'',
                                    'is_default':'False'
                                    }
                        })

                elif re.match(r"ARROND", line[0]):
                    line_of_quartier = 0
                    decalage_code_quartier = 0
                    line_of_arron = 0
                    line_of_commune += 1
                    decalage_code_quartier = 0
                    line_of_quartier = 0

                    if line_of_arron >= 10:
                        decalage_code_arron += 1 

                    c_qua = 0   # On réinitialise le code quartier
                    #if len(str(c_arr)) >= 1:
                        #print("Code Arron avant composition : {}".format(str(c_arr)[1]))
                    c_qua = int(str(c_arr)+str(c_qua)) # On recompose le code quartier
                    #print("Code mairie  : {}  ---->  Code arrondissement : {}".format(code,c_arr))
                    counter_arron += 1
#                    word = line[1:]
                    arrondissement = " ".join(line[1:])
                    arron += 1
                    data['Arrondissement'].append({
                        "model": "geodivision.arrondissement",
                        'pk': counter_arron,
                        "fields": {
                                    'c_arr': c_arr,
                                    'mairie': code,
                                    'nom':arrondissement,
                                    'adresse':'',
                                    }
                        })
                    c_arr += 1

                else:
                    line_of_arron += 1
                    line_of_quartier += 1
                    if line_of_quartier >= 10:
                        decalage_code_quartier += 1
                        c_qua = c_qua + decalage_code_quartier 
                    #    decalage_code_quartier = 0
                    #    line_of_quartier = 0
                    #print("Commune :   {}  ------>  Arrondissement : {} ---->  Nbr quartier : {} ".format(commune,arrondissement,line_of_quartier ))
                    c_qua += 1
                    counter_qua += 1
                    data['quartier'].append({
                        "models": "geodivision.quartier",
                        'pk': counter_qua,
                        "fields": {
                                    'c_qua': c_qua,
                                    'arrondissement': c_arr,
                                    'nom':" ".join(line[1:]),
                                    'adresse':'',
                                    }
                        })

            else:
                    line_of_arron += 1
                    line_of_quartier += 1
                    if line_of_quartier >= 10:
                        decalage_code_quartier += 1
                        c_qua = c_qua + decalage_code_quartier 
                    #print("Commune :   {}  ------>  Arrondissement : {} ---->  Nbr quartier : {} ".format(commune,arrondissement,line_of_quartier ))
                    counter_qua += 1
                    data['quartier'].append({
                        "model": "geodivision.quartier",
                        'pk': counter_qua,
                        "fields": {
                                    'c_qua': c_qua,
                                    'arrondissement': c_arr,
                                    'nom':" ".join(line),
                                    'adresse':'',
                                    }
                        })
                    c_qua += 1

with open('data.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
