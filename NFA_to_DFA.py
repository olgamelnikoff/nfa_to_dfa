'''
Test this with the following input:
0 1
q0 q1
q0
q1
q0,q1
q0
q0
0
'''

from graphviz import Digraph
import json
import graphviz
import pydot
import re
import os

from texttable import Texttable
from collections import defaultdict

def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele
        str1 = str1 + " "
    
    # return string   
    return str1.rstrip()

def powerset (inputStates):
    inputStatesSize = len(inputStates)
    outputStatesSize = 2 ** inputStatesSize
    counter = 0
    i = 0
    listOfDFAStates = []
    for counter in range(outputStatesSize):
        localList = []
        for i in range(inputStatesSize): 
            if((counter & (1 << i)) > 0):
                newString = inputStates[i]
                localList.append(newString)
        thisString = listToString(localList)
        if (len(thisString) == 0):
            thisString = u'\u00d8'
        listOfDFAStates.append(thisString)
        print("")
    return listOfDFAStates

def replaceByAlphabet (i):
    asciiInt = i + 64
    character = str(chr(asciiInt))
    return character

def convertingKey1ToSet(key):
    cellArrayOfStates = []
    cellArrayOfStates = key.split()

    #Eliminating additional arrows and stars
    if ((len(cellArrayOfStates) > 1) & (key.startswith('->'))):
        if ('*' in key):
            key = key.replace('->', '')
            key = key.replace('*', '')
            key = '*' + key
        else:
            key = key.replace('->', '')
    elif((len(cellArrayOfStates) > 1)):
        if ('*' in key):
            key = key.replace('*', '')
            key = '*' + key

    #Converting the string into an array of sets
    cellArray = []
    cellStatesSet = set()
    cellStarArrowSet = set()
    if(key != u'\u00d8'):
        if ('->*' in key):
            key = key.replace('->*', '')
            cellStarArrowSet.add('->*')
        elif ('->' in key):
            key = key.replace('->', '')
            cellStarArrowSet.add('->')
        elif ('*' in key):
            key = key.replace('*', '')
            cellStarArrowSet.add('*')
        if (len(cellStarArrowSet) > 0):    
            cellArray.append(cellStarArrowSet)
 
        finalArrayOfStates = []
        finalArrayOfStates = key.split()
        if (len(finalArrayOfStates) > 1):
            for i in range(len((finalArrayOfStates))):
                cellStatesSet.add(finalArrayOfStates[i])
        else:
            cellStatesSet.add(key)
        cellArray.append(cellStatesSet)
    
    else:
        cellArray.append(u'\u00d8')
    
    return cellArray

def removeArrowsStars(key):
    if ('->*' in key):
        newKey = key.replace('->*', '')
    elif ('->' in key):
        newKey = key.replace('->', '')
    elif ('*' in key):
        newKey = key.replace('*', '')
    else:    
        newKey = key

    return newKey


def inputToTable ():
    #Creating a class for a diagram
    dot = Digraph()
    
    tableNFA = []
    tableDFAInterm = []
    tableDFAFinal = []
    
    print('Please enter the alphabet symbols in your alphabet separated by white spaces.')
    alphabetInput = input()
    alphabetInput = alphabetInput.split()

    #Creating an array of alphabet symbols
    alphabetArray = []

    numOfAlphSymb = len(alphabetInput)
    for i in range(numOfAlphSymb):
        alphabetArray.append(alphabetInput[i])
    
    #Creating the first row of the table consisting of one white space
        #and all the alphabet symbols.
    firstRow = []
    firstRow.append(' ')
    for i in range (numOfAlphSymb):
        firstRow.append(alphabetInput[i])

    tableNFA.append(firstRow)
    tableDFAInterm.append(firstRow)
    tableDFAFinal.append(firstRow)
    
    #Prompting the user to enter all the states
    print('Please enter the states separated by white spaces. They are your table row names.')
    statesInput = input()
    statesInput = statesInput.split()

    #Prompting the user to enter the start state
    print('Please enter the start state out of the list you entered.')
    startState = input()

    #Prompting the user to enter the accepting state / states
    print('Please enter the accepting state or states out of the list you entered.')
    print('If there are several accepting states, separate them by white spaces.')
    acceptingStates = input()

    numOfInputStates = len(statesInput)

    #Creating maps
    mapNFA = defaultdict(dict)
    intermMapDFA = defaultdict(dict)
    finalMapDFA = defaultdict(dict)
    alphabetMapDFA = dict()

    #Constructing an NFA table:
    updatedStatesInputNFA = []
    for i in range(numOfInputStates):
        if ((startState == statesInput[i]) and (startState in acceptingStates)):
            updatedStatesInputNFA.append('->*' + statesInput[i])
        elif (startState == statesInput[i]):
            updatedStatesInputNFA.append('->' + statesInput[i])
        elif (statesInput[i] in acceptingStates):
            updatedStatesInputNFA.append('*' + statesInput[i])
        else:
            updatedStatesInputNFA.append(statesInput[i])

    #User enters input to fill out the source NFA table
    for i in range (numOfInputStates):
        #Key 1 is a key in the map that designates the source state
        key1 = str(updatedStatesInputNFA[i])
        print('Entering input for row '+ str(updatedStatesInputNFA[i]) + '.')

        #Local list is a list created for this particular row.
        localList = []
        #Adding the first cell to the row (it has a source NFA state)
        localList.append(updatedStatesInputNFA[i])

        #A loop for the user to enter the data
        for j in range(numOfAlphSymb):
            #Key 2 is a second key in the map that denotes
            #an alphabet symbol
            key2 = str(alphabetArray[j])
            print('Please enter an input for alphabetical symbol '+ str(alphabetArray[j]) + '.')
            print('If there are several states for one cell, separate them by commas.')
            print('If there are no states in the cell, indicate it by 0')
            localInput = input()
            if (localInput == '0'):
                value = u'\u00d8'
            else: 
                value = set()
                if (',' in localInput):
                    localInput = localInput.split(',')
                    for k in range(len(localInput)):
                        value.add(localInput[k])
                else:
                    value.add(localInput)          
            localList.append(value)
            mapNFA[key1][key2] = value
        tableNFA.append(localList)

    #NFA Map is ready
    #NFA Table is ready

    #Showing the entered information to the user in a tabular form. 
    #The user is prompted to answer "Yes" if the table is correct.
    
    tNFA = Texttable()
    tNFA.add_rows(tableNFA)
    print(tNFA.draw())
    
    print('Here is the table constructed based on your input. Is it correct? Type Yes or No.')
    answer = input()

    if (answer != 'Yes'):
        print('Table incorrect. Exiting program.')
        exit()

    #Creating a list of target states of the target DFA
    #using the powerset function.
        
    statesDFA = powerset(updatedStatesInputNFA)

    #Filling the DFA map using two keys and 1 value
    finalStates = []
    for i in range(len(statesDFA)):
        key1 = statesDFA[i]
        for j in range(len(alphabetArray)):
            key2 = alphabetArray[j]
            #For now, just putting empty values for the DFA map
            intermMapDFA[key1][key2] = '' 

    firstColumnOfFinalTableArray = []

    for key1DFA in intermMapDFA.keys():
        localListDFA = []
        localListDFA.append(convertingKey1ToSet(key1DFA))
        firstColumnOfFinalTableArray.append(convertingKey1ToSet(key1DFA))
        if (key1DFA == u'\u00d8'):
            for key2 in intermMapDFA[key1DFA]: 
                value = u'\u00d8'
                intermMapDFA[key1DFA][key2] = value  
                localListDFA.append(value)
            tableDFAInterm.append(localListDFA)
               
        else:
            arrayOfStates = []
            arrayOfStates = key1DFA.split()
            if (len(arrayOfStates) == 1):
                for key1NFA in mapNFA.keys():
                    if (key1DFA == key1NFA):
                        for key2 in mapNFA[key1NFA]:
                            value = mapNFA[key1NFA][key2]
                            intermMapDFA[key1DFA][key2] = value
                            localListDFA.append(value)
                        tableDFAInterm.append(localListDFA)
                        break
                     
            else:
                for key2 in intermMapDFA[key1DFA]:
                    cellSet = set()
                    for k in range(len(arrayOfStates)):
                        value = mapNFA[arrayOfStates[k]][key2]
                        if(value != (u'\u00d8')):
                            cellSet.update(value)
                    if (len(cellSet) == 0):
                        intermMapDFA[key1DFA][key2] = u'\u00d8'
                        localListDFA.append(u'\u00d8')
                    else:
                        intermMapDFA[key1DFA][key2] = cellSet
                        localListDFA.append(cellSet)
                
                tableDFAInterm.append(localListDFA)

    #The intermediate DFA table is ready

    print('Here is an intermediary transition table of all the DFA states')
    tDFA = Texttable()
    tDFA.add_rows(tableDFAInterm)
    print(tDFA.draw())

    arrayOfLetters = []
    #Creating a map with alphabet characters as a key and equivalent
    #states as a value
    counter = 0
    for j in firstColumnOfFinalTableArray:
        i = j
        counter = counter + 1
        if (len(i) == 2):
            i = i[1]
            thisSet = i
        else:
            i = i[0]
        thisSet = i
        key1 = ''
        key1 = replaceByAlphabet(counter)
        arrayOfLetters.append(key1)
        alphabetMapDFA[key1] = thisSet
        
    for key1 in intermMapDFA.keys():
        newKey = removeArrowsStars(key1)
        for key2 in intermMapDFA[key1]: 
            finalMapDFA[newKey][key2] = intermMapDFA[key1][key2]
    
    finalFirstColumn = []

    #Filling out the first column
    for j in firstColumnOfFinalTableArray:
        localList = []
        if (len(j) == 2):
            i = j
            localListOfSets = []
            localListOfSets.append(i[0])
            m = i[1]
            for k in alphabetMapDFA:
                if (alphabetMapDFA[k] == m):
                    node = str(k)
                    if (i[0] == {'->*'}):
                        dot.node('Fake', 'q', style = 'invisible')
                        dot.edge('Fake', node, style = 'bold')
                        dot.node(node, node, root = 'true', shape = 'doublecircle')
                    elif (i[0] == {'->'}):
                        dot.node('Fake', 'q', style = 'invisible')
                        dot.edge('Fake', node, style = 'bold')
                        dot.node(node, node, root = 'true')
                    elif(i[0] == {'*'}):
                        dot.node(node, node, shape = 'doublecircle')
                    localListOfSets.append(k)
            finalFirstColumn.append(localListOfSets)
        else:
            if (j == [u'\u00d8']):
                i = u'\u00d8'
            else:
                i = set()
                i = j [0]
            for k in alphabetMapDFA:
                if (alphabetMapDFA[k] == i):
                    finalFirstColumn.append(k)
                    dot.node(k, k)
            
    #Creating the table
    #localListCounter = 0
    newCounter = 0
    for key1 in finalMapDFA.keys():
        localListDFA = []
        localListDFA.append(finalFirstColumn[newCounter])
        initialStateForNode = finalFirstColumn[newCounter]
        arrayForNode = finalFirstColumn[newCounter]
        #if (len(finalFirstColumn[newCounter]) == 2):
            #nodeText
        #dot.node(str(finalFirstColumn[newCounter]), str(finalFirstColumn[newCounter]))
        newCounter = newCounter + 1
        for key2 in finalMapDFA[key1]:
            oldTableValue = finalMapDFA[key1][key2]
            newTableValue = oldTableValue
            for key in alphabetMapDFA:
                    value = alphabetMapDFA[key]
                    if (oldTableValue == value):
                        newTableValue = key
                        if (len(arrayForNode) == 2):
                            initialStateForNode = arrayForNode[1] 
            dot.edge(initialStateForNode, newTableValue, label = key2)
            localListDFA.append(newTableValue)

        tableDFAFinal.append(localListDFA)

    print('Here is the final transition table of all the DFA states')
    tFinalDFA = Texttable()
    tFinalDFA.add_rows(tableDFAFinal)
    print(tFinalDFA.draw())
    
    #Outputting the FA diagram using the render() method
    return dot.render('q2_DFA_diagram.gv', view=True)  # doctest: +SKIP

            

#main
var = inputToTable()
