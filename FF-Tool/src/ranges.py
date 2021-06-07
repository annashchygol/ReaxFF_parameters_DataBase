#Produce ranges: 
#Input: ffield
#Output: min, max;
#How it works:
#> I parse input file: -> List of keys: {atoms. bonds, etc.} to look for min and max;
#> At first I will start with the atoms and than extend further to whole force field;
#> To gather min and max values per atom:

import copy
import numpy as np
import io
import logging


# This could be extended, especially if I am gonna use quartiles instead of min and max
def getMinMax(d2List):
    A = np.array(d2List)
    #logging.debug('{} {}'.format('A =', A))
    mins = np.amin(A, axis= 0)
    maxs = np.amax(A, axis= 0)
    return mins, maxs

# This will be more robust and statistically more reliable;
# Here I can add what Toon has suggested before:[to decrease sensitivity to outliers]
# 1. [Q1 - (Q3-Q1)/2, Q3 + (Q3-Q1)/2],  halfFlag = True
# 2. [Q1 - (Q3-Q1),   Q3 + (Q3-Q1)],    halfFlag = False 
def getMinMaxByQuartiles(d2List, halfFlag):
    logging.info('Quartiles-based min & max.')
    A = np.array(d2List)
    Q1 = np.percentile(A, 25, axis = 0)
    Q3 = np.percentile(A, 75, axis = 0)
    logging.debug('{} {} {} {}'.format('Q1 & Q3 = \n', Q1, '\n', Q3))

    #this is one of the ways to go
    diff = Q3 - Q1
    diff = diff * halfFlag
    
    mins = Q1 - diff
    maxs = Q3 + diff
    
    logging.debug('{} {} {}'.format('Here they are:\n', mins, maxs))
    return mins, maxs

# This is more of a way to generate random initial guess within certain ranges; 
# Think more about it; 
def getRandomGuessWithinDBRanges(d2List):
    logging.info('Random guess (min & max).')
    A = np.array(d2List)
    mins = np.amin(A, axis= 0)
    print('min:', mins)
    maxs = np.amax(A, axis= 0)
    print('max:', maxs)

    # There should be a better way. 
    A_len  = A.shape[1]
    rand = np.random.random_sample(A_len)
    #init_guess = mins + rand * (maxs - mins)

    # Suggestion from Toon: To avoid strting from the corner; 
    delta4 = (maxs - mins)/4
    low = mins + delta4 
    high = maxs - delta4
    init_guess = low + rand * (high - low)
    return init_guess


def getMedian(d2List):
    A = np.array(d2List)
    median = np.median(A, axis=0)
    return median, median

def addDistinctItem(key, dictElem, distinctItemsList): # Not just add. But also check!!!
    if (key in dictElem.keys()): # -> 1-line:
        logging.debug('{} {}'.format('Successfull if condition for KEY:', key))
        curItem = dictElem[key]
        if isinstance(curItem[0], list): # => List of lists. Need to get contribution from all.
            # To check if the value is already present in the key:
            #distinctItemsList.extend(curItem)
            for i in curItem:
                if i not in distinctItemsList:
                    distinctItemsList.append(i)
             
        elif curItem not in distinctItemsList: # Adding only elements, not present in the list; 
            distinctItemsList.append(curItem)
    return distinctItemsList


def reverseKey(key): # should be elsewhere
    keyLst = key.split('-')
    keyLst.reverse()
    reverseKey = '-'.join(keyLst)
    return reverseKey


def gatherDataByKey(dataBase, block, directItemKey, quartileFlag = False, randGuess = False):
    #medianFlag = True # ToDO: comment this out; 
    logging.info('{} {} {} {}'.format('Gathering ff data, [KEY] =', directItemKey, 'type', type(directItemKey)))
    logging.debug('{} {}'.format('Flag. Immediately! [2]:', quartileFlag))
    # At first parameters are together. [More convenient for quartiles]

    reverseItemKey = reverseKey(directItemKey) # direct key could be an argument;
    logging.debug('{} {} {} {}'.format('Direct key =', directItemKey, 'of type =', type(directItemKey)))

    if (block != 'general'):
        distinctItems = []

        for elem in dataBase:
            #print ("FF NAME:", elem['info']['name'])

            logging.debug('{} {} {} {}'.format('ELEM[', len(elem[block].keys()), '] =', elem[block].keys()))
            distinctItems = addDistinctItem(directItemKey, elem[block], distinctItems)

            if reverseItemKey and (block != 'hydrogen'): # For hydrogen block order matters. 
                distinctItems = addDistinctItem(reverseItemKey, elem[block], distinctItems)

        #print('Gathered Item List size:', len(distinctItems))
        logging.debug('{} {} {}'.format("\n > Gathered Item List", len(distinctItems), distinctItems))

        # After this 2d list is ready, I can manipulate with data: get mins / maxs / quartiles.
        # Since repeating elements are not added to the list of 'distinctItems', this will affect the Q1, Q3. Think over!  
        # Error occurs, when gathered list of distinctItems is empty:
        try:
            #if isinstance(gatheredItemsList, list):
            logging.info("Is instance!" + " List: " + str(distinctItems))
            #print ("Yes, is instance. LIST:", gatheredItemsList) #!!! TODO: uncomment; writing in the wrong channel; strean it to log;
            logging.debug('{} {}'.format('Flag. Immediately! [3]:', quartileFlag))

            if randGuess:
                #if not distinctItems:
                #    print("dataBase", dataBase)
                return getRandomGuessWithinDBRanges(distinctItems)

            if quartileFlag:
                return getMinMaxByQuartiles(distinctItems, quartileFlag)
            #if medianFlag:
            #    return getMedian(distinctItems)
            elif distinctItems:
                return getMinMax(distinctItems)

        except IndexError:
            logging.error("This Key is not present")


# Looping through all of the elements of inFF; and getting ranges for every block;
def getRanges(inFF, dataBase, quartileFlag = False):
    logging.info("   >>> Getting ranges:")
    logging.info('{} {}'.format('Flag. Immediately! [1]:', quartileFlag))
    logging.debug('{} {}'.format('Blocks of the initial force field: \n', inFF.keys()))
    for block in inFF: #These keys I'm going to use for DB search

        logging.info('_______________________')
        if (block != None):
            logging.debug(" Block name = " + str(block) + ", Length = "+ str(len(inFF[block])))
            print('  > Block',  block)

            for key in block: # why oblect is not  iterable ?
                logging.debug("First loop!")
                return gatherDataByKey(dataBase, block, key, quartileFlag)


def getDirectRanges(inFF, dataBase, quartileFlag = False):
    logging.info(">>> Getting Direct ranges:")
    # What I need to know is old keys and print stuff in terms of old
    for block in inFF: #These keys I'm going to use for DB search
        logging.debug('{} {}'.format("Block:", block, len(inFF[block])))
        if (block == 'general'):
            logging.info("Not for general block...")

        for key in inFF[block]:
            #print(key)
            gatherDataByKey(dataBase, block, key, quartileFlag)
