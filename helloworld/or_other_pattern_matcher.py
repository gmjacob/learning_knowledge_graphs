from pattern_matcher import PatternMatcher
from spacy.tokens import Doc
from relation import Relation

class OrOtherPatternMatcher(PatternMatcher):

    __matcherId: str
    
    def __init__(self, nlp):
        pattern = [
            {'POS': 'NOUN'},
            {'Lower': 'or'},
            {'Lower': 'other'},
            {'POS': 'NOUN'},
        ]
        self.__matcherId = "orOther"
        PatternMatcher.__init__(self, pattern, nlp, self.__matcherId)

    def getRelations(self, doc: Doc) -> [Relation]:
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

            relations.append(
                Relation(hypernym, span.text.split()[0], self.__matcherId)
            )

            if len(relations) >0:
                for result in results:
                    relations.append(
                        Relation(hypernym, result.text, self.__matcherId)
                    )
        return relations