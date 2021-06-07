#TABS! pay attantion!


class ForceField:

    i = 123  # -> What is the use of this?

    def __init__(self, blocks=None):
        self.info = self.Info()
        self.General = self.General(blocks[1])

    def getInfo(self):
        return self.info

# You do not put a class inside a class there is not point in doing so


class Info(object):
    """
    #list; TODO: this one
    """
    def __init__(self):
        self.data = []
        # 1: name of the ff
        # 2. DOI

    def set(self, value):
        self.data.append(value)

    def get(self):
        return self.data

    def pr(self):
        print(self)

    # I DO NO SEE WHY DO YOU WANT TO OVERWRITE THIS METHOD
    def __print__(self):
        print("Info item:")


# Rest of the blocks should just set those inner objects to blocks;


class General:
    """ 1 """
    data = [] # TODO: transfer to tuple at some point

    def __init__(self, block = None):
        self.data = block

    def set(self, blocks):
        """
        # here Block - list of items: keys - unimportant; values - are;
        #print "======Set function=======:"
        """
        lstOfItems = blocks[1]
        # print lstOfItems
        # params = lstOfItems[2]
        # print "params =  %s" %params
        # self.data = (params[0])
        # print "self data = %s" %self.data

    # Are you sure you want to do this? the __str__ should be enough.
    def __print__(self):
        print(self.data)

    def __str__(self):
        return "General >> : %s" % ("".join(str(item) for item in self.data))
