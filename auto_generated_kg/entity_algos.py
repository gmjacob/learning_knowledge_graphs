import pandas as pd
import re
import spacy 
import neuralcoref
#Load the English large web model
nlp = spacy.load("en_core_web_md")
neuralcoref.add_to_pipe(nlp)

def entity_pairs(text, coref=True):
    # replace multiple new lines with '.'
    text = re.sub(r'\n+','. ', text)
    # remove reference numbers
    text = re.sub(r'\[\d+\]', ' ', text)
    # Load language model with the text base
    text = nlp(text)

    if coref:
        # resolve coreference clusters
        # he, she, them etc will be replaced by the entity noun that they refer to
        text = nlp(text._.coref_resolved)
    # split text into an array of sentences and remove any extra spaces
    sentences = [sent.string.strip() for sent in text.sents]
    # initialise entity pairs list
    ent_pairs = list()

    for sent in sentences:
        #create the langauge model for each sentence
        sent = nlp(sent)
        #Create a list that contains the sentences entities and noun chucks
        spans = list(sent.ents) + list(sent.noun_chunks)
        #Filter a sequence of span objects and remove duplicates or overlaps. 
        #Removes overlapping entities and noun chunks
        spans = spacy.util.filter_spans(spans)
        print("sentence ->\n", sent)
        print("spans ->\n", spans)

        with sent.retokenize() as retokenizer:
            [retokenizer.merge(span) for span in spans]

        # dep = [token.dep_ for token in sent]
        
        # limit our example to simple sentences with one subject and object
        # if (dep.count('obj') + dep.count('dobj')) != 1\
        #         or (dep.count('subj') + dep.count('nsubj')) != 1:
        #         print("multiple instances, continue..")
        #         continue
        
        for token in sent:
            # identify object nodes
            if token.dep_ not in ('obj', 'dobj'):
                continue
            # Subject or nominal subject
            subject = [w for w in token.head.lefts if w.dep_ in ('subj', 'nsubj')]

            if subject:
                subject = subject[0]
                # identify relationship by root dependency
                relation = [w for w in token.ancestors if w.dep_ == 'ROOT']
                if relation:
                    relation = relation[0]
                    # add adposition or particle to relationship
                    # https://spacy.io/api/token#nbor - nbor reference
                    if relation.nbor(1).pos_ in ('ADP', 'PART'):
                        relation = ' '.join((
                            str(relation),
                            str(relation.nbor(1))
                        ))
                else:
                    relation = 'unknown'
                
                subject, subject_type = refine_ent(subject, sent)
                token, object_type = refine_ent(token, sent)
                
                ent_pairs.append([
                    str(subject),
                    str(relation),
                    str(token),
                    str(subject_type),
                    str(object_type),
                ])
    
    filtered_ent_pairs = [
        sublist for sublist in ent_pairs
        if not any(str(x) == '' for x in sublist)
        ]
    
    pairs = pd.DataFrame(
        filtered_ent_pairs,
        columns=['subject', 'relation', 'object', 'subject_type', 'object_type']
    )

    print('Entity pairs extracted: ', str(len(filtered_ent_pairs)))
    # print(pairs.to_csv('entity_pairs.csv', index = True))
    return pairs

"""
    @description: For the entity in a sentence, if its a phrase, it removes all the 
    unwanted tokens from the phrase and returns.
    If the entity is a nominal, cardinal or ordinal type, it builds the entity value
    If its neither, it returns the initial values
"""
def refine_ent(ent, sent):
    unwanted_tokens = (
        'PRON',  # pronouns
        'PART',  # particle
        'DET',  # determiner
        'SCONJ',  # subordinating conjunction
        'PUNCT',  # punctuation
        'SYM',  # symbol
        'X',  # other
    )
    ent_type = ent.ent_type_
    
    if ent_type == '':
        # in this case the entity is not determined, as it is a noun phrase  
        ent_type = 'NOUN_CHUNK'
        # In the noun phrase, for each token, remove unwanted tokens and stop words
        ent = ' '.join(str(t.text) for t in
                nlp(str(ent)) if t.pos_
                not in unwanted_tokens and t.is_stop == False)
    elif ent_type in ("NOMINAL", "CARDINAL", "ORDINAL") and str(ent).find(' ') == -1:
        # Cardinal -> Counting numbers
        # Ordinal -> first, second, third etc.
        # Nominal -> a word or word group functioning as a noun
        t = ''
        for i in range(len(sent)-ent.i):
            """
            for the entity and each word in front of the entity in the document
            if the word is not a verb or a punctuation,
              add it to the text that will form the entity 
            else 
              when a verb or punctuation is encountered, 
              set the entity as t and end the iteration
            """
            if ent.nbor(i).pos_ not in ('VERB', 'PUNCT') :
                t += ' ' + str(ent.nbor(i))
            else:
                ent = t.strip()
                break
        
    return ent, ent_type