import os
import numpy as np
import math
from time import sleep
import cProfile
import pickle
import concurrent.futures
import psutil
def index(partial):
    
    #pathName = 0
    x = 0
    y = 0
    z = 0
    type = 0
    purity = 0
    useint = settings['useint'][0]
    for line in partial:
       # if "pathName" in line:
        #    line = line.split('"')
         #   line = line[3]
          #  line = line.split(".")
           # pathName = line[1]

        if '"x"' in line:
            line = line.split(',')
            line = line[0]
            line = line.split(':')
            x = line[1].strip()
            x = float(x)
            
        if '"y"' in line:
            line = line.split(',')
            line = line[0]
            line = line.split(':')
            y = line[1].strip()
            y = float(y)

        if '"z"' in line:
            line = line.split(',')
            line = line[0]
            line = line.split(':')
            z = line[1].strip()
            z = float(z)

        if "type" in line:
            line = line.split('"')
            type = line[3]

        if "purity" in line:
            line = line.split('"')
            purity = line[3]
            if purity == "pure":
                purity = 3
            elif purity == "impure":
                purity = 1
            elif purity == 'normal':
                purity = 2
        

        if useint:
            x = math.floor(float(x))
            x = int(x)
            y = math.floor(float(y))
            y = int(y)
            z = math.floor(float(z))
            z = int(z)
       
    if type != 0:
        if type == 'coal':
            index = 'co'
        elif type == 'copper':
            index = 'c'
        elif type == 'caterium':
            index = 'ca'
        elif type == 'sam':
            index = 'm'
        elif type == 'green':
            index = 'blue'
        elif type == 'mercer':
            index = 'me'
        elif type == 'somersloop':
            index = 'so'
        else:
            index = type[0:1]

        if index not in name.keys():
                name[index] = type
        if purity != 0:
            if index not in ores.keys():
                ores[index] = []
            ores[index].append([x,y,z,purity])
        else:
            if index not in collectible.keys():
                collectible[index] = []
            collectible[index].append([x,y,z])
        
            

def parse():
    partial = []
    file = open(os.path.abspath("en-stable.json"))
    for line in file:
        if "{" in line:
            partial = []
        if "}" in line:
            index(partial)
            partial = []
        
        elif not(('[' in line)or(']' in line)):
            partial.append(line.strip())
    file.close()

def confirm()->bool:
    if settings['confirm'] == 1:
        good = False
        string = input()
        while not good:
            string = string.lower()
            if ('y' or '1') in string:
                good = True
                value = True
            elif('n' or '0') in string:
                good = True
                value = False
            else:
                string = input('input not reccognised, please try again: (y/n)\n')
    else:
        return(True)
    return value
        
def key2name(key):
        return name[key]

def name2key(names):
    inv_name = {v: k for k, v in name.items()}
    if names in inv_name.keys():
        return inv_name[names]
    else:
        return 0

def isore(key):
    return(key in ores.keys())

def seeColec():
    print("collection:")
    for item in collection.keys():
        if isore(item):
            print("{}/min of {}".format(collection[item]*300,key2name(item)))
        else:
            print("{} of {}".format(collection[item],key2name(item)))

def addore():
    valid = False
    while not valid:
        print('ore to add:')
        io = dict()
        i = 0
        for ore in ores.keys():
            print("{}){}".format(i+1,key2name(ore)))
            io[i] = ore
            i += 1
        
        print('{})back'.format(i+1))
        select = input()
        #checks if they put a number
        if select.isnumeric():
            #for the back option\
            select = int(select)
            if select == i+1:
                return
            #see if valid num, if so use as input
            elif select <= len(ores):
                select = io[select-1]
                valid = True
            #tries to match text
        elif name2key(select) != 0:
                select = name2key(select)
        else:
            ("invalid input, please try again")
            sleep(1)

    #asks how much to add
    valid = False
    while not valid:
        amount = input('how much {} per min?\n'.format(key2name(select)))
        if amount.isnumeric():
            valid = True
            amount = int(amount)
        else:
            print('not a number')


    #adds to the dict
    
    if select in collection.keys():
        collection[select] += math.ceil(amount/300)
    else:
        collection[select] = math.ceil(amount/300)
    
    if (select == 'ca') and collection[select]%2 != 0:
        collection[select] += 1
        amount += 300

    print("added {0} {1}/min for a total of {2} {1}/min".format(math.ceil(amount/300)*300,key2name(select),collection[select]*300))

def addCol():
    valid = False
    while not valid:
        print('collectible to add:')
        print('slugs:')
        io = dict()
        i = 0
        for collec in collectible.keys():
            print("{}){}".format(i+1,key2name(collec)))
            io[i] = collec
            i += 1
        
        print('{})back'.format(i+1))
        select = input()
        #checks if they put a number
        if select.isnumeric():
            #for the back option\
            select = int(select)
            if select == i+1:
                return
            #see if valid num, if so use as input
            elif select <= len(ores):
                select = io[select-1]
                valid = True
            #tries to match text
        elif name2key(select) != 0:
                select = name2key(select)
        else:
            ("invalid input, please try again")
            sleep(1)

    #asks how much to add
    valid = False
    while not valid:
        amount = input('how much {} to add?\n'.format(key2name(select)))
        if amount.isnumeric():
            valid = True
            amount = int(amount)
        else:
            print('not a number')


    #adds to the dict
    
    if select in collection.keys():
        collection[select] += amount
    else:
        collection[select] = amount
    
    print("added {0} {1}(s) for a total of {2} {1}(s)".format(amount,key2name(select),collection[select]))
    
def calculate(collection):
    print('calculating permutations, may take a while')
    sm = 0
    options = dict()
    for item in collection.keys():
        print('on {}'.format(key2name(item)))
        purity = []
        if isore(item):
            for node in range(0,len(ores[item])):
                purity.append(ores[item][node][3]) 
            choices = np.zeros(collection[item],dtype=int)
            good2 = list()

            if settings['multithread'][0] == 1:
                
                pool = concurrent.futures.ThreadPoolExecutor(max_workers=len(purity))
                choices = np.zeros(collection[item]-1,dtype=int)
                for star in range(0,len(purity)):
                    pool.submit(incriment,0,len(purity),choices,good2,purity,star)
            else:
                choices = np.zeros(collection[item],dtype=int)
                incriment(0,len(purity),choices,good2,purity,-1)
            if settings['multithread'][0] == 1:
                print('threads initialised')
                pool.shutdown(wait=True)
            options[item] = good2
        else:
            print('do this lazy butt')
    
    sm = 1
    for resource in options.keys():
        sm *= len(options[resource])
    print("there are {} permutations to try, continue? (y/n)".format(sm))
    if confirm():
        max = []
        for key in options.keys():
            max.append(len(options[key]))
        #base of each digit is = max n
        count = np.zeros(len(options.keys()),dtype=int)

        bestdist,distpos,done = countoff(max,count,0,False,options)

        print('the best distance was {:.2f} with the following locations:'.format(bestdist))
        i = 0
        for resource in options.keys():
            num = 1
            print('{}:'.format(key2name(resource)))
            cur = options[resource][distpos[i]]
            skip = 0
            for node in cur:
                if skip == 0:
                    position =  ores[resource][node]
                    x = (position[0])
                    y = (position[1])
                    z = (position[2])
                    if isore(resource):
                        pure = int(position[3])
                        if pure == 1:
                            pure = 'impure'
                        elif pure == 2:
                            pure = 'normal'
                            skip = 1
                        elif pure == 3:
                            pure = 'pure'
                            skip = 3
                        print('node {} : ({:.2f},{:.2f},{:.2f}), {}'.format(num,x,y,z,pure))
                    else:
                        print('node {} : ({:.2f},{:.2f},{:.2f})'.format(num,x,y,z))
                else:
                    skip -= 1
                    num -=1
                num += 1
            i += 1




    
def countoff(max,count,pos,done,options):
    
    if pos > 2:
        sm = 0
        at = 0
        place = 0
        for i in range(0,len(count)):
            sm += (max[i]**place)* count[i]
            at += (max[i]**place) * max[i]
            place += 1
        print('{:.3f}%'.format(sm/at*100))

    go = True
    bestdist = -1
    while go and not done:

        #increases if less then 10
        if count[pos] < max[pos]:
            dist = distance(count,options)
            if dist < bestdist or bestdist == -1:
                distpos = []
                bestdist = dist
                for i in count:
                    distpos.append(i)
                

        #goes to 10 when needed
        elif pos < (len(max)-1):
            count[pos] = 0
            count[pos+1] += 1
            if pos == 0 :
                dist,retpos,done = countoff(max,count,pos+1,done,options)
            if pos > 0:
                return(countoff(max,count,pos+1,done,options))
            if dist < bestdist and dist >= 0:
                bestdist = dist
                distpos = retpos

        else:
            go = False
            done = True
            if pos != 0:
                distpos = []
                bestdist = -2
            return(bestdist,distpos,done)
        if pos != 0:
            go = False
        elif not done:
            count[pos] += 1
        if done:
            go = False
            print(done)
    return(bestdist,distpos,done)


def distance(pos,options):
    allpos = []
    i = 0
    for resource in options.keys():
        cur = options[resource][pos[i]]
        for node in cur:
            position =  ores[resource][node]
            x = (position[0])
            y = (position[1])
            z = (position[2])
            allpos.append([x,y,z])
        i+=1
    distsm = 0
    total = 0
    for node1 in allpos:
        for node2 in allpos:
            if node2 > node1:
                total += 1
                sm = 0
                for i in range(0,3):
                    sm = ((node1[i]+node2[i])**2)
                distsm += math.sqrt(sm)
    if total != 0:
        dist = distsm/total
    else:
        dist = 0
    return dist


def incriment(position,base,choices,good2,nums,star):
    if star == -1:
        if position > 2:
            total = 0
            sm = 0
            place = 0
            for i in choices:
                sm+= (base**place) * int(i)
                total += (base**place) * base
                place += 1
            print('{:.{}f}%'.format(sm/total*100,len(choices)-2))

    
    go = True
    while go and (choices[0] != -3):
        if choices[position] < base:
            valid = isValid(choices,nums,star)
            if valid:
                temp = np.zeros(len(choices),dtype=int)
                for i in range(0,len(temp)):
                    temp[i] = choices[i]
                good2.append(temp)
            
        else:
            #print(choices)
            full = True
            for n in choices:
                if n != base:
                    full = False
                    
            if full:
                go = False
                choices[0] = -3
                return()
            else:
                choices[position+1] += 1
                i = position
                while i >= 0:
                    choices[i] = choices[position+1]
                    i -= 1
                incriment(position+1,base,choices,good2,nums,star)
        if position != 0:
            go = False
        else:
            if choices[0] != -3:
                choices[position]+=1
    
    return()


def isValid(array,nums,star):
    if star != -1:
        np.append(array,star)
    ones = 0
    twos = 0
    if settings['efficiency'][0] == 2:
        #checks for pure nodes for this one, so uranium works
        pureexists = False
        for y in nums:
            if 3 == y:
                pureexists = True
    for x in range(0,len(array)):
        if (nums[array[x]] == 2) or (nums[array[x]] == 3):
            if (nums[array[x]] == 2):
                twos += 0.5
            match2 = 0
            match3 = 0
            for y in range(0,len(array)):
                if y != x:
                    if nums[array[y]] == 2 and (array[y] == array[x]):
                        match2 += 1
                    if nums[array[y]] == 3 and (array[y] == array[x]):
                        match3 += 1
            if (match2 != 1) and (nums[array[x]] == 2):
                return(False)
            if (match3 != 3) and (nums[array[x]] == 3):
                return(False)
        else:
            ones +=1
            for y in range(x+1,len(array)):
                if array[y] == array[x]:
                    return(False)
        if settings['efficiency'][0] == 2:
            if pureexists:
                #makes sure we are using pure nodes befoe anything else
                amount = len(array)
                if amount % 2 == 1:
                    amount -= 1
                    if ones > 1:
                        return(False)
                else:
                    if ones > 0:
                        return(False)
                amount = amount/2
                if amount % 2 == 1:
                    if twos > 1:
                        return(False)
                else:
                    if twos > 0:
                        return(False)
            else:
                #defaults to normal otherwise
                amount = len(array)
                normal = amount % 2
                if normal == 1:
                    if ones > 1:
                        return(False)            
                else:
                    if ones > 0:
                        return(False)

        if settings['efficiency'][0] == 1:
            #makes sure we are using pure and normal before impure
            amount = len(array)
            normal = amount % 2
            if normal == 1:
                if ones > 1:
                    return(False,1)

            else:
                if ones > 0:
                    return(False,1)

    return True

def saveset(settings):
    with open('settings.pickle', 'wb') as handle:
        pickle.dump(settings, handle, protocol=pickle.HIGHEST_PROTOCOL)

def loadset():
    if os.path.isfile("settings.pickle"):
        with open('settings.pickle', 'rb') as handle:
            settings = pickle.load(handle)
    else:
        settings = dict()

    possible = {'efficiency':[1,2,"if not zero ignores impure in favor of normal/pure,drastically decreases computation time, but may give worse results\n"],
                'useint':[1,1,"uses ints for all values instead of floats,less acurate but faster\n"],
                'multithread':[0,1,"adds multithreading, may not improve performance\n"],
                'confirm':[1,1,"confirm before doing stuff\n"]}
    for i in possible.keys():
        if i not in settings.keys():
            settings[i] = possible[i]
    return(settings)
        
def chngset(settings):
    go = True
    while go:
        string = ('setting: \t current: \t max:\n')
        for i in settings.keys():
            string += ('{}: \t   {} \t \t {}\n'.format(i,settings[i][0],settings[i][1]))
            string += settings[i][2]
        string+=("to exit: 'exit' or 0")
        print(string)
        key = input('which setting would you like to change?:\n')
        key = key.lower()
        if key =='0' or key == 'exit':
            go = False
        elif key in settings.keys():
            value = input('changing {}, new value?:\n'.format(key))
            if value.isnumeric():
                value = int(value)
                if value >=0 and value <= settings[key][1]:
                    print('{} set to {}'.format(key,value))
                    settings[key][0] = value
                else:
                    print('value out of range')
            else:
                print('not valid setting')
    saveset(settings)
    return(settings)



settings = loadset()
print("initialising")
ores = dict()
collectible = dict()
name = dict()
parse()
go = True
collection = dict()
eep = 0


while go:
    if eep != 0:
        sleep(eep)
        eep = 0
    print('optimal location calculator:\n1)add ores\n2)add collectibles\n3)see collection\n4)reset collection\n5)calculate\n9)settings\n0)exit')
    match input():
        case '1':
            addore()
        case '2':
            addCol()
        case '3':
            seeColec()
            eep = 3
        case '4':
            print('reset collection?(y/n)')
            if confirm():
                collection = dict()
                print('collection reset')
                eep = 1
        case '5':
            seeColec()
            print('calculate with this collection?(y/n)')
            if confirm():
                good2 = []
                cProfile.run('calculate(collection)') 
                #calculate(collection)
                eep = 5
        case '9':
            settings = chngset(settings)
        case '0':
            print('exit program?(y/n)')
            if confirm():
                print('saving settings')
                saveset(settings)
                go = False
        case _:
            print('invalid input, please try again')
            eep = 1
            
