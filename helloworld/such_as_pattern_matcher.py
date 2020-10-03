from pattern_matcher import PatternMatcher
from spacy.tokens import Doc
from relation import Relation

class SuchAsPatternMatcher(PatternMatcher):

    __matcherId: str

    def __init__(self, nlp):
        pattern = [{'POS': 'NOUN'},
                   {'IS_PUNCT': True, 'OP': '?'},
                   {'LOWER': 'such'},
                   {'LOWER': 'as'},
                   {'POS': 'NOUN'}]
        self.__matcherId = "suchAs"
        PatternMatcher.__init__(self, pattern, nlp, self.__matcherId)
        
    def getRelations(self, doc: Doc) -> [Relation]:
        relations = []
        matches = self._matcher(doc)

        for match_id, start, end in matches:
            span = doc[start:end]
            hypernym = span.root.text
            hyponym = span.text.split()[-1]

            relations.append(
                Relation(
                    hypernym,
                    hyponym,
                    self.__matcherId
                )
            )

            for right in span.rights:
                if right.pos_ == "NOUN":
                    relations.append(
                        Relation(
                            hypernym,
                            right.text,
                            self.__matcherId
                        )
                    )
        return relations
        