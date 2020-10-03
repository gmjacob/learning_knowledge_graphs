class Relation:

    __hypernym: str
    __hyponym: str
    __matcher: str

    def __init__(self, hypernym, hyponym, matcher):
        self.__hypernym = hypernym
        self.__hyponym = hyponym
        self.__matcher = matcher
    
    def getHypernym(self):
        return self.__hypernym

    def getHyponym(self):
        return self.__hyponym
    
    def getMatcherId(self):
        return self.__matcher