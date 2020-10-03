from pattern_matcher import PatternMatcher
from spacy.tokens import Doc
from relation import Relation

class AndOtherPatternMatcher(PatternMatcher):
    '''
     Look for structures containing 4 words: 
        the first word is a NOUN (POS stands for Part-Of-Speech), 
        second word is <<and>>, 
        third is <<other>>
        last word is also a Noun
    '''
    __matcherId: str

    def __init__(self, nlp):
        pattern = [
            {'POS': 'NOUN'},
            {'Lower': 'and'},
            {'Lower': 'other'},
            {'POS': 'NOUN'},
        ]
        self.__matcherId = "andOther"
        PatternMatcher.__init__(self, pattern, nlp, self.__matcherId)
    
    def getRelations(self, doc) -> [Relation]:
        relations = []
        matches = self._matcher(doc)
        
        for match_id, start, end in matches:
            span = doc[start:end]
            firstToken = span.root.head
            results = [firstToken]
            
            while firstToken and firstToken.head.pos_ == "NOUN":
                results.append(firstToken.head)
                firstToken = firstToken.head
            
            hypernym = span.text.split()[-1]
            relations.append(Relation(hypernym, span.text.split()[0], self.__matcherId))

            if len(results) > 0:
                for result in results:
                    relations.append(Relation(hypernym, result.text, self.__matcherId))
        
        return relations