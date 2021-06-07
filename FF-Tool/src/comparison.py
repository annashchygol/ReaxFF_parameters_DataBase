from items import processInKEYs
from ranges import reverseKey
import logging

def ff_have_same_blocks(ff1,ff2):
    return True

# Comparison between list and list of lists (of params). 
# returns True, if there are any 'overlapping keys' in both lists
# If values are exactly the same - this should be checked before calling this function; 
def partlyTheSameVals(val1, val2):
    same = []
    if isinstance(val1[0], list) and isinstance(val2[0], list):
        same = [True for v1 in val1 for v2 in val2 if v1 == v2]

    elif isinstance(val1[0], list):
        same = [True for v in val1 if v == val2]

    elif isinstance(val2[0], list): # can just swap val1 and
        same = [True for v in val2 if v == val1]

    if same:
        #print('partly the same values ... ', val1, val2) # One of the keys is the same as in another list
        return True
    else:
        return False 


def extractBlockKeys(b, keysFromInput):
    logging.info('Extracting input keys per block.')

    inKeys = processInKEYs(keysFromInput[b]) # <- Set it to something; Pass it further; should be reasonable obj;
    logging.debug('{} {}'.format('Input key(s):', inKeys))
    neededKeys = []

    if (inKeys == '-A'):  # Now it's the same behaviour as for the absent blocks; But should be different; absent blocks in Keys shouldn't be processed
        return '-A'
    else:
        neededKeys = keysFromInput[b].keys() # Not that straghtforward! Sometimes parse the line; 
        indeed_neededKeys = [k.split(', ') for k in neededKeys]
        indeed_neededKeys = [item for sublist in indeed_neededKeys for item in sublist]
        logging.debug('{} {}'.format('extrected keys:', indeed_neededKeys))
        return indeed_neededKeys


def outPrint(text, listName):
    if listName:
        print(text, listName)


def compareFFsDict(ff1, ff2, keysFromInput= None, skip_blocks=['info', 'general'], unreversable_blocks = ['atoms', 'hydrogen']): # Key will play a role of a filter; Compare 'key' from ff1 and ff2, lst
    #print('Comparison of 2 force fields:')
    if not ff_have_same_blocks(ff1,ff2):
        return False

    if keysFromInput:
        print(' Requested keys:', keysFromInput) # Dictionary ok keys

    blocks = ff1.keys()

    for b in blocks:

        if b and (b not in skip_blocks):
        
            #print('This block matches:', b) # Don't really have to print it.
            neededKeys = []
            inputKeyCondition = keysFromInput and b in keysFromInput.keys()

            if (ff1[b] == ff2[b]):
                if inputKeyCondition or keysFromInput == None:
                    print('{} {:12} {}'.format(' > ', b, '- same blocks'))
            else:

                keys1 = set([k for k in ff1[b]])
                keys2 = set([k for k in ff2[b]])

                #print('Keys lists: \n k1 =', keys1, '\n k2 =', keys2)

                common_keys = keys1.intersection(keys2)  # Nice try! #wouldn't work immedeiately compare direct and reverse keys!
                absent_keys1 = keys1 - keys2
                absent_keys2 = keys2 - keys1

                # 1. For Common Keys:
                same_keys = set(k for k in common_keys if ff1[b][k] == ff2[b][k] )
                diff_keys = common_keys - same_keys 
                partial_match = set(k for k in diff_keys if partlyTheSameVals(ff1[b][k], ff2[b][k]) ) #comparing list vs list of lists 

                
                # 2. Reverse keys, that are left:
                if (b not in unreversable_blocks):
                    # Reversing second diff; 
                    diff_keys2_reverse = {reverseKey(key) for key in absent_keys2}
                    common_with_reverseKeys = diff_keys2_reverse.intersection(keys1)

                    # Substracting the ones, which turned out to be the same after reverse;
                    reverse_diff_k2 = diff_keys2_reverse - common_with_reverseKeys
                    absent_keys1 = absent_keys1 - common_with_reverseKeys # ==> ABSENT_KEYS
                    absent_keys2 = {reverseKey(key) for key in reverse_diff_k2} # reversing back;

                    # For common with reverse Keys:
                    same_reverse_keys = {k for k in common_with_reverseKeys if ff1[b][k] == ff2[b][reverseKey(k)] }
                    same_keys.union(same_reverse_keys)

                    # The rest is added to diff keys: [Direct key for ff1]
                    diff_reverse_keys = common_with_reverseKeys - same_reverse_keys
                    diff_keys.union(diff_reverse_keys)

                    partial_match_reverse = {k for k in diff_reverse_keys if partlyTheSameVals(ff1[b][k], ff2[b][reverseKey(k)]) }
                    partial_match.union(partial_match_reverse)

                diff_keys = diff_keys - partial_match
                

                #Everything related to inputKeys;    
                if inputKeyCondition:
                    neededKeys = extractBlockKeys(b, keysFromInput) # Ideally to get rid of ff1 and ff2 -> Transferable / universal func;     
                    
                #Output for keys:
                if inputKeyCondition and neededKeys != '-A': # second condition is to avoid failing;
                    print (' > ', b)

                    format_str = '{:>5} {}'
                    for k in neededKeys:
                        if k in absent_keys2:
                            print(format_str.format(k, '- absent in ff1'))
                        if k in absent_keys1:
                            print(format_str.format(k, '- absent in ff2'))
                        elif k in same_keys:
                            print(format_str.format(k, '- same'))
                        elif k in diff_keys:
                            print(format_str.format(k, '- different'))
                        elif k in partial_match:
                            print(format_str.format(k, '- partial match'))

                    #Alternative: intersection between needed_keys and other dicts;  Todo this, I need to set to needed keys smth; 

                else:
                    if keysFromInput == None or (keysFromInput and neededKeys and neededKeys == '-A'): # This should describe both: '-A' block and whole files; 
                    # Output for files:
                        print (' > ', b)

                        if absent_keys1 or absent_keys2:
                            print ("  ===ABSENT KEYS ===:")
                            outPrint('  in ff2:', absent_keys1)
                            outPrint('  in ff1:', absent_keys2)
                        outPrint("  ===SAME KEYS ===:", same_keys) 
                        outPrint("  ===DIFF KEYS ===:", diff_keys)
                        outPrint("  ===PART.MATCH KEYS===:", partial_match)

            #else:
                #Otherwise we do not get here: #
                #print('{} {:12} {}'.format(' > ', b, '- same blocks')) # not really the case now. Think it over!


#To compare general blocks of 2 ffields => Conclusion if we can combine them, or not.
# TODO: rewrite it into 
def compareGeneralBlocksOf2FF(ff1Blocks, ff2Dict):
    print("\nComparison of parameters from general block:")
    #print("\nff1Blocks", ff1Blocks[1]) #<- This refers to block with general parametesrs; 
    #print("\nff2Dict, general block\n", ff2Dict['general'][0])
    #This is to check first if there are general parameters at all;
    if (ff1Blocks[1] == ff2Dict['general'][0]):
        print("Lists are equal")
    else:
        for i in range(0, len(ff2Dict['general'][0])):
            if (ff1Blocks[1][0][i] != ff2Dict['general'][0][i]): #<- because it's list inside the list;
                print("Diff param #", i, " == ",ff1Blocks[1][0][i], "!=", ff2Dict['general'][0][i]) 
    print("\nComparison is over!")
