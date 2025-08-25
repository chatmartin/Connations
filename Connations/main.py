from country import *
import csv
import random,datetime
from flask import Flask,jsonify,request,render_template

def file_read():
    country_dict = {}
    color_dict = {}
    lang_dict = {}
    relig_dict = {}
    region_dict = {}
    num_border_dict = {}
    country_list = []

    with open('bb/country_data.csv', newline='') as csvfile:
        info = csv.reader(csvfile, delimiter=',')
        next(info)
        for row in info:
            color_list = []
            ind = 0
            while ind < len(row[1]) and ind != -1:
                try:
                    ind2 = row[1].index(' ',ind)
                except ValueError:
                    ind2 = -1
                if ind2 != -1:
                    color_list.append(row[1][ind:ind2])
                else:
                    color_list.append(row[1][ind:])
                ind = ind2
                if ind != -1:
                    ind += 1
            ind = 0
            border_list = []
            while ind < len(row[4]) and ind != -1:
                try:
                    ind2 = row[4].index('/', ind)
                except ValueError:
                    ind2 = -1
                if ind2 != -1:
                    border_list.append(row[4][ind:ind2])
                else:
                    border_list.append(row[4][ind:])
                ind = ind2
                if ind != -1:
                    ind += 1
            ind = 0
            lang_list = []
            while ind < len(row[5]) and ind != -1:
                try:
                    ind2 = row[5].index(' ', ind)
                except ValueError:
                    ind2 = -1
                if ind2 != -1:
                    lang_list.append(row[5][ind:ind2])
                else:
                    lang_list.append(row[5][ind:])
                ind = ind2
                if ind != -1:
                    ind += 1

            country = Country(row[0],color_list,row[2]=='Y',row[3]=='Y',border_list,lang_list,row[6]=='Y',row[7]=='Y',row[8]=='Y',row[9]=='Y',row[10]=='Y',row[11]=='Y',row[12]=='Y',row[13]=='Y',row[14]=='Y',row[15]=='Y',row[16]=='Y',row[17]=='Y',row[18]=='Y',row[19]=='N',row[20],row[21]=='Y',row[22])
            country_dict[row[0]] = country
            #color dictionary setup
            for col in color_list:
                if col not in color_dict:
                    color_dict[col]=[]
                    color_dict[col].append(row[0])
                else:
                    color_dict[col].append(row[0])
            #language dictionary setup
            for lang in lang_list:
                if lang not in lang_dict:
                    lang_dict[lang]=[]
                    lang_dict[lang].append(row[0])
                else:
                    lang_dict[lang].append(row[0])
            #religion dictionary setup
            if row[20] not in relig_dict:
                relig_dict[row[20]]=[]
                relig_dict[row[20]].append(row[0])
            else:
                relig_dict[row[20]].append(row[0])
            #region dictionary setup
            if row[22] not in region_dict:
                region_dict[row[22]]=[]
                region_dict[row[22]].append(row[0])
            else:
                region_dict[row[22]].append(row[0])
            #country list setup
            country_list.append(row[0])

            if len(border_list) not in num_border_dict:
                num_border_dict[len(border_list)]=[]
                num_border_dict[len(border_list)].append(row[0])
            else:
                num_border_dict[len(border_list)].append(row[0])

    big_list = [country_dict, color_dict, lang_dict, relig_dict, region_dict, num_border_dict, country_list]
    return big_list

def check_group1(country_dict:dict,group1:list,other:list):
    reason1 = group1[4]
    spec1 = group1[5]
    if reason1 == 'Borders X Country':
        for i in range(len(other)-2):
            if spec1 in country_dict[other[i]].borders:
                return False
    elif reason1 == 'Borders n Countries':
        for i in range(len(other)-2):
            if spec1 == len(country_dict[other[i]].borders):
                return False
    else:
        for i in range(len(other)-2):
            if spec1 == country_dict[other[i]].region:
                return False
    return True

def check_group2(country_dict:dict,group2:list,other:list):
    reason2 = group2[4]
    spec2 = group2[5]
    if reason2 == 'Flag 3 Color':
        ind1 = spec2.index(' ')
        ind2 = spec2.index('/')
        col1 = spec2[:ind1]
        col2 = spec2[ind1+1:ind2]
        col3 = spec2[ind2+1:]
        for i in range(len(other)-2):
            if col1 in country_dict[other[i]].flag_color and col2 in country_dict[other[i]].flag_color and col3 in country_dict[other[i]].flag_color:
                return False
    elif reason2 == 'Flag Color':
        ind = spec2.index(' ')
        col1= spec2[0:ind]
        col2= spec2[ind+1:]
        for i in range(len(other)-2):
            if col1 in country_dict[other[i]].flag_color and col2 in country_dict[other[i]].flag_color:
                return False
    elif reason2 == 'Star':
        for i in range(len(other)-2):
            if country_dict[other[i]].star:
                return False
    elif reason2 == 'Coat of Arms':
        for i in range(len(other)-2):
            if country_dict[other[i]].coat_of_arms:
                return False
    elif reason2 == 'Language':
        for i in range(len(other)-2):
            if spec2 in country_dict[other[i]].official_lang:
                return False
    else:
        for i in range(len(other)-2):
            if spec2 == country_dict[other[i]].maj_relig:
                return False
    return True

def check_group3(country_dict:dict,group3:list,other:list):
    reason3 = group3[4]
    spec3 = group3[5]
    if reason3 == 'Island':
        for i in range(len(other) - 2):
            if country_dict[other[i]].island:
                return False
    elif reason3 == 'Landlocked':
        for i in range(len(other) - 2):
            if country_dict[other[i]].landlocked:
                return False
    elif reason3 == 'Multiple Timezones':
        for i in range(len(other) - 2):
            if country_dict[other[i]].mult_timezones:
                return False
    elif reason3 == "Capital not most pop":
        for i in range(len(other) - 2):
            if country_dict[other[i]].cap_pop:
                return False
    elif reason3 == "Borders X Country":
        for i in range(len(other)-2):
            if spec3 in country_dict[other[i]].borders:
                return False
    else:
        for i in range(len(other)-2):
            if spec3 == country_dict[other[i]].region:
                return False
    return True

def check_group4(country_dict:dict,group4:list,other:list):
    reason4 = group4[4]
    if reason4 == 'GDP':
        for i in range(len(other)-2):
            if country_dict[other[i]].gdp:
                return False
    elif reason4 == 'Population':
        for i in range(len(other)-2):
            if country_dict[other[i]].pop:
                return False
    elif reason4 == 'World Cup Host':
        for i in range(len(other)-2):
            if country_dict[other[i]].cup_host:
                return False
    elif reason4 == 'Olympics Host':
        for i in range(len(other)-2):
            if country_dict[other[i]].olympic_host:
                return False
    elif reason4 == 'European Union Member':
        for i in range(len(other)-2):
            if country_dict[other[i]].european_union:
                return False
    elif reason4 == 'Former Soviet State':
        for i in range(len(other)-2):
            if country_dict[other[i]].ussr:
                return False
    elif reason4 ==  'Commonwealth Member':
        for i in range(len(other)-2):
            if country_dict[other[i]].commonwealth:
                return False
    elif reason4 == 'BRICS+ Member or Partner':
        for i in range(len(other)-2):
            if country_dict[other[i]].brics:
                return False
    elif reason4 == 'Monarchy':
        for i in range(len(other)-2):
            if country_dict[other[i]].monarchy:
                return False
    else:
        for i in range(len(other)-2):
            if country_dict[other[i]].left_side:
                return False
    return True

def check_compatibility(country_dict:dict, group1:list, group2:list, group3=None, group4=None):
    a1 = check_group1(country_dict, group1, group2)
    a2 = check_group2(country_dict, group2, group1)
    if group3 is None:
        return a1 and a2
    a3 = check_group1(country_dict, group1, group3)
    a4 = check_group2(country_dict, group2, group3)
    a5 = check_group3(country_dict, group3, group1)
    a6 = check_group3(country_dict, group3, group2)
    if group4 is None:
        return a1 and a2 and a3 and a4 and a5 and a6
    a7 = check_group1(country_dict, group1, group4)
    a8 = check_group2(country_dict, group2, group4)
    a9 = check_group3(country_dict, group3, group4)
    a10 = check_group4(country_dict, group4, group1)
    a11 = check_group4(country_dict, group4, group2)
    a12 = check_group4(country_dict, group4, group3)
    return a1 and a2 and a3 and a4 and a5 and a6 and a7 and a8 and a9 and a10 and a11 and a12


def gen_group_1(cat1:int,country_list:list,country_dict:dict,num_border_dict:dict,region_dict:dict):
    group1 = []
    if cat1 < 125:
        country_ind = random.randrange(0,len(country_list))
        while len(country_dict[country_list[country_ind]].borders) < 4:
            country_ind = random.randrange(0,len(country_list))
        border_list = country_dict[country_list[country_ind]].borders
        count = 0
        while count < 4:
            ind = random.randrange(0,len(border_list))
            if border_list[ind] not in group1:
                group1.append(border_list[ind])
                count+=1
        group1.append('Borders X Country')
        group1.append(country_list[country_ind])
    elif cat1 < 175:
        key_list = list(num_border_dict.keys())
        random_num = random.choice(key_list)
        while len(num_border_dict[random_num])<4:
            random_num = random.choice(key_list)
        count = 0
        while count < 4:
            nat = random.choice(num_border_dict[random_num])
            if nat not in group1:
                group1.append(nat)
                count+=1
        group1.append('Borders n Countries')
        group1.append(random_num)
    else:
        key_list = list(region_dict.keys())
        random_reg = random.choice(key_list)
        while len(region_dict[random_reg])<4:
            random_reg = random.choice(key_list)
        count = 0
        while count < 4:
            nat = random.choice(region_dict[random_reg])
            if nat not in group1:
                group1.append(nat)
                count+=1
        group1.append('In X Region')
        group1.append(random_reg)
    return group1

def gen_group_2(cat2:int,country_dict:dict,color_dict:dict,lang_dict:dict,relig_dict:dict):
    group2 = []
    if cat2 < 300:
        key_list = list(color_dict.keys())
        random_color = random.choice(key_list)
        random_color2 = random.choice(key_list)
        random_color3 = random.choice(key_list)
        while len(set(color_dict[random_color]) & set(color_dict[random_color2]) & set(color_dict[random_color3])) < 4 or random_color == random_color2 or random_color == random_color3 or random_color2 == random_color3 or random_color == 'Gray' or random_color2 == 'Gray' or random_color3 == 'Gray':
            random_color = random.choice(key_list)
            random_color2 = random.choice(key_list)
            random_color3 = random.choice(key_list)
        count = 0
        while count < 4:
            nat = random.choice(list(set(color_dict[random_color]) & set(color_dict[random_color2]) & set(color_dict[random_color3])))
            if nat not in group2:
                group2.append(nat)
                count += 1
        group2.append('Flag 3 Color')
        group2.append(random_color + ' ' + random_color2 + '/' + random_color3)
    elif cat2 < 600:
        key_list = list(color_dict.keys())
        random_color = random.choice(key_list)
        random_color2 = random.choice(key_list)
        while len(set(color_dict[random_color])&set(color_dict[random_color2]))<4 or random_color == random_color2 or random_color == 'Gray' or random_color2 == 'Gray':
            random_color = random.choice(key_list)
            random_color2 = random.choice(key_list)
        count = 0
        while count < 4:
            nat = random.choice(list(set(color_dict[random_color])&set(color_dict[random_color2])))
            if nat not in group2:
                group2.append(nat)
                count+=1
        group2.append('Flag Color')
        group2.append(random_color+' '+random_color2)
    elif cat2 < 800:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group2 and country_dict[nat].star:
                group2.append(nat)
                count+=1
        group2.append('Star')
        group2.append('Star')
    elif cat2 < 900:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group2 and country_dict[nat].coat_of_arms:
                group2.append(nat)
                count+=1
        group2.append('Coat of Arms')
        group2.append('Coat of Arms')
    elif cat2 < 1100:
        key_list = list(lang_dict.keys())
        random_lang = random.choice(key_list)
        while len(lang_dict[random_lang])<4:
            random_lang = random.choice(key_list)
        count = 0
        while count < 4:
            nat = random.choice(lang_dict[random_lang])
            if nat not in group2:
                group2.append(nat)
                count+=1
        group2.append('Language')
        group2.append(random_lang)
    else:
        key_list = list(relig_dict.keys())
        random_relig = random.choice(key_list)
        while len(relig_dict[random_relig])<4:
            random_relig = random.choice(key_list)
        count = 0
        while count < 4:
            nat = random.choice(relig_dict[random_relig])
            if nat not in group2:
                group2.append(nat)
                count+=1
        group2.append('Religion')
        group2.append(random_relig)
    return group2

def gen_group_3(cat3:int,country_dict:dict,region_dict:dict):
    group3 = []
    if cat3 < 100:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group3 and country_dict[nat].island:
                group3.append(nat)
                count+=1
        group3.append('Island')
        group3.append('Island')
    elif cat3 < 200:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group3 and country_dict[nat].landlocked:
                group3.append(nat)
                count+=1
        group3.append('Landlocked')
        group3.append('Landlocked')
    elif cat3 < 300:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group3 and country_dict[nat].mult_timezones:
                group3.append(nat)
                count+=1
        group3.append('Multiple Timezones')
        group3.append('Multiple Timezones')
    elif cat3 < 400:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group3 and country_dict[nat].cap_pop:
                group3.append(nat)
                count+=1
        group3.append('Capital not most pop')
        group3.append('Capital not most pop')
    elif cat3 < 500:
        key_list = list(country_dict.keys())
        rand_nat = random.choice(key_list)
        while len(country_dict[rand_nat].borders)<4:
            rand_nat = random.choice(key_list)
        count = 0
        while count < 4:
            nat = random.choice(country_dict[rand_nat].borders)
            if nat not in group3:
                group3.append(nat)
                count+=1
        group3.append('Borders X Country')
        group3.append(rand_nat)
    else:
        key_list = list(region_dict.keys())
        rand_region = random.choice(key_list)
        while len(region_dict[rand_region])<4:
            rand_region = random.choice(key_list)
        count = 0
        while count < 4:
            nat = random.choice(region_dict[rand_region])
            if nat not in group3:
                group3.append(nat)
                count+=1
        group3.append('In X Region')
        group3.append(rand_region)
    return group3

def gen_group_4(cat4:int,country_dict:dict):
    group4 = []
    if cat4 < 110:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group4 and country_dict[nat].gdp:
                group4.append(nat)
                count+=1
        group4.append('GDP')
        group4.append('GDP')
    elif cat4 < 200:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group4 and country_dict[nat].pop:
                group4.append(nat)
                count+=1
        group4.append('Population')
        group4.append('Population')
    elif cat4 < 300:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group4 and country_dict[nat].cup_host:
                group4.append(nat)
                count+=1
        group4.append('World Cup Host')
        group4.append('World Cup Host')
    elif cat4 < 425:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group4 and country_dict[nat].olympic_host:
                group4.append(nat)
                count+=1
        group4.append('Olympics Host')
        group4.append('Olympics Host')
    elif cat4 < 550:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group4 and country_dict[nat].european_union:
                group4.append(nat)
                count+=1
        group4.append('European Union Member')
        group4.append('European Union Member')
    elif cat4 < 625:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group4 and country_dict[nat].ussr:
                group4.append(nat)
                count+=1
        group4.append('Former Soviet State')
        group4.append('Former Soviet State')
    elif cat4 < 750:
        key_list = list(country_dict.keys())
        count=0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group4 and country_dict[nat].commonwealth:
                group4.append(nat)
                count+=1
        group4.append('Commonwealth Member')
        group4.append('Commonwealth Member')
    elif cat4 < 850:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group4 and country_dict[nat].brics:
                group4.append(nat)
                count+=1
        group4.append('BRICS+ Member or Partner')
        group4.append('BRICS+ Member or Partner')
    elif cat4 < 975:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group4 and country_dict[nat].monarchy:
                group4.append(nat)
                count+=1
        group4.append('Monarchy')
        group4.append('Monarchy')
    else:
        key_list = list(country_dict.keys())
        count = 0
        while count < 4:
            nat = random.choice(key_list)
            if nat not in group4 and country_dict[nat].left_side:
                group4.append(nat)
                count+=1
        group4.append('Left Side Driver')
        group4.append('Left Side Driver')

    return group4

def create_groups():
    info = file_read()
    cat1 = random.randrange(0,
                            300)  # if x<125 then borders x country, if 125<=x<175 then borders n countries, if 175<=x then region
    cat2 = random.randrange(0,
                            1200)  # if x<300 then 3 colors, if 300<=x<600 then 2 colors, if 600<=x<800 then star, if 800<=x<900 then coat of arms, if 900<=x<1100 then language, if 1100<=x then religion
    cat3 = random.randrange(0,
                            600)  # if x<100 then island, if 100<=x<200 then landlocked, if 200<=x<300 then timezone, if 300<=x<400 then capital, if 400<=x<500 then borders x country, if 500<=x then region
    cat4 = random.randrange(0,
                            1100)  # if x<110 then GDP, if 110<=x<200 then population, if 200<=x<300 then world cup, if 300<=x<425 then olympics, if 425<=x<550 then EU, if 550<=x<625 then USSR, if 625<=x<750 then Commonwealth, if 750<=x<850 then BRICS, if 850<=x<975 then monarchy, if 975<=x then left side driving
    country_dict = info[0]
    color_dict = info[1]
    lang_dict = info[2]
    relig_dict = info[3]
    region_dict = info[4]
    num_border_dict = info[5]
    country_list = info[6]
    group1 = gen_group_1(cat1, country_list, country_dict, num_border_dict, region_dict)
    group2 = gen_group_2(cat2, country_dict, color_dict, lang_dict, relig_dict)
    while not check_compatibility(country_dict, group1, group2):
        cat1 = random.randrange(0, 300)
        cat2 = random.randrange(0, 1200)
        group1 = gen_group_1(cat1, country_list, country_dict, num_border_dict, region_dict)
        group2 = gen_group_2(cat2, country_dict, color_dict, lang_dict, relig_dict)

    group3 = gen_group_3(cat3, country_dict, region_dict)
    while not check_compatibility(country_dict, group1, group2, group3):
        cat1 = random.randrange(0, 300)
        cat2 = random.randrange(0, 1200)
        cat3 = random.randrange(0, 600)
        group1 = gen_group_1(cat1, country_list, country_dict, num_border_dict, region_dict)
        group2 = gen_group_2(cat2, country_dict, color_dict, lang_dict, relig_dict)
        group3 = gen_group_3(cat3, country_dict, region_dict)

    group4 = gen_group_4(cat4, country_dict)
    while not check_compatibility(country_dict, group1, group2, group3, group4):
        cat1 = random.randrange(0, 300)
        cat2 = random.randrange(0, 1200)
        cat3 = random.randrange(0, 600)
        cat4 = random.randrange(0, 1100)
        group1 = gen_group_1(cat1, country_list, country_dict, num_border_dict, region_dict)
        group2 = gen_group_2(cat2, country_dict, color_dict, lang_dict, relig_dict)
        group3 = gen_group_3(cat3, country_dict, region_dict)
        group4 = gen_group_4(cat4, country_dict)

    if (group1[4] == 'Borders X Country'):
        reason1 = 'Borders ' + group1[5]
    elif (group1[4] == 'Borders n Countries'):
        reason1 = 'Borders ' + str(group1[5]) + ' Countries'
    else:
        reason1 = 'In the ' + group1[5] + ' Region'

    reason2 = ''
    if group2[4] == 'Flag 3 Color':
        ind = group2[5].index(' ')
        ind2 = group2[5].index('/')
        reason2 = 'Flags with the Colors ' + group2[5][:ind] + ', ' + group2[5][ind + 1:ind2] + ', and ' + group2[5][
                                                                                                           ind2 + 1:]
    elif group2[4] == 'Flag Color':
        ind = group2[5].index(' ')
        reason2 = 'Flags with the Colors ' + group2[5][:ind] + ' and ' + group2[5][ind + 1:]
    elif group2[4] == 'Star':
        reason2 = 'Flag has a Star or Sun'
    elif group2[4] == "Coat of Arms":
        reason2 = "Flag has a Coat of Arms"
    elif group2[4] == "Language":
        reason2 = group2[5] + ' is an Official (or de facto) Language'
    elif group2[4] == 'Religion':
        if group2[5] == 'No Majority':
            reason2 = 'No majority religion'
        elif group2[5] == 'Non-Religious':
            reason2 = 'Majority Non-Religious Population'
        else:
            reason2 = 'Majority Religion is ' + group2[5]

    if group3[4] == 'Island':
        reason3 = 'Island Nations'
    elif group3[4] == 'Landlocked':
        reason3 = 'Landlocked Countries'
    elif group3[4] == 'Multiple Timezones':
        reason3 = 'Countries with Multiple Timezones'
    elif group3[4] == 'Capital not most pop':
        reason3 = 'Capital is Not the Most Populated City'
    elif group3[4] == 'Borders X Country':
        reason3 = 'Borders ' + group3[5]
    else:
        reason3 = 'In the ' + group3[5] + ' Region'

    if group4[4] == 'GDP':
        reason4 = 'GDP is Over $1 Trillion'
    elif group4[4] == 'Population':
        reason4 = 'Population is Over 100 Million People'
    elif group4[4] == 'World Cup Host':
        reason4 = 'World Cup Hosts'
    elif group4[4] == 'Olympics Host':
        reason4 = 'Hosted the Olympics'
    elif group4[4] == 'European Union Member':
        reason4 = group4[5] + 's'
    elif group4[4] == 'Former Soviet State':
        reason4 = 'Former or Current Communist State'
    elif group4[4] == 'Commonwealth Member':
        reason4 = group4[5] + 's'
    elif group4[4] == 'BRICS+ Member or Partner':
        reason4 = 'BRICS Member or Partner'
    elif group4[4] == 'Monarchy':
        reason4 = 'Monarchies'
    else:
        reason4 = 'Drives on the Left'

    return [{"reason":reason1, "countries":group1[0:4], "color":'#48A2F7'},
           {"reason":reason2, "countries":group2[0:4], "color":'#06AA0F'},
           {"reason":reason3, "countries":group3[0:4], "color":'#E7D10A'},
           {"reason":reason4, "countries":group4[0:4], "color":'#DD3E32'}]

def generate_board(seed=None):
    random.seed(seed)
    groups = create_groups()
    countries = [country for group in groups for country in group["countries"]]
    random.shuffle(countries)
    return {
        "groups": groups,
        "tiles": countries,
        "tries": 4
    }

def create_app():
    app = Flask(__name__, template_folder="templates",static_folder="static")

    groups = create_groups()

    tries = {"value":4}

    @app.route('/',methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/init", methods=["GET"])
    def init():
        countries = [country for group in groups for country in group["countries"]]
        random.shuffle(countries)
        return jsonify({"tiles": countries, "tries":tries["value"]})

    @app.route("/check", methods=["POST"])
    def check_guess():
        data = request.get_json()
        guess = data.get("guess",[])
        m=0
        for group in groups:
            if sorted(guess) == sorted(group["countries"]):
                if group == groups[0]:
                    res = ['B','B','B','B']
                elif group == groups[1]:
                    res = ['G','G','G','G']
                elif group == groups[2]:
                    res = ['Y','Y','Y','Y']
                else:
                    res = ['R','R','R','R']
                return jsonify({
                    "correct":2,
                    "reason":group["reason"],
                    "color":group["color"],
                    "tries":tries["value"],
                    "result":res
                })
            else:
                n = 0
                for country in group["countries"]:
                    if country in guess:
                        n+=1
                if n > m:
                    m = n

        tries["value"] -= 1
        res = []
        for country in guess:
            if country in groups[0]["countries"]:
                res.append('B')
            elif country in groups[1]["countries"]:
                res.append('G')
            elif country in groups[2]["countries"]:
                res.append('Y')
            else:
                res.append('R')
        if m == 3:
            return jsonify({"correct": 1, "tries": tries["value"], "result":res})
        return jsonify({"correct":0,"tries":tries["value"], "result":res})

    @app.route("/loss",methods={"GET"})
    def pass_groups():
        return jsonify({"groups":groups})

    @app.route("/new")
    def new_board():
        tries["value"] = 4
        new_groups = create_groups()
        for i in range(len(groups)):
            groups[i] = new_groups[i]
        return

    @app.route("/daily")
    def daily():
        today = datetime.date.today().isoformat()
        return jsonify(generate_board(seed=today))

    return app

def main():
    app = create_app()
    app.run(debug=True)




if __name__ == '__main__':
    main()