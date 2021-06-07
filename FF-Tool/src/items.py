#to deal with keys and values only;
#based on keys and values we'll create Items and Blocks: 
from parseString import getKeysAddValues
from ranges import gatherDataByKey, reverseKey
import io
import logging
import yaml
import ast


class Block:
    items = []
    num = 0
    name = ''
    def __init__(self, number = 0, name = None):
        self.items = []
        self.num = int(number)
        self.name = name

    def addItem(self, item):
        if item:
            self.items.append(item)

    def setNum(self, number):
        self.num = int(number)

    def setName(self, name):
        self.name = name

    def __print__(self):
        print("Block items")

    def __getitem__(self, key):
        return self.items[key]

    def __iter__(self):
        return iter(self.items)

    def __str__(self):
        return ">Block:\n" + "[name = %s, " %self.name + "# = %s]\n" %self.num + "%s" %("".join(str(item) for item in self.items))
        #return "Block: %s" %("\n".join(str(item) for item in self.items))
        # return "Block : [ %s ]" %(", ".join(str(item) for item in self.items))
    def __len__(self):
        return len(items)


class Item:
    keys = []
    values = []
    def __init__(self, key = [], value = []):
        #assert key
        #assert value 
        self.keys = key
        self.values = value

    def add(self, key, value):
        self.keys += key
        self.values += value

    def __print__(self):
        print ("Item Keys  :", self.keys)
        print ("Item Values:", self.values)

    def __str__(self): 
        #return "  Item Keys = %s" %self.keys + '\n  '+ "Item Values = %s" %self.values
        return "%s" %self.keys + "%s" %self.values + '\n'


def getPaperItem(keys):
    sub = "http://dx.doi.org"
    doi = "".join(s for s in keys if sub in s)
    if doi:
        return Item(['DOI'], doi)
    else:
        return None


def createNewBlock(keys):
    num = keys[0]
    name = keys[4] #ReaxFF format:
    name = ''.join(e for e in name if e.isalnum())
    return Block(num, name)


def createFFBlocks(data):
    lst = data.split('\n')
    blocks = []
    curBlock = Block();
    #curItem = Item();
    for l in lst:
        keyVal = getKeysAddValues(l)
        keys = keyVal[0]
        values = keyVal[1]

        #types of parsed string:
        newBlock = len(keys) >=2 and keys[1] == '!'
        emptyBlock = newBlock and keys[0] == 0
        newItem = len(keys) >=0 
        paramString = len(keys) == 0
        headerString =  len(values) == 0        

        if emptyBlock: #don't add a block if it's empty;
            logging.debug(" >> empty block ")

        if paramString: #add to current item 
            if curItem:
                curItem.add(keys, values)
            
        elif newBlock:
            #print "old curItem = %s" %curItem
            curBlock.addItem(curItem)
            blocks.append(curBlock)         
            curItem = None
            curBlock = createNewBlock(keys)
            
        elif headerString:
            curItem = getPaperItem(keys)
            if curItem:
                curBlock = Block(1 ,"info")

        elif newItem:
            curBlock.addItem(curItem)
            curItem = Item(keys, values)

    curBlock.addItem(curItem)
    #print("current block: ")
    blocks.append(curBlock) #otherwise last element isn't added; 


    #print "===Final object==="
    j = len(blocks)
    logging.debug("# of ff blocks: %s", j)

    # Uncomment to print blocks
    for i in range(j):
        logging.debug("====%s \n" %blocks[i])
    
    #last = len(blocks) - 1
    #print "The last block: %s" blocks[last]
    return blocks


def updateKeys(blocks):
    #print ("start of updateKeys")
    atoms = ['*']
    for b in blocks:
        #UNCOMMENT THIS!
        #print ("block name: %s; " %b.name + "block num: %s" %b.num)
        if (b.name == "atoms"):
            atoms += [b.items[index].keys[0] for index in range(b.num)]
            #print("ATOMS: %s" %atoms)

        elif (b.name == "general"): #creating 1 single list instead of list of itemst
            newItem = []
            newItem.append([b.items[index].values[0] for index in range(b.num)])
            b.items = newItem
            #b.values = [b.name]
            #print(b)

        elif (b.name != "info"): #to add reversed keys; 
            for item in b.items:
                #print("ITEM:", item)
                #print ("KEYS:", item.keys)
                item.keys = [atoms[int(x)] for x in item.keys]
                #item.keys = reversed(item.keys) #Maybe is not that needed; When accessing will check both: direct and reverse key.
                #print ("KEYS:  ", item.keys) #Uncomment here;
                #print("ITEM:", item, "\n")
    #print("end of updateKeys")


def createFFDictionaries(blocks):
    #print ("== Creating new dictionary ==")
    ff = {}

    for b in blocks:
        if (b.name == "general"):
            blockDict = b.items
        else: #for values with the same key
            blockDict = {}
            for item in b.items:
                keyStr = "-".join(str(item) for item in item.keys)
                if keyStr in blockDict.keys(): #if the key already exists, creating a list of items instead.
                    l = [blockDict[keyStr]]
                    l.append(item.values)
                    blockDict[keyStr] = l
                else:
                    blockDict[keyStr] = item.values
                #print "Key: %s " %keyStr + "  Dict: %s" %blockDict[keyStr]
                # "dictionary %s:" %blockDict
            #print "blockDict Length = %s" %len(blockDict)
            #print blockDict
        ff[b.name] = blockDict
    #print ("== Dictionary created ==")
    return ff   


def printBlock2Str(block):
    blockStr = ''
    #I just need to make a string instead of block; Same as print would do; [only for a string]
    #The same loop as I had for each item:
    
    #1. Add header;
    blockStr = addHeader(blockStr, block)
    #2. Add rest of the items;

    for item in block:
        keys = ' '.join(item.keys)
        values = item.values # Lst
        blockStr = ''.join([blockStr, printItem(keys, values)]) #strNumberKey

    return blockStr


def printItem(header, data): # Header == key; 
    # first we split the data in groups of 8 (like Hans suggested)
    #logging.debug("PrintItem starts!")

    chunks = [data[x:x+8] for x in range(0, len(data), 8)]
    #print('CHUNKS:', chunks)
    # Empty line heathers (except for the first one:)
    line_header = ['' for i in range(len(chunks))]
    line_header[0] = header

    format_line = '{:10}'
    itemStr = ''
    # Condition that it's not a list of lists:
    if isinstance(chunks[0][0], list):
        chunks[0] = chunks[0][0] # Bad solution. To print only nice data. 

    for i in range(len(chunks[0])): #To get format, depending on how much columns are included:
        format_line += ' {:8.4f}'
   
    for c,l in zip(chunks,line_header):
        st = format_line.format(l, *c)
        itemStr = ''.join([itemStr, st, '\n'])
    logging.debug('{} {}'.format('ItemStr', itemStr))
        #print(format_line.format(l,*c)) # *- is to unzip; # Should print it to the correct channel;
    #logging.debug("PrintItem ends!")
    return itemStr


def setGeneralBlock2Opt(block, opt=None):
    logging.debug('Setting general block to 0s.')
    for item in block:
        item.values = [0.0000]
    return block


def printGeneralParams(block):
    generalBlockStr = ''
    #generalBlockStr = ''.join([generalBlockStr, 'BEGIN func\n']) # In this line - there is extra space
    for item in block.items:
        outKey = ''.join(item.keys)
        generalParamStr = ' {:9.4f} {:9}\n'.format(item.values[0], outKey, '.4f')
        generalBlockStr = ''.join([generalBlockStr, generalParamStr])
    #generalBlockStr = ''.join([generalBlockStr, 'END func\n'])
    return generalBlockStr


def addHeader(mStr, block):
    try:
        #headerStr = ''.join([str(len(block.items)), ' ! ',block.name, '\n'])
        # Based on Ugly reaxff convensions; TODO: Try to run reaxff with more elegant header
        headerStr = ''.join([str(len(block.items)), ' ! Number of ',block.name, ' parameters\n'])
        mStr = ' '.join([mStr, headerStr])
        
        # Horrible, ugly solution, to make it compatiable with reaxff input;
        junkStr = 'Junk\n'
        if block.name == 'atoms':
            # 3 lines of junk
            mStr = ' '.join([mStr, junkStr, junkStr, junkStr])
        elif block.name == 'bonds':
            # 1 line of junk
            mStr = ' '.join([mStr, junkStr])
    except TypeError:
        logging.error('Cannot add header.')
    return mStr


def setItemParamToOpt(item, num = None): # num = list of parameter indeces to optimise, or '-A' if we need to optimise all;
    lstToOpt = [0 for i in item.values]
    logging.debug('{} {}'.format('lstToOpt', lstToOpt))
    if num: 
        if num == '-A': 
            lstToOpt = [1 for i in item.values]
        else: 
            #lstToOpt = [1 for n in num]
            for i in num:
                lstToOpt[i -1] = 1  #shift on '-1'; Because enumerating of params starts from 1 unstead of 0. 

    logging.debug('{} {}'.format('lstToOpt', lstToOpt))
    item.values = lstToOpt
    return item.values


def getBoolItemValStr(item, optKeys, strLetterKey):
    itemValStr = ''
    if strLetterKey in optKeys.keys():
        #Optimise defined param; set to 1;
        itemValStr = setParamToOpt(item, optKeys[strLetterKey])
    else:
        itemValStr = setParamToOpt(item) # set all to 0;
    return itemValStr


def setBlockToOpt(block, opt = False): #for every item/ either optimise or not;
    logging.debug('Setting whole block at once.')
    if opt:
        val = '-A'
    else:
        val = None

    for item in block:
        item = setItemParamToOpt(item, val)
    return block


def processInKEYs(keys2OptDict, keyFromBlock = None): #, atomsLst): # EX: (C, H, N, K): [1,2,5]
    # Maybe not only keyFromBlock, but also: 
    #provide(s) list of indexes for parameters to be optimised;
    logging.debug('Deciding, which params to optimise.')
    logging.debug('{} {}'.format('keysToOptDict', keys2OptDict))
    logging.debug('{} {}'.format('keyFromBlock', keyFromBlock))
    
    if (keys2OptDict == '-A'):
        logging.debug('Optimise all!')
        #setItemParamToOpt(keyFromBlock) <- in order to use this one - all str; Ideally should not occur; 
        return '-A'

    else:    
        optIndexSet = []#set()  # can use set instead of lst!!!
        for fragment in keys2OptDict:
            #StrKeyFromNumKey(fragment)
            logging.debug('{} {} {} {}'.format('whole fragment =', fragment, ' type =', type(fragment)))
            fragLst = fragment.split(', ') # Think over; I should get rid of ',' => Use it as separator! 
            logging.debug('{} {}'.format('Frags list', fragLst)) #Sometimes it's '-A'; Should be treated separately;
            paramLst = keys2OptDict[fragment]
            logging.debug('{} {}'.format('Corresponding params :', paramLst)) 

            #1. Turn num- based key into letter=based key;
            #   -> Atoms array is needed;
            #2. Check if the letterKey is to be optimised;
        
            #letterKey = StrKeyFromNumKey(keyFromBlock, keysOptLst)

            if keyFromBlock == None or str(keyFromBlock) in fragLst: # either element or a tuple!  # 
                logging.debug('{} {}'.format('Yes, present:', keyFromBlock))
                logging.debug('{} {} '.format('> type', type(paramLst)))
                #optIndexSet.append(paramLst)

                # The same is in function: alternativeGetKeysFromDict
                if (type(paramLst) == list):
                    logging.debug('Type : LST!')
                    optIndexSet.extend(paramLst)
                    logging.debug('{} {}'.format(' optIndexSet = ', optIndexSet))
                elif (type(paramLst) == int):
                    logging.debug('Type : INT!')
                    optIndexSet.append(paramLst)
                    logging.debug('{} {}'.format(' optIndexSet = ', optIndexSet))
                elif(type(paramLst) == str and paramLst == '-A'):
                    logging.debug('All params!')
                    optIndexSet = '-A' #Tell to optimise all; rest is parsed further at setItemParamToOpt;
                    logging.debug('{} {}'.format(' optIndexSet = ', optIndexSet))
            else:
                logging.debug('{} {}'.format('Not present:', keyFromBlock))
                # Key is not there; 
        
        logging.debug('{} {}'.format(' Params to opt', optIndexSet))
    return  optIndexSet


def inputBasedBoolStr(blocks, keysToOpt):
    boolStr = 'BOOL ReaxFF ff:\n' # Needed some junk str, to be parsed further by ReaxFF input 
    atoms = ['*']
    #1. Loop through all of the parameters in blocks; 
    #2. Check if parameter / block is present among keys: If so - set parameter to 1; else - leave 0;
    blocksToOptLst = keysToOpt.keys()

    # 'General block' should be added with item(s) set to 0; 

    for b in blocks:
        logging.debug(b.name)
        if (len(b.items) == 0 or b.name == 'info'): #means None:
            print("")
        else:
            
            #1. Check if the block with the specified block is present among keys:
            logging.debug('Check if the blockKey is present among keysToOpt')

            logging.debug(">> Just before the general block:")
            if (b.name == 'general'):
                logging.debug(">> General correct print:")
                boolStr = addHeader(boolStr, b)
                b = setGeneralBlock2Opt(b)
                generalBlockStr = printGeneralParams(b) # Is it the correct output ? 
                boolStr = ''.join([boolStr, generalBlockStr])
                logging.debug('{} {}'.format('General part pf the bool str\n', boolStr))
                logging.debug(">> Correct print is over:")

            #2. Getting  list atoms in ff to further refer to.
            elif (b.name == 'atoms'):
                #atoms += [b.items[index].keys[0] for index in range(b.num)]
                atoms = getAtomsLst(b)
                #for iten in b: 
                #    strLetterKey = item.keys#' '.join(item.keys)
                #    par2opt = optimiseWhichParam(strLetterKey, keyBlockVals)

            #Exclude general block from here!!!:
            if (b.name in blocksToOptLst) and (b.name != 'general'): # Not entirely correct; For atoms also needed;
                logging.debug('{} {} {}'.format(' >>>> ', b.name, '- block to opt'))
                boolStr = addHeader(boolStr, b)


                #2. Check if one should optimise whole block; If Value = '-A'
                keyBlockVals = keysToOpt[b.name] 
                logging.debug('{} {}'.format('TYPE:', type(keyBlockVals)))   

                if (type(keyBlockVals) == str and keyBlockVals == ' - A'):
                    logging.debug('Optimise whole block!')
                    b = setBlockToOpt(b, True)
                    boolStr = ''.join([boolStr, printBlock2Str(b)])

                elif(b.name != "general"): 
                 #3. If not - than [for every item]
                    logging.debug('Item by item ...')
                    
                    for item in b:
                        # For each item: we decide if it should be optimised or not; If so: which ones [params]?
                        strLetterKey = ' '.join(item.keys)
                        if (b.name == 'atoms'):
                            strKey = strLetterKey
                        else:
                            strKey = StrKeyFromNumKey(item, atoms)
                        logging.debug('{} {} {} {}'.format('item =', item.keys, '=> ', strKey))
                        logging.debug('{} {}'.format('keyBlockVals', keyBlockVals))
                        par2opt = processInKEYs(keyBlockVals, strKey)
                        #Generate bool string based on which params to optimise;

                        optVal = setItemParamToOpt(item, par2opt)
                        #Each item should be turned into str, right ?
                        boolStr = ''.join([boolStr, printItem(strLetterKey, optVal)]) #strNumberKey
            elif(b.name != 'general'): # excessive; better to reorganise the code;
                logging.debug('{} {}'.format(b.name, '- not here'))
                #Set all of the block to 0s; -> Add these '0' to the bool string;
                b = setBlockToOpt(b, False)
                boolStr = ''.join([boolStr, printBlock2Str(b)])
            logging.info('_______________________')

    logging.debug('{} {}'.format("Bool STR:\n", boolStr))
    return boolStr


def getAtomsLst(block):
    # Getting  list atoms in ff to further refer to.
    atoms = ['*']
    if (block.name == 'atoms'):
        atoms += [block.items[index].keys[0] for index in range(block.num)]
    return atoms


def StrKeyFromNumKey(item, atoms): # Atom(s) already contain information about direct and reverse;
    strNumberKey = '  '.join(item.keys)
    letterKey = [atoms[int(x)] for x in item.keys]
    strLetterKey = '-'.join(letterKey)
    return strLetterKey


def randomGuessInRanges(blocks, dataBase, rangesFlag):
    #These are the Strings instead of files; Files would be created out of it;
    rangesFlag = False
    randGuessFlag = True

    guessStr = 'Random ReaxFF ff:\n' # Had to write these junk lines, to have it compatiable with ReaxFF input:
    atoms = ['*']
    for b in blocks:
        logging.debug(b.name)
        logging.debug(b)
        if (len(b.items) == 0): #means None:
            print("")
        else:
             st = ''.join([str(len(b.items)), ' ! ', b.name, '\n']) # <-This string should be added somewhere

        logging.debug('{} {}'.format('$$$ Block name: >>> ', b.name))
        print(' >> ', b.name)
        if (b.name == "general"): #creating 1 single list instead of list of itemst
            #printGeneralParamsToBothChannels(b, minFile, maxFile)
            guessStr = addHeader(guessStr, b)

            generalBlockStr = printGeneralParams(b) # TODO: Get general parameters instead. 
            guessStr = ' '.join([guessStr, generalBlockStr]) #minFile)]) # MIN # I should print them in different files;

        elif (b.name == "atoms"):
            guessStr = addHeader(guessStr, b)

            atoms += [b.items[index].keys[0] for index in range(b.num)]
            logging.debug("ATOMS: %s" %atoms)

            logging.debug("Are there any items ?")
            for item in b.items:
                strLetterKey = ' '.join(item.keys)
                #strKey = directAndReverseKeyStrFromNumKey(item.keys, atoms) <- Not sure yet;
                # Maybe I should check reverse keys here as well !? Sounds reasonable. reverseKey
                # WHat about reverse key ?

                guess = gatherDataByKey(dataBase, b.name, strLetterKey, rangesFlag, randGuessFlag)
                logging.debug('{} {}'.format('GUESS', guess))

                logging.debug('{} {}'.format("keys:", strLetterKey))
                guessStr = ''.join([guessStr, printItem(strLetterKey, guess)]) # guess[0] ? 

        elif (b.name != "info"):
            guessStr = addHeader(guessStr, b)

            for item in b.items:
                strNumberKey = '  '.join(item.keys)
                strLetterKey = StrKeyFromNumKey(item, atoms)
                #print(strLetterKey, ' | ', end=' ')
                # 1.+ Get the right key[numbers]; Already printed out;
                # 2.+ Transfer the key into key[letters];
                # 3.+ Make a (std) string out of it; 
                # 4.+ Pick the right item, based on the key.
                # 5.+ Use PrintItem to correctly print out the results.
                logging.debug("About to get initial guess for non-atoms block")
                guess = gatherDataByKey(dataBase, b.name, strLetterKey, rangesFlag, randGuessFlag) #strLetterKey
                #TODO: uncomment this:
                #logging.debug('{} {}'.format("strNumKey", strNumberKey))
                try:
                    guessStr = ''.join([guessStr, printItem(strNumberKey, guess)]) # guess[0] ? 
                except TypeError:
                    logging.error('Type Error has occured')
            #logging.debug('{} {} {}'.format('guess str -> file', guessStr))
    return guessStr


def inputFFBasedMinMaxStr(blocks, dataBase, rangesFlag): # Keys uzhe pochemu-to updated; Maybe, because of pointers; 
    #These are the Strings instead of files; Files would be created out of it;
    minStr = 'MIN ReaxFF ff:\n' # Had to write these junk lines, to have it compatiable with ReaxFF input:
    maxStr = 'MAX ReaxFF ff:\n'
    atoms = ['*']
    for b in blocks:
        logging.debug(b.name)
        logging.debug(b)
        if (len(b.items) == 0): #means None:
            print("")
        else:
             st = ''.join([str(len(b.items)), ' ! ', b.name, '\n']) # <-This string should be added somewhere

        logging.debug('{} {}'.format('$$$ Block name: >>> ', b.name))
        print(' >> ', b.name)
        if (b.name == "general"): #creating 1 single list instead of list of itemst
            #printGeneralParamsToBothChannels(b, minFile, maxFile)
            minStr = addHeader(minStr, b)
            maxStr = addHeader(maxStr, b)

            generalBlockStr = printGeneralParams(b) # TODO: Get general parameters instead. 
            minStr = ' '.join([minStr, generalBlockStr]) #minFile)]) # MIN # I should print them in different files; 
            maxStr = ' '.join([maxStr, generalBlockStr]) #maxFile) # MAX
            #instead have a generalBlockStr:
            #append this string to minStr, maxStr; 

        elif (b.name == "atoms"):
            minStr = addHeader(minStr, b)
            maxStr = addHeader(maxStr, b)

            atoms += [b.items[index].keys[0] for index in range(b.num)]
            logging.debug("ATOMS: %s" %atoms)

            logging.debug("Are there any items ?")
            for item in b.items:
                strLetterKey = ' '.join(item.keys)
                #strKey = directAndReverseKeyStrFromNumKey(item.keys, atoms) <- Not sure yet;
                # Maybe I should check reverse keys here as well !? Sounds reasonable. reverseKey
                # WHat about reverse key ?
                minmax = gatherDataByKey(dataBase, b.name, strLetterKey, rangesFlag)
                logging.debug('{} {}'.format('MINMAX', minmax))

                logging.debug('{} {}'.format("keys:", strLetterKey))
                minStr = ''.join([minStr, printItem(strLetterKey, minmax[0])]) #minFile)]) # MIN # I should print them in different files; 
                maxStr = ''.join([maxStr, printItem(strLetterKey, minmax[1])]) #maxFile) # MAX

        elif (b.name != "info"):
            minStr = addHeader(minStr, b)
            maxStr = addHeader(maxStr, b)

            for item in b.items:
                strNumberKey = '  '.join(item.keys)
                strLetterKey = StrKeyFromNumKey(item, atoms)
                #print(strLetterKey, ' | ', end=' ')
                # 1.+ Get the right key[numbers]; Already printed out;
                # 2.+ Transfer the key into key[letters];
                # 3.+ Make a (std) string out of it; 
                # 4.+ Pick the right item, based on the key.
                # 5.+ Use PrintItem to correctly print out the results.
                logging.debug("About to get ranges for non-atoms block")
                minmax = gatherDataByKey(dataBase, b.name, strLetterKey, rangesFlag) #strLetterKey
                #TODO: uncomment this:
                #logging.debug('{} {}'.format("strNumKey", strNumberKey))
                try:
                    minStr = ''.join([minStr, printItem(strNumberKey, minmax[0])]) #minFile)]) # MIN # I should print them in different files; 
                    maxStr = ''.join([maxStr, printItem(strNumberKey, minmax[1])]) #maxFile) # MAX
                except TypeError:
                    logging.error('Type Error has occured')
            logging.debug('{} {} {}'.format('Min(s) and Max(s) str -> file', minStr, maxStr))
    return (minStr, maxStr)