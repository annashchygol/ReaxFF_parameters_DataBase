# This would be to detect VdW Type:
import argparse
from items import createFFBlocks
from items import updateKeys
from items import createFFDictionaries
from items import gatherFFInfo
from copy import deepcopy


def main(options):
    for ffinpath in options.inputFFRanges:  # Neopnyatno zachem for.
        with open(ffinpath, 'r') as ffinfile:
                ffindata = ffinfile.read()
        inBlocks = createFFBlocks(ffindata)

        print("InBlocks:", inBlocks)
        # Before update; This is just a pointer to the same list; I need a deep copy instead;
        inBlocksOldKeys = deepcopy(inBlocks)  # You are not using this
        updateKeys(inBlocks)
        ffinDict = createFFDictionaries(inBlocks)

        print("By now everything is fine:)")

        gatherFFInfo(ffinDict, 'NAME')

    print("Branch:", ffinDict['info']['branch'])
    print("VdWType", ffinDict['info']['VdWtype'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputForRanges', '-i', action='append', dest='inputFFRanges', default=[])

    options = parser.parse_args()

    main(options)
