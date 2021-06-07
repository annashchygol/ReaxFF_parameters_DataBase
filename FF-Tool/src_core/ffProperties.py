import logging

#__________FF Properties____________#

def printFF(ff): # Still amount of digits is a bit different;
    print("Printing force fields:")
    for block in ff:        
        if (block != None and block!= "general"):
            #if (block != "general"):
            print(len(block), block) #, ff[block]);
            for item in ff[block]:
                print( repr(item).ljust(10), end=' ')
                j = 0
                for i in ff[block][item]:
                    #j += 1
                    if j >= 8:
                        print()
                        j = 0
                        print(str(' ').rjust(10), end=' ')

                    print(repr(i).rjust(8), end=' ') #add condition: <= 8 columns;      
                    j += 1          
                print(' ')


def nicePrintFF(ff):
    print("________________________Nicer print:________________________")
    for block in ff:
        if (block != None and block != "general" and block != "info"):
            print(len(ff[block]), '!', block)
            for item in ff[block]:
                printItem(item, ff[block][item])
    print("____________________________________________________________")


def detectBranch(ff):  #TODO: add proper condition for COMBUSTION branch: 'combustion'
    #INDEPENDENT: By default
    #WATER:       Hydrogen Bond: O-H-O: "2.1200  -3.5800   1.4500  19.5000"
    #COMBUSTION:  C-O dissosiation energies # C-O bond  # same as in CHO.ff ? 

    ff['info']['branch'] = 'independent' # By default: branch set to 'combustion'
    waterKey = "O-H-O"
    combustKey = 'C-O'

    # First, check if it's combustion. [Some of 'water' ff can end up here]  
    if ff['bonds'] and combustKey in ff['bonds']:
        ff['info']['branch'] = 'combustion' # At first only presence of the 'C-O' key is checked: 

    # Secondly, check condition for water branch;
    if 'hydrogen' in ff and waterKey in ff['hydrogen']:
        waterBranchCondition = ff['hydrogen']['O-H-O'][1] == -3.5800 and ff['hydrogen']['O-H-O'][2] == 1.4500
        if waterBranchCondition:
            ff['info']['branch'] = 'water'
    
    logging.info('{} {}'.format('Branch =', ff['info']['branch']))


def addFFName(ff, name):
    ff['info']['name'] = name
    print('   *',ff['info']['name'])
    logging.info('{} {}'.format('name =', ff['info']))


def addChargeMethod(ff):
    ff['info']['chargeMethod'] = 'EEM'
    generalBlock = ff['general'][0] # <- This is silly! Why there is a list inside list ? 
    chargeModel = 'EEM'

    #ACKS2 condition: presence of general paramter #35
    if generalBlock[34] != 0.5: #34, because we start from 0; All EEM params # 34 == 0.5; 
        ff['info']['chargeMethod'] = 'ACKS2'
    logging.info('{} {}'.format ('charge method:', ff['info']['chargeMethod']))


def addVanDerWaalsType(ff):
    #Inner Wall condition : ratomparam(:,30)>0.01 .and. ratomparam(:,32)>0.01
    #Shielding condition  : ratomparam(:,10)>0.5
    
    #print("Adding Van der Waals condition:")
    ff['info']['VdWtype']='No inner wall, no shielding'
    
    # Setting vdw type for the first atom;
    prevShiledCondition = None
    prevIwCondition = None
    shieldingCondition = None
    innerWallCondition = None

    for atomParams in ff['atoms'].values(): #loop through list of atoms;

        prevShiledCondition = shieldingCondition
        prevIwCondition = innerWallCondition

        l = atomParams

        #print ("lll:","params #10, #30, #32",l[9], l[29], l[31]) #!Indexes - are starting from 0

        shieldingCondition = l[29] > 0.01 and l[31] > 0.01
        innerWallCondition = l[9] > 0.5

        # Check for ff consistency: All of the ff atoms have the same vdw type;
        inconsistency = prevIwCondition != innerWallCondition or shieldingCondition != prevShiledCondition
        if prevIwCondition != None and prevShiledCondition != None and inconsistency:
            print('Inconsistent vdw type!!!') # Why don't I get here ?
            logging.error('Inconsistent vdw type!')
            ff['info']['VdWtype'] = 'Inconsistent'
            return

    if shieldingCondition:
        if innerWallCondition:
            ff['info']['VdWtype']='Inner wall, Shielding'
        else:
            ff['info']['VdWtype']='No inner wall, Shielding'
    elif innerWallCondition:
        ff['info']['VdWtype']='Inner wall, No shielding'
    logging.info('{} {}'.format ('vdw type =', ff['info']['VdWtype']))


def gatherFFInfo(ff, name):
    #print("gathering FF info")
    if 'info' not in ff.keys():
        ff['info']={}
    addFFName(ff, name)
    detectBranch(ff)
    addChargeMethod(ff)
    addVanDerWaalsType(ff)
    print ('    ', ff['info'])
