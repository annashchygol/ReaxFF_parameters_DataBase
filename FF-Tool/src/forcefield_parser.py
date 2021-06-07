
from DataBase import ForceField
from items import createFFBlocks, updateKeys, createFFDictionaries
from items import inputFFBasedMinMaxStr, inputBasedBoolStr, randomGuessInRanges
from comparison import compareFFsDict
from ffProperties import detectBranch, addFFName, gatherFFInfo, printFF, nicePrintFF
from ranges import gatherDataByKey, getRanges, getDirectRanges
from input_output import parse
from copy import deepcopy
import os
import logging


def getFFData(ffilePath):
    """
    Add Doc
    """
    with open(ffilePath, 'r') as ffinfile:
            ffindata = ffinfile.read()

    return ffindata


def processFF(ffpath, ranges=False):
    logging.info("Processing force field.")
    tup = os.path.split(ffpath)
    filename =  tup[1]# python thing with the str ; get name or smth 
    logging.debug (' {} {} {} {}{}'.format('ffpath =', str(ffpath), '[filename =', filename, ']'))
    #logging.debug(''.format( ffpath))
    ffdata = getFFData(ffpath)
    blocks = createFFBlocks(ffdata)
    if ranges:
        oldKeysInBlocks = []
        oldKeysInBlocks = deepcopy(blocks)
    updateKeys(blocks)
    ffDict = createFFDictionaries(blocks)
    gatherFFInfo(ffDict, filename)
    if ranges:
        return (ffDict, oldKeysInBlocks)
    return ffDict


def printInfoRequest(dataBase, infoRequestStr):
    for i in dataBase:
        print(i["info"]["name"], i["info"][infoRequestStr])


def checkNegativeParamEq13a(dataBase):
        #Before everything: 
        #Just looking if there are any negative valance angle parameters:
        #PRINT parameter #2: 
        logging.info('____________________________________\n', "CHECKING NEGATIVE param for EQ(13a)")
        for elem in dataBase:
                logging.debug("NAME:", elem['info']['name'])
                for itemKey in elem['angles']:

                        if isinstance(elem['angles'][itemKey][0], list):
                                if float(elem['angles'][itemKey][1][0]) < 0.0 or float(elem['angles'][itemKey][1][1]) < 0.0:
                                        logging.debug(itemKey, elem['angles'][itemKey][1], elem['angles'][itemKey])

                        elif float(elem['angles'][itemKey][1]) < 0.0:
                                        logging.debug(itemKey, elem['angles'][itemKey][1], elem['angles'][itemKey]) 

        logging.info("CHECKED!", '\n____________________________________')


def createMinMaxFiles(path, min, max): 
        # 1.Check current working directory;
        retval = os.getcwd()
        logging.info("Current working directory", retval)
        if not os.path.exists(path):
                os.makedirs(path)
        #open("testAnna.ff", 'a')

def randomInitGuessStr(inBlocksOldKeys, dataBase, rangesFlag):
    logging.info("Getting random initial guess from DataBase.")
    return randomGuessInRanges(inBlocksOldKeys, dataBase, rangesFlag)


def minMax2outStr(inBlocksOldKeys, dataBase, rangesFlag): #flag shouldn't be here.
    # Now is just a wrapper; 
    logging.info("[MINMAX] Getting min/max out of DataBase.")
    return inputFFBasedMinMaxStr(inBlocksOldKeys, dataBase, rangesFlag)


def bool2outStr(inBlocksOldKeys, keysToOpt):
    logging.info("[BOOL] Generating bool file from input KEYs.")
    return inputBasedBoolStr(inBlocksOldKeys, keysToOpt)


def getOldFFKeys(inputFFs):
    #____________________________________________________
    #Open the ff file, for which ranges are needed:
    logging.info('Function getOldFFKeys: starts')

    for ffindata in inputFFs:
        inBlocks = createFFBlocks(ffindata)
        # Bofore blocks are updated, I can use the same keys for printing.
        logging.debug('{} {}'.format("InBlocks:", inBlocks))
        oldKeysInBlocks = deepcopy(inBlocks) # Before update; This is just a pointer to the same list; I need a deep copy instead;

    logging.info('Function getOldFFKeys: ends')
    return oldKeysInBlocks


def compareFFs(ffs, ffsDB, keys = None): # ffs is needed at least to introduce order; key is the key(s) I might be intersted in

    for i in range(len(ffs)):
        for j in range(i+1, len(ffs)):
            ff1 = ffs[i]
            # when I take them(ffs) from DB, they(ffs) already have a name;
            # Need to use it to extraxt the name: 
            ff1db = ffsDB[i]
            ff2db = ffsDB[j]

            print('\n >>> Comparing 2 ff files:', ff1db['info']['name'], 'vs', ff2db['info']['name']) # Ne to; Too much; only names are needed.
            #compareFFs(ff1, ff2db)
            #print('_____________________________________________')
            compareFFsDict(ff1db, ff2db, keys)


def main(options):

    logging.basicConfig(format= '%(levelname)s:%(message)s', filename='ffTool.log',level=logging.DEBUG) # Move creation of this file into ''
    logging.basicConfig(filename='ffToolInfo.log',level=logging.INFO) # Move creation of this file into ''

    dataBase = [processFF(ffpath, filename) for ffpath in options.inputFF for filename in os.listdir(ffpath)]

    if options.checkEq13:
        checkNegativeParamEq13a(dataBase)

    inBlocksOldKeys = getOldFFKeys(options)
    minMax2File1(options, inBlocksOldKeys, dataBase) #TODO: uncomment

    #=======================================================#
    #getLeftKeysParents(dataBase)
    #=======================================================#
    #Investigate the diff between O-H bonds; different branches;
    #print("\nO-H bonds params investigation:")
    #gatherDataByKey(dataBase, "bonds", 'O-H')
    #gatherDataByKey(dataBase, "bonds", 'H-O')
    #=======================================================#
    #minMax2File(options)

if __name__ == "__main__":
   options = parse()
   main(options)