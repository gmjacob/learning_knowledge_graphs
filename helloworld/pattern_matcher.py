from spacy.matcher import Matcher
from spacy.tokens import Doc

from abc import abstractmethod
from relation import Relation

'''
    Base class for pattern matchers
'''
class PatternMatcher:
    '''
        pattern: The pattern to be matched
        nlp: Spacys nlp module
        matcherId: So that we know which mathcher the result came from
    '''
    def __init__(self, pattern, nlp, matcherId):
        super().__init__()
        self._matcher = Matcher(nlp.vocab)
        self._matcher.add(matcherId, None, pattern)
    
    # method to be implemented by all subclasses
    @abstractmethod
    def getRelations(self, doc: Doc) -> [Relation]:
        ...