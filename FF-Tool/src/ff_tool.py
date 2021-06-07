# FF-Tool. Task manager: 

#1. Get the input, Should be dictionary; [based on cmd / Yaml];
#2. Create the object for task manager; fill in all the fields;
#3. Perform / schedule correspondin

from input_output import getInputArgs, convertQuartileFlag
from input_output import printRangesToFiles, printBoolToFile, copyStartingFField
from forcefield_parser import processFF, getOldFFKeys, getFFData, minMax2outStr, bool2outStr, compareFFs, randomInitGuessStr
from filters import applyFilters
from nparrAnalysis import extractNeededKeys

import logging
import yaml # Used to dump a dictionary into a better, more readable format.


def process(options):
    if(options.inputYaml):
        logging.debug("YAML")
        #Handeled a level higher and if there is anything to be extracted - it should be extracted before.

    if (options.inputFF):
        logging.debug("FF")
        #FF(s) -> Obj for further actions; parse each of them; -> List of FF objects;
        ffs = [getFFData(ffpath) for ffpath in options.inputFF]
        ffsDB = [processFF(ffpath) for ffpath in options.inputFF] #similar to DB input;
        logging. debug("Force fields to process are gathered.")

    if (options.DBinput):
        logging.debug("DB")
        logging.debug('{:>50}'.format(" >> MAKING DATABASE FROM NEXT FILES: >> "))
        dataBase = [processFF(ffpath) for ffpath in options.DBinput]
        logger = logging.getLogger(__name__)

        logger.info('Printing DataBase in the separate file...')
        with open('dataBase.yml', 'w') as outfile:
            DByamlStr = yaml.dump(dataBase, outfile) #Now it's separate file #TODO: dump to yaml and print to logger!;
        #logging.debug('{} {}'.format('DataBase:', dataBase))
        logger.info('DataBase is printed.')

    if (options.params):
        # Todo: 
        #1. Extract ranges from the params file [as numpy array].
        #2. Use these ranges instead of DB.
        params = options.params
        print("Params files are here", params)


    #Needed to Normalise data:
    if (options.inMin and options.inMax):
        logging.debug("InMIN and InMax for normalisation.")
        inMinFF = processFF(options.inMin[0]) # Even though it shouldn't be a list, it is; easier now;
        inMaxFF = processFF(options.inMax[0])

    if (options.inputKeys):
        logging.debug("KEY(s); should be DICTIONARIES:")
        #to make a dictionary out of Key(s);

        # It should already be dictionary; // Maybe list of dictionaries;
        logging.debug(options.inputKeys)

        #key(s) -> Obj for further actions; 

    if (options.outputPath):
        logging.debug("Outpath")
        #Path for output {FFs, min/max}

    #__________action / analysis flags___________#
    #Some keys will only work in combination with the others! ex: inputFF / DataBase
    if (options.ranges): 
        logging.debug("Ranges...")
        # Do everything related to ranges handeling here; 
        # 1. TODO: check if there are any keys for alternative ranges; Default: minmax
        rangesFlag = convertQuartileFlag(options.ranges[0])
        logging.debug('{} {}'.format('Qflag = ', rangesFlag))

    if (options.check):
        logging.debug("Check...") 
        # This should reffer to some functon check....
        # This could include all of the gathered conditions 

    if (options.compare):
        logging.debug("Compare...")
        # KEYs or entire FFs could be compared:

        # 0. Check what to compare:
        keys = None
        whatToCompare = options.compare
        if whatToCompare == 'keys' or whatToCompare == 'k':
            logging.info('Specific keys from the ffs to be compared.')
            if options.keys:
                keys = options.keys # get Keys from inputKeys;

        if ffs and ffsDB:
            compareFFs(ffs, ffsDB, keys)

        # 2.KEY(s) in FF(s):
            #[0]. make DB of ffs // should be already done before; 
            #[1]. loop through the KEY(s)
            #[2]. For each Key: 
                #[3]. Check if it's present; should be done in another option;
                #[4]. Pair by pair: compare paramenetrs;

    if (options.detect):
        logging.debug("Detect...")

    if (options.ffInfo):
        logging.debug("Force Field info:")

    if (options.filter):
        logging.debug("Filter [DataBase]")

        if dataBase:
            print('Filter...')
            print(options.filter)
            applyFilters(options, dataBase)
    
    if (options.randGuess):
        oldKeys = getOldFFKeys(ffs)
        if options.params:
            print('Rand guess, based on params file.')
        else:
            guess = randomInitGuessStr(oldKeys, dataBase, False)
            copyStartingFField(guess, options)

    if (options.mcffInput):
        logging.debug("Generating input for MCFF optimiser")

        # 1. If there are any rangesFLags, it's specified above.
    
        # 2. Create min/max strings to pass to the file(s), based on input-file;
        oldKeys = getOldFFKeys(ffs)
        minMax = minMax2outStr(oldKeys, dataBase, rangesFlag)
        
        # 3. Write to files;
        printRangesToFiles(minMax, options)

        # 4. TODO: copy input forcefiled into ffiled file.
        copyStartingFField(ffs[0], options) # this should be streamed to ffield; # I'm considering only 1st ff, not to overwrite it; 

        # 5. Generate a bool file / based on keys;
        if options.keys:
            boolFile = bool2outStr(oldKeys, options.keys)
            printBoolToFile(boolFile, options)

    if (options.bool):
        logging.debug("Generating bool file [defining which parametrs to optimise]")
        # same as #4 in MCFF input. #2 for 'oldKeys' is also required. Maybe this step should be before mcffInputFlags:

    if (options.getKey):
        logging.debug("Key [from the file / DataBase]")

    if(options.nparr):
        logging.debug("Flag to get nparrays")

        if dataBase and options.keys:
            if inMinFF and inMaxFF:
                extractNeededKeys(dataBase, options.keys, inMinFF, inMaxFF)
            else:
                extractNeededKeys(dataBase, options.keys)
            #if options.inMIN and options.inMAX:   
               # normalise(matrix, minFF, maxFF)

    #__________filtering / detction flags___________#
    if (options.branch):
        logging.debug("Branch:")

    if (options.vanDerWaals):
        logging.debug("vanDerWaals")

    if (options.chargeMethod):
        logging.debug("charge Model:")

    if (options.logLevel):
        logging.debug("Log Level")
        # Set Log Level here; 

options = getInputArgs()
process(options)
